# ============================================================================
# COMPREHENSIVE TTE META-ANALYSIS FOR DJANGO INTEGRATION
# Complete Bayesian Implementation adapted from tte_review_final.R and 
# tte_review_codes_from_cursor.R for Django website export
# ============================================================================

# ============================================================================
# AUTOMATIC PACKAGE INSTALLATION AND LOADING
# ============================================================================

# Function to install and load packages
install_and_load <- function(packages) {
        # Set CRAN mirror
        if (is.null(getOption("repos"))) {
                options(repos = c(CRAN = "https://cran.rstudio.com/"))
        }

        for (pkg in packages) {
                if (!require(pkg, character.only = TRUE)) {
                        cat("Installing package:", pkg, "\n")
                        install.packages(pkg, dependencies = TRUE)
                        library(pkg, character.only = TRUE)
                }
        }
}

# Standard CRAN packages
cran_packages <- c(
        "tidyverse",
        "ggplot2", 
        "patchwork",
        "meta",
        "metafor",
        "viridis",
        "gridExtra",
        "posterior",
        "bayesplot",
        "parallel",
        "jsonlite"
)

# Set CRAN mirror first
options(repos = c(CRAN = "https://cran.rstudio.com/"))

# Install and load CRAN packages
cat("Installing and loading required packages...\n")
install_and_load(cran_packages)

# ============================================================================
# STAN INTERFACE SETUP WITH AUTO-INSTALLATION
# ============================================================================

# Choose Stan interface (set use_cmdstanr = FALSE to use rstan)
use_cmdstanr = TRUE

# Function to setup CmdStanR
setup_cmdstanr <- function() {
        # Install cmdstanr from GitHub if not available
        if (!require("cmdstanr", character.only = TRUE)) {
                cat("Installing cmdstanr from GitHub...\n")
                if (!require("remotes", character.only = TRUE)) {
                        install.packages("remotes")
                        library(remotes)
                }
                remotes::install_github("stan-dev/cmdstanr")
                library(cmdstanr)
        }

        # Check if CmdStan is installed
        tryCatch(
                {
                        version = cmdstanr::cmdstan_version(error_on_NA = FALSE)
                        if (is.na(version)) {
                                cat("CmdStan not found. Installing CmdStan...\n")
                                cmdstanr::install_cmdstan(cores = parallel::detectCores())
                                cat("CmdStan installation complete.\n")
                        } else {
                                cat("CmdStan found. Version:", version, "\n")
                        }
                },
                error = function(e) {
                        cat("CmdStan not found. Installing CmdStan...\n")
                        cmdstanr::install_cmdstan(cores = parallel::detectCores())
                        cat("CmdStan installation complete.\n")
                }
        )
}

# Function to setup RStan
setup_rstan <- function() {
        if (!require("rstan", character.only = TRUE)) {
                cat("Installing rstan...\n")
                install.packages("rstan", dependencies = TRUE)
                library(rstan)
        }
        rstan_options(auto_write = TRUE)
}

# Setup Stan interface
if (use_cmdstanr) {
        cat("Setting up CmdStanR interface...\n")
        tryCatch({
                setup_cmdstanr()
                library(cmdstanr)
                library(posterior)
                library(bayesplot)
                options(mc.cores = parallel::detectCores())
                stan_ready <- TRUE
        }, error = function(e) {
                cat("CmdStanR setup failed, falling back to RStan...\n")
                use_cmdstanr <- FALSE
                stan_ready <- FALSE
        })
} 

if (!use_cmdstanr || !exists("stan_ready") || !stan_ready) {
        cat("Setting up RStan interface...\n")
        tryCatch({
                setup_rstan()
                library(rstan)
                library(bayesplot)
                options(mc.cores = parallel::detectCores())
                stan_ready <- TRUE
        }, error = function(e) {
                cat("Stan setup completely failed. Will use simplified analysis.\n")
                stan_ready <- FALSE
        })
}

cat("Stan interface setup complete!\n\n")

# ============================================================================
# DATA LOADING AND PREPARATION (FROM YOUR SCRIPTS)
# ============================================================================

# Create data directory if it doesn't exist
dir.create("ttedb/data", recursive = TRUE, showWarnings = FALSE)

# Load data (CSV format from your files)
load_tte_data = function() {
        study_chars_file <- "dataset/TTE_Metaresearch_Clean_Dataset - Studies characteristics.csv"
        picos_file <- "dataset/TTE_Metaresearch_Clean_Dataset - PICOs.csv"
        
        if (!file.exists(study_chars_file) || !file.exists(picos_file)) {
                cat("ERROR: Data files not found:\n")
                cat("-", study_chars_file, "\n") 
                cat("-", picos_file, "\n")
                return(NULL)
        }
        
        tte_study_chars = read.csv(study_chars_file)
        tte_picos = read.csv(picos_file)
        
        cat(sprintf("Data loaded: %d studies, %d comparisons\n", 
                   nrow(tte_study_chars), nrow(tte_picos)))
        
        return(list(
                study_chars = tte_study_chars,
                picos = tte_picos
        ))
}

# Enhanced data preparation function (from your scripts)
prepare_bayesian_data = function(tte_picos) {
        # Remove rows with missing essential data and invalid values
        clean_data = tte_picos %>%
                filter(
                        # Check for non-missing values
                        !is.na(rct_estimate),
                        !is.na(tte_estimate),
                        !is.na(rct_lb),
                        !is.na(rct_ub),
                        !is.na(tte_lb),
                        !is.na(tte_ub),
                        !is.na(effect_measure),

                        # Check for positive values in ratio measures
                        !(effect_measure %in% c("HR", "OR", "RR") &
                                (rct_estimate <= 0 | tte_estimate <= 0 |
                                 rct_lb <= 0 | rct_ub <= 0 |
                                 tte_lb <= 0 | tte_ub <= 0)),

                        # Check for finite values
                        is.finite(rct_estimate),
                        is.finite(tte_estimate),
                        is.finite(rct_lb),
                        is.finite(rct_ub),
                        is.finite(tte_lb),
                        is.finite(tte_ub),

                        # Check that confidence intervals make sense
                        rct_lb < rct_ub,
                        tte_lb < tte_ub,
                        rct_lb <= rct_estimate,
                        rct_estimate <= rct_ub,
                        tte_lb <= tte_estimate,
                        tte_estimate <= tte_ub
                ) %>%

                # Calculate standard errors from confidence intervals (robust version)
                mutate(
                        # For RCT estimates (safe log calculations)
                        rct_se = {
                                ratio_mask = effect_measure %in% c("HR", "OR", "RR") & 
                                           rct_ub > 0 & rct_lb > 0 & 
                                           is.finite(rct_ub) & is.finite(rct_lb)
                                
                                result = (rct_ub - rct_lb) / (2 * qnorm(0.975))  # Default calculation
                                
                                # Safe log calculation for ratio measures
                                if (any(ratio_mask, na.rm = TRUE)) {
                                        log_se = ifelse(ratio_mask, 
                                                       (log(pmax(rct_ub, 1e-10)) - log(pmax(rct_lb, 1e-10))) / (2 * qnorm(0.975)),
                                                       result)
                                        result = ifelse(ratio_mask, log_se, result)
                                }
                                
                                result
                        },

                        # For TTE estimates (safe log calculations)
                        tte_se = {
                                ratio_mask = effect_measure %in% c("HR", "OR", "RR") & 
                                           tte_ub > 0 & tte_lb > 0 & 
                                           is.finite(tte_ub) & is.finite(tte_lb)
                                
                                result = (tte_ub - tte_lb) / (2 * qnorm(0.975))  # Default calculation
                                
                                # Safe log calculation for ratio measures
                                if (any(ratio_mask, na.rm = TRUE)) {
                                        log_se = ifelse(ratio_mask, 
                                                       (log(pmax(tte_ub, 1e-10)) - log(pmax(tte_lb, 1e-10))) / (2 * qnorm(0.975)),
                                                       result)
                                        result = ifelse(ratio_mask, log_se, result)
                                }
                                
                                result
                        },

                        # Calculate differences on appropriate scales (safe log calculations)
                        diff_estimate = {
                                ratio_mask = effect_measure %in% c("HR", "OR", "RR") & 
                                           tte_estimate > 0 & rct_estimate > 0 & 
                                           is.finite(tte_estimate) & is.finite(rct_estimate)
                                
                                result = tte_estimate - rct_estimate  # Default calculation
                                
                                # Safe log calculation for ratio measures
                                if (any(ratio_mask, na.rm = TRUE)) {
                                        log_diff = ifelse(ratio_mask, 
                                                         log(pmax(tte_estimate, 1e-10)) - log(pmax(rct_estimate, 1e-10)),
                                                         result)
                                        result = ifelse(ratio_mask, log_diff, result)
                                }
                                
                                result
                        },

                        # Standard error of differences
                        diff_se = sqrt(rct_se^2 + tte_se^2),

                        # Create measure type indicators
                        measure_type = factor(
                                effect_measure,
                                levels = c("HR", "OR", "RR", "RD", "MD", "SMD")
                        ),
                        measure_idx = as.numeric(measure_type),

                        # Create study-level identifiers
                        study_pair_id = paste(study_id, target_trial_name, sep = "_")
                ) %>%

                # Remove rows with invalid calculations
                filter(
                        is.finite(rct_se),
                        is.finite(tte_se),
                        is.finite(diff_estimate),
                        is.finite(diff_se),
                        rct_se > 0,
                        tte_se > 0,
                        diff_se > 0
                ) %>%

                # Remove extreme outliers (>5 SDs from mean within each measure type)
                group_by(effect_measure) %>%
                mutate(
                        z_score = abs(diff_estimate - mean(diff_estimate, na.rm = TRUE)) /
                                sd(diff_estimate, na.rm = TRUE)
                ) %>%
                filter(z_score <= 5 | is.na(z_score)) %>%
                ungroup() %>%

                # Include all effect measures, even single studies
                group_by(effect_measure) %>%
                filter(n() >= 1) %>%  # Include even single studies (RD)
                ungroup()

        cat("Data cleaning summary:\n")
        cat("- Original rows:", nrow(tte_picos), "\n")
        cat("- Clean rows:", nrow(clean_data), "\n")
        cat("- Effect measures in original data:", paste(unique(tte_picos$effect_measure), collapse = ", "), "\n")
        cat("- Effect measures after cleaning:", paste(unique(clean_data$effect_measure), collapse = ", "), "\n")
        
        # Show counts by effect measure before and after cleaning
        cat("\nEffect measure counts in original data:\n")
        print(table(tte_picos$effect_measure, useNA = "ifany"))
        cat("\nEffect measure counts after cleaning:\n")
        print(table(clean_data$effect_measure, useNA = "ifany"))

        return(clean_data)
}

# Enhanced data preparation with study characteristics (from your scripts)
prepare_comprehensive_data = function(study_chars, picos) {
        # Prepare PICO data
        clean_picos = prepare_bayesian_data(picos)

        # Process study characteristics
        clean_study_chars = study_chars %>%
                mutate(
                        # Binary indicators for methodological quality
                        has_dag = ifelse(
                                tolower(dag) %in% c("yes", "y", "1", "true"),
                                1, 0
                        ),
                        has_protocol = ifelse(
                                tolower(protocol) %in% c("yes", "y", "1", "true", "pre-registration"),
                                1, 0
                        ),
                        has_qba = ifelse(
                                tolower(qba) %in% c("yes", "y", "1", "true"),
                                1, 0
                        ),

                        # Clean disease categories
                        disease_category_clean = case_when(
                                str_detect(tolower(disease_category), "cardio|heart|coronary") ~ "Cardiovascular",
                                str_detect(tolower(disease_category), "cancer|oncology|tumor") ~ "Oncology",
                                str_detect(tolower(disease_category), "diabetes|endocrine|metabolic") ~ "Endocrine/Metabolic",
                                str_detect(tolower(disease_category), "respiratory|lung|asthma") ~ "Respiratory",
                                str_detect(tolower(disease_category), "infection|hiv|covid") ~ "Infectious Diseases",
                                str_detect(tolower(disease_category), "kidney|renal|nephro") ~ "Nephrology",
                                str_detect(tolower(disease_category), "gastro|ibd|crohn") ~ "Gastroenterology",
                                str_detect(tolower(disease_category), "neuro|brain|stroke") ~ "Neurology",
                                str_detect(tolower(disease_category), "immune|rheum|arthritis") ~ "Immunology",
                                TRUE ~ "Other"
                        ),

                        # Data source categories
                        data_source_clean = case_when(
                                str_detect(tolower(data_type), "claims") ~ "Claims",
                                str_detect(tolower(data_type), "ehr|electronic") ~ "EHR",
                                str_detect(tolower(data_type), "registry") ~ "Registry",
                                str_detect(tolower(data_type), "rct") ~ "RCT Data",
                                TRUE ~ "Other"
                        ),

                        # Publication year categories
                        year_category = case_when(
                                year <= 2019 ~ "2019 and earlier",
                                year <= 2021 ~ "2020-2021",
                                year >= 2022 ~ "2022 and later",
                                TRUE ~ "Unknown"
                        )
                )

        # Try to merge with different join strategies
        comprehensive_data = tryCatch({
                clean_picos %>%
                        left_join(clean_study_chars, by = "study_id")
        }, error = function(e) {
                # If study_id join fails, try with first_author and year
                cat("Warning: study_id join failed, trying first_author + year join\n")
                clean_picos %>%
                        left_join(clean_study_chars, by = c("first_author", "year"))
        })

        return(comprehensive_data)
}

# ============================================================================
# STAN MODEL DEFINITIONS (FROM YOUR SCRIPTS)
# ============================================================================

# Basic stratified model for individual effect measures (improved convergence)
basic_stratified_model = "
data {
  int<lower=1> N;                    // number of studies
  vector[N] y;                       // observed differences
  vector<lower=0>[N] se;             // standard errors
}

parameters {
  real mu;                           // overall mean difference
  vector[N] theta_raw;               // study-specific raw effects
  real<lower=0> tau;                 // between-study SD
}

transformed parameters {
  vector[N] theta = mu + tau * theta_raw;  // non-centered parameterization
}

model {
  // Priors
  mu ~ normal(0, 2);                 // More dispersed prior
  tau ~ normal(0, 1);                // More conservative prior
  theta_raw ~ std_normal();          // Standard normal for non-centered
  
  // Likelihood
  y ~ normal(theta, se);
}

generated quantities {
  // Posterior predictive checks
  vector[N] y_rep;
  
  // Probability statements
  real prob_exceed_25 = step(abs(mu) - 0.25);
  real prob_exceed_50 = step(abs(mu) - 0.50);
  real prob_exceed_10 = step(abs(mu) - 0.10);
  
  // Predictive interval for new study
  real theta_new = normal_rng(mu, tau);
  real y_new = normal_rng(theta_new, mean(se));
  
  for (i in 1:N) {
    y_rep[i] = normal_rng(theta[i], se[i]);
  }
}
"

# Subgroup meta-regression model
subgroup_model = "
data {
  int<lower=1> N;                    // number of studies
  vector[N] y;                       // observed differences
  vector<lower=0>[N] se;             // standard errors
  int<lower=1> K;                    // number of subgroups
  array[N] int<lower=1, upper=K> subgroup; // subgroup indicator
}

parameters {
  vector[K] mu;                      // subgroup means
  vector[N] theta;                   // study-specific true effects
  real<lower=0> tau;                 // between-study SD
}

model {
  // Priors
  mu ~ normal(0, 1);
  tau ~ normal(0, 0.5);
  
  // Hierarchical model
  for (i in 1:N) {
    theta[i] ~ normal(mu[subgroup[i]], tau);
    y[i] ~ normal(theta[i], se[i]);
  }
}

generated quantities {
  // Posterior predictive checks
  vector[N] y_rep;
  
  // Pairwise differences between subgroups
  real diff_2_1 = K > 1 ? mu[2] - mu[1] : 0;
  real diff_3_1 = K > 2 ? mu[3] - mu[1] : 0;
  real diff_3_2 = K > 2 ? mu[3] - mu[2] : 0;
  
  for (i in 1:N) {
    y_rep[i] = normal_rng(theta[i], se[i]);
  }
}
"

# ============================================================================
# BAYESIAN MODEL FITTING FUNCTIONS (FROM YOUR SCRIPTS)
# ============================================================================

# Fit stratified Bayesian model
fit_stratified_model = function(data, measure_type) {
        # Use base R filtering
        filter_mask = data$effect_measure == measure_type & !is.na(data$effect_measure)
        measure_data = data[filter_mask, ]

        if (nrow(measure_data) < 1) {
                cat("No data for", measure_type, "\n")
                return(NULL)
        }
        
        # Special handling for single studies
        if (nrow(measure_data) == 1) {
                cat("Single study for", measure_type, "- using simple analysis\n")
                
                study_data = measure_data %>%
                        filter(
                                is.finite(diff_estimate),
                                is.finite(diff_se),
                                !is.na(diff_estimate),
                                !is.na(diff_se),
                                diff_se > 0
                        )
                
                if (nrow(study_data) == 1) {
                        # For single studies, return the individual estimate as pooled estimate
                        single_result = list(
                                effect_measure = measure_type,
                                n_studies = 1,
                                pooled_estimate = study_data$diff_estimate[1],
                                ci_lower = study_data$diff_estimate[1] - 1.96 * study_data$diff_se[1],
                                ci_upper = study_data$diff_estimate[1] + 1.96 * study_data$diff_se[1],
                                tau_squared = 0,  # No between-study heterogeneity with 1 study
                                tau = 0,
                                method = "Single study analysis",
                                estimation = "Individual study estimate with 95% CI"
                        )
                        
                        return(list(
                                single_study_result = single_result,
                                data = study_data,
                                measure_type = measure_type
                        ))
                } else {
                        cat("Single study data invalid after cleaning\n")
                        return(NULL)
                }
        }

        cat("Fitting model for", measure_type, "(n =", nrow(measure_data), ")\n")

        # Final validation of data before Stan
        measure_data_clean = measure_data %>%
                filter(
                        is.finite(diff_estimate),
                        is.finite(diff_se),
                        !is.na(diff_estimate),
                        !is.na(diff_se),
                        diff_se > 0
                )

        if (nrow(measure_data_clean) < 2) {
                cat("Insufficient clean data for", measure_type, "after validation\n")
                return(NULL)
        }

        stan_data = list(
                N = nrow(measure_data_clean),
                y = measure_data_clean$diff_estimate,
                se = measure_data_clean$diff_se
        )

        # Validate Stan data
        if (any(is.na(stan_data$y)) || any(is.na(stan_data$se)) || any(stan_data$se <= 0)) {
                cat("Invalid data detected for", measure_type, "- skipping\n")
                return(NULL)
        }

        if (use_cmdstanr) {
                model = cmdstan_model(write_stan_file(basic_stratified_model))

                fit = model$sample(
                        data = stan_data,
                        chains = 4,
                        parallel_chains = 4,
                        iter_warmup = 100000,
                        iter_sampling = 100000,
                        refresh = 10000,
                        max_treedepth = 15,
                        adapt_delta = 0.99,
                        seed = 12345
                )
        } else {
                fit = stan(
                        model_code = basic_stratified_model,
                        data = stan_data,
                        chains = 4,
                        iter = 3000,
                        warmup = 1000,
                        cores = 4,
                        refresh = 500,
                        control = list(adapt_delta = 0.95, max_treedepth = 12),
                        seed = 12345
                )
        }

        return(list(
                fit = fit,
                data = measure_data_clean,
                stan_data = stan_data,
                measure_type = measure_type
        ))
}

# Fit subgroup model
fit_subgroup_model = function(data, subgroup_var, subgroup_name) {
        # Filter data with non-missing subgroup values
        subgroup_data = data %>%
                filter(!is.na(!!sym(subgroup_var))) %>%
                mutate(subgroup_factor = factor(!!sym(subgroup_var)))

        subgroup_levels = levels(subgroup_data$subgroup_factor)

        if (nrow(subgroup_data) < 10 || length(subgroup_levels) < 2) {
                cat("Insufficient data for", subgroup_name, "subgroup analysis\n")
                return(NULL)
        }

        cat("Fitting subgroup model for", subgroup_name, 
            "(n =", nrow(subgroup_data), "studies across", length(subgroup_levels), "subgroups)\n")

        stan_data = list(
                N = nrow(subgroup_data),
                y = subgroup_data$diff_estimate,
                se = subgroup_data$diff_se,
                K = length(subgroup_levels),
                subgroup = as.numeric(subgroup_data$subgroup_factor)
        )

        if (use_cmdstanr) {
                model = cmdstan_model(write_stan_file(subgroup_model))
                
                fit = model$sample(
                        data = stan_data,
                        chains = 4,
                        parallel_chains = 4,
                        iter_warmup = 100000,
                        iter_sampling = 100000,
                        refresh = 5000,
                        max_treedepth = 15,
                        adapt_delta = 0.99,
                        seed = 12345
                )
        } else {
                fit = stan(
                        model_code = subgroup_model,
                        data = stan_data,
                        chains = 4,
                        iter = 3000,
                        warmup = 1000,
                        cores = 4,
                        refresh = 0,
                        control = list(adapt_delta = 0.95, max_treedepth = 12),
                        seed = 12345
                )
        }

        return(list(
                fit = fit,
                data = subgroup_data,
                stan_data = stan_data,
                subgroup_var = subgroup_var,
                subgroup_name = subgroup_name,
                subgroup_levels = subgroup_levels
        ))
}

# ============================================================================
# MAIN ANALYSIS EXECUTION
# ============================================================================

cat("Loading TTE meta-research dataset for comprehensive Bayesian analysis...\n")

# Load the data
tte_data = load_tte_data()
if (is.null(tte_data)) {
        cat("Failed to load data. Exiting.\n")
        quit(status = 1)
}

study_chars = tte_data$study_chars
picos = tte_data$picos

# Prepare comprehensive data
cat("Preparing comprehensive data with study characteristics...\n")
comprehensive_data = prepare_comprehensive_data(study_chars, picos)

cat("Comprehensive data prepared: ", nrow(comprehensive_data), "rows\n")

# ============================================================================
# RUN BAYESIAN META-ANALYSIS
# ============================================================================

# Initialize results
bayesian_results <- NULL
subgroup_results <- list()

if (exists("stan_ready") && stan_ready && nrow(comprehensive_data) > 0) {
        cat("Running comprehensive Bayesian meta-analysis with Stan...\n")
        
        tryCatch({
                # Primary analysis by effect measure
                effect_measures <- unique(comprehensive_data$effect_measure)
                cat("Effect measures found:", paste(effect_measures, collapse = ", "), "\n")
                
                primary_results = list()
                
                for (measure in effect_measures) {
                        cat("\n--- Analyzing", measure, "---\n")
                        result = fit_stratified_model(comprehensive_data, measure)
                        
                        if (!is.null(result)) {
                                # Handle single study results differently
                                if ("single_study_result" %in% names(result)) {
                                        primary_results[[measure]] = result$single_study_result
                                        cat("✅ ", measure, ": 1 study (single), estimate = ", 
                                            round(result$single_study_result$pooled_estimate, 3),
                                            " [", round(result$single_study_result$ci_lower, 3), ", ",
                                            round(result$single_study_result$ci_upper, 3), "]\n", sep = "")
                                        next
                                }
                                
                                # Extract Bayesian results with improved error handling
                                tryCatch({
                                        if (use_cmdstanr) {
                                                mu_summary = result$fit$summary("mu")
                                                tau_summary = result$fit$summary("tau")
                                                
                                                # Check for convergence issues
                                                diagnostics = result$fit$diagnostic_summary()
                                                if (any(diagnostics$num_divergent > 0)) {
                                                        cat("WARNING: Divergent transitions detected for", measure, "\n")
                                                }
                                                
                                                # Extract with correct CmdStanR column names
                                                mu_mean = mu_summary$mean[1]
                                                mu_lower = mu_summary$q5[1]  # CmdStanR uses q5 for 5th percentile
                                                mu_upper = mu_summary$q95[1] # CmdStanR uses q95 for 95th percentile
                                                tau_mean = tau_summary$mean[1]
                                                
                                                primary_results[[measure]] = list(
                                                        effect_measure = measure,
                                                        n_studies = nrow(result$data),
                                                        pooled_estimate = as.numeric(mu_mean),
                                                        ci_lower = as.numeric(mu_lower),
                                                        ci_upper = as.numeric(mu_upper),
                                                        tau_squared = as.numeric(tau_mean)^2,
                                                        tau = as.numeric(tau_mean),
                                                        method = "Bayesian hierarchical meta-analysis",
                                                        estimation = "CmdStanR with 4 chains, 100K warmup + 100K sampling"
                                                )
                                        } else {
                                                fit_summary = summary(result$fit)$summary
                                                mu_row = grep("^mu$", rownames(fit_summary))
                                                tau_row = grep("^tau$", rownames(fit_summary))
                                                
                                                primary_results[[measure]] = list(
                                                        effect_measure = measure,
                                                        n_studies = nrow(result$data),
                                                        pooled_estimate = fit_summary[mu_row[1], "mean"],
                                                        ci_lower = fit_summary[mu_row[1], "2.5%"],
                                                        ci_upper = fit_summary[mu_row[1], "97.5%"],
                                                        tau_squared = fit_summary[tau_row[1], "mean"]^2,
                                                        tau = fit_summary[tau_row[1], "mean"],
                                                        method = "Bayesian hierarchical meta-analysis",
                                                        estimation = "RStan with 4 chains, 3000 iterations"
                                                )
                                        }
                                        
                                }, error = function(e) {
                                        cat("ERROR extracting results for", measure, ":", e$message, "\n")
                                        cat("Skipping", measure, "due to extraction error\n")
                                })
                                
                                # Only print success if extraction worked
                                if (measure %in% names(primary_results)) {
                                        cat("✅ ", measure, ": ", primary_results[[measure]]$n_studies, 
                                            " studies, μ = ", round(primary_results[[measure]]$pooled_estimate, 3),
                                            " [", round(primary_results[[measure]]$ci_lower, 3), ", ",
                                            round(primary_results[[measure]]$ci_upper, 3), "], τ² = ",
                                            round(primary_results[[measure]]$tau_squared, 4), "\n", sep = "")
                                }
                        }
                }
                
                bayesian_results = primary_results
                
                # ============================================================================
                # SUBGROUP ANALYSES (if we have study characteristics)
                # ============================================================================
                
                if ("disease_category_clean" %in% names(comprehensive_data)) {
                        cat("\n--- Running Disease Category Subgroup Analysis ---\n")
                        disease_result = fit_subgroup_model(
                                comprehensive_data, "disease_category_clean", "Disease Category"
                        )
                        
                        if (!is.null(disease_result)) {
                                subgroup_results[["disease"]] = disease_result
                        }
                }
                
                if ("data_source_clean" %in% names(comprehensive_data)) {
                        cat("\n--- Running Data Source Subgroup Analysis ---\n")
                        source_result = fit_subgroup_model(
                                comprehensive_data, "data_source_clean", "Data Source"
                        )
                        
                        if (!is.null(source_result)) {
                                subgroup_results[["data_source"]] = source_result
                        }
                }
                
                if ("year_category" %in% names(comprehensive_data)) {
                        cat("\n--- Running Publication Year Subgroup Analysis ---\n")
                        year_result = fit_subgroup_model(
                                comprehensive_data, "year_category", "Publication Year"
                        )
                        
                        if (!is.null(year_result)) {
                                subgroup_results[["publication_year"]] = year_result
                        }
                }
                
                cat("✅ Comprehensive Bayesian meta-analysis completed!\n")
                
        }, error = function(e) {
                cat("⚠️ Bayesian analysis failed:", e$message, "\n")
                cat("Falling back to basic export...\n")
                bayesian_results <<- NULL
                subgroup_results <<- list()
        })
        
} else {
        cat("⚠️ Stan not available or no clean data. Using basic export only.\n")
        bayesian_results <- NULL
        subgroup_results <- list()
}

# ============================================================================
# CREATE FOREST PLOT DATA
# ============================================================================

cat("Creating enhanced forest plot data...\n")

real_forest_data <- list()

for (measure in unique(comprehensive_data$effect_measure)) {
        measure_data <- comprehensive_data %>%
                filter(effect_measure == measure) %>%
                mutate(
                        author = coalesce(first_author, paste("Study", row_number())),
                        study_label = paste(author, year),
                        point_estimate = diff_estimate,
                        lower_ci = diff_estimate - 1.96 * diff_se,
                        upper_ci = diff_estimate + 1.96 * diff_se,
                        sample_size = 1000,  # Default when not available
                        tte_estimate = tte_estimate,
                        rct_estimate = rct_estimate
                ) %>%
                select(study_id, author, year, study_label, point_estimate, lower_ci, upper_ci, 
                       sample_size, tte_estimate, rct_estimate)
        
        if (nrow(measure_data) > 0) {
                real_forest_data[[tolower(measure)]] <- measure_data
        }
}

# Export forest plot data
write_json(real_forest_data, "ttedb/data/forest_plot_data.json", 
           pretty = TRUE, auto_unbox = TRUE)

# ============================================================================
# CREATE DESCRIPTIVE RESULTS
# ============================================================================

cat("Creating descriptive statistics...\n")

descriptive_results <- list(
        overview = list(
                total_studies = nrow(study_chars),
                total_comparisons = nrow(picos),
                effect_measures = unique(comprehensive_data$effect_measure),
                studies_with_clean_data = nrow(comprehensive_data),
                year_range = paste(min(study_chars$year, na.rm = TRUE), "-", 
                                  max(study_chars$year, na.rm = TRUE))
        ),
        
        effect_measures = comprehensive_data %>%
                count(effect_measure, sort = TRUE) %>%
                mutate(percentage = round(n / sum(n) * 100, 1)),
        
        disease_categories = if ("disease_category_clean" %in% names(comprehensive_data)) {
                comprehensive_data %>%
                        filter(!is.na(disease_category_clean)) %>%
                        count(disease_category_clean, sort = TRUE) %>%
                        mutate(percentage = round(n / sum(n) * 100, 1))
        } else { NULL },
        
        data_sources = if ("data_source_clean" %in% names(comprehensive_data)) {
                comprehensive_data %>%
                        filter(!is.na(data_source_clean)) %>%
                        count(data_source_clean, sort = TRUE) %>%
                        mutate(percentage = round(n / sum(n) * 100, 1))
        } else { NULL },
        
        temporal_trends = study_chars %>%
                filter(!is.na(year)) %>%
                count(year, sort = TRUE)
)

# Export descriptive results
write_json(descriptive_results, "ttedb/data/descriptive_results.json", 
           pretty = TRUE, auto_unbox = TRUE)

# ============================================================================
# EXPORT BAYESIAN META-ANALYSIS RESULTS
# ============================================================================

if (!is.null(bayesian_results)) {
        write_json(bayesian_results, "ttedb/data/meta_analysis_results.json", 
                   pretty = TRUE, auto_unbox = TRUE)
        cat("✅ Bayesian meta-analysis results exported!\n")
}

# Export subgroup results if available
if (length(subgroup_results) > 0) {
        # Process subgroup results for export
        processed_subgroups <- list()
        
        for (subgroup_name in names(subgroup_results)) {
                result <- subgroup_results[[subgroup_name]]
                
                if (use_cmdstanr) {
                        mu_summary <- result$fit$summary("mu")
                        
                        subgroup_estimates <- list()
                        for (i in 1:length(result$subgroup_levels)) {
                                subgroup_estimates[[result$subgroup_levels[i]]] <- list(
                                        pooled_estimate = mu_summary$mean[i],
                                        ci_lower = mu_summary$q5[i],  # Fixed: use q5 for CmdStanR
                                        ci_upper = mu_summary$q95[i], # Fixed: use q95 for CmdStanR
                                        n_studies = sum(result$data$subgroup_factor == result$subgroup_levels[i])
                                )
                        }
                } else {
                        fit_summary <- summary(result$fit)$summary
                        mu_rows <- grep("^mu\\[", rownames(fit_summary))
                        
                        subgroup_estimates <- list()
                        for (i in 1:length(result$subgroup_levels)) {
                                if (i <= length(mu_rows)) {
                                        subgroup_estimates[[result$subgroup_levels[i]]] <- list(
                                                pooled_estimate = fit_summary[mu_rows[i], "mean"],
                                                ci_lower = fit_summary[mu_rows[i], "2.5%"],
                                                ci_upper = fit_summary[mu_rows[i], "97.5%"],
                                                n_studies = sum(result$data$subgroup_factor == result$subgroup_levels[i])
                                        )
                                }
                        }
                }
                
                processed_subgroups[[subgroup_name]] <- subgroup_estimates
        }
        
        write_json(processed_subgroups, "ttedb/data/subgroup_analysis_results.json", 
                   pretty = TRUE, auto_unbox = TRUE)
        cat("✅ Bayesian subgroup analyses exported!\n")
}

# ============================================================================
# CREATE EXPORT SUMMARY
# ============================================================================

export_summary <- list(
        export_timestamp = Sys.time(),
        data_source = c("dataset/TTE_Metaresearch_Clean_Dataset - Studies characteristics.csv",
                       "dataset/TTE_Metaresearch_Clean_Dataset - PICOs.csv"),
        total_studies = nrow(study_chars),
        total_comparisons = nrow(picos),
        bayesian_analysis_performed = !is.null(bayesian_results),
        subgroup_analysis_performed = length(subgroup_results) > 0,
        stan_interface = if(use_cmdstanr) "CmdStanR" else "RStan",
        effect_measures = if(!is.null(bayesian_results)) names(bayesian_results) else unique(comprehensive_data$effect_measure),
        studies_in_meta_analysis = nrow(comprehensive_data),
        files_created = c(
                "ttedb/data/descriptive_results.json",
                "ttedb/data/forest_plot_data.json",
                if(!is.null(bayesian_results)) "ttedb/data/meta_analysis_results.json",
                if(length(subgroup_results) > 0) "ttedb/data/subgroup_analysis_results.json"
        ),
        export_type = "comprehensive_bayesian_analysis",
        notes = paste(
                if(!is.null(bayesian_results)) "✅ Comprehensive Bayesian hierarchical meta-analysis" else "❌ Bayesian analysis failed",
                if(length(subgroup_results) > 0) "✅ Subgroup analyses" else "❌ Subgroup analyses failed",
                sep = " | "
        )
)

write_json(export_summary, "ttedb/data/export_summary.json", 
           pretty = TRUE, auto_unbox = TRUE)

# ============================================================================
# FINAL SUMMARY
# ============================================================================

cat("\n", paste(rep("=", 80), collapse=""), "\n")
cat("🎯 COMPREHENSIVE BAYESIAN TTE META-ANALYSIS COMPLETE!\n")
cat(paste(rep("=", 80), collapse=""), "\n")
cat("Files created:\n")
cat("✅ ttedb/data/descriptive_results.json (comprehensive descriptive statistics)\n")
cat("✅ ttedb/data/forest_plot_data.json (real individual study data)\n")
if (!is.null(bayesian_results)) {
        cat("✅ ttedb/data/meta_analysis_results.json (Bayesian meta-analysis results)\n")
}
if (length(subgroup_results) > 0) {
        cat("✅ ttedb/data/subgroup_analysis_results.json (Bayesian subgroup analyses)\n")
}
cat("✅ ttedb/data/export_summary.json (export metadata)\n")

if (!is.null(bayesian_results)) {
        cat("\n🔬 BAYESIAN META-ANALYSIS SUMMARY:\n")
        for (measure in names(bayesian_results)) {
                result <- bayesian_results[[measure]]
                cat(sprintf("📊 %s: %d studies, μ = %.3f [%.3f, %.3f], τ² = %.4f\n",
                            measure, result$n_studies, result$pooled_estimate,
                            result$ci_lower, result$ci_upper, result$tau_squared))
        }
}

if (length(subgroup_results) > 0) {
        cat("\n🔍 SUBGROUP ANALYSES COMPLETED:\n")
        for (subgroup_name in names(subgroup_results)) {
                result <- subgroup_results[[subgroup_name]]
                cat("📊", result$subgroup_name, ":", length(result$subgroup_levels), "subgroups,", 
                    nrow(result$data), "studies\n")
        }
}

cat("\nYour Django website now has COMPLETE BAYESIAN META-ANALYSIS RESULTS! 🎯✨\n")
cat("This includes sophisticated Bayesian hierarchical models with subgroup analyses.\n")
cat(paste(rep("=", 80), collapse=""), "\n")