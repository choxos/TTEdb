# **Comparative Efficacy Estimates Concordance Between Target Trial Emulations and Their Corresponding Target Trials: Protocol for a Living Meta-Epidemiological Study**

Ahmad Sofi-Mahmudi1, ORCiD: 0000-0001-6829-0823, [a.sofimahmudi@gmail.com](mailto:a.sofimahmudi@gmail.com).

Kristian Thorlund1, ORCiD: 0000-0001-5848-3111, [thorluk@mcmaster.ca](mailto:thorluk@mcmaster.ca).

Louis Dron2, ORCiD: 0000-0002-3276-3948, [louisdron@gmail.com](mailto:louisdron@gmail.com).

Paul Arora3,4, ORCiD: 0000-0001-6617-3631, [paul.arora@utoronto.ca](mailto:paul.arora@utoronto.ca).

**1** Department of Health Research Methods, Evidence and Impact, McMaster University, Hamilton, Ontario, L8S 4L8, Canada.

**2** Cascade Outcomes Research, Vancouver, British Columbia, Canada.

**3** Division of Epidemiology, Dalla Lana School of Public Health, University of Toronto, Toronto, Ontario, M5T 3M7, Canada.

**4** Inka Health, Schwartz Reisman Innovation Campus, University of Toronto, Toronto, Ontario, M5G 0C6, Canada.

**Corresponding author:** ; **Address**: ; **Email**: .

 

**Conflict of interest disclosure:** ASM is an employee of Cytel Canada Health Inc.

**Funding disclosure:** This study did not receive any funding. 

**Data and code availability:** All the data and codes will be available from our Open Science Framework (OSF) repository at [https://osf.io/yzgkj/](https://osf.io/yzgkj/).

# 

# **Abstract**

**Background:** While randomized controlled trials (RCTs) remain the gold standard for establishing causality in clinical research, they face limitations, including high costs and limited real-world generalizability. Target trial emulation (TTE) has emerged as a methodological framework that uses observational data to emulate key components of randomized trials. Despite the growing adoption of TTEs and successful applications across various therapeutic areas, there has been limited systematic evaluation of how well TTE results align with their corresponding target trials.

**Objective:** This meta-epidemiological study aims to assess the consistency between effect estimates from TTEs and their corresponding target trials, and to identify methodological factors associated with better concordance. Secondary objectives include evaluating the impact of study characteristics, examining patterns across different disease areas and interventions, and assessing the relationship between methodological quality indicators and estimate consistency.

**Methods:** We will conduct a comprehensive systematic search across Embase and MEDLINE databases, with living updates via PubMed’s E-utilities application programming interface. Studies will be included if they explicitly utilize target trial emulation methodology, compare their results with a previously conducted RCT, present original research, and provide quantifiable effect estimates. We will extract publication metadata, research transparency indicators, study context information, methodological approaches, sample characteristics, and target trial information. The primary analysis will evaluate differences between TTE and RCT effect estimates using ratio measures analysis for ratio measures (hazard ratios, odds ratios, and risk ratios) and additive measures analysis for additive measures (risk differences, mean differences, and standardized mean differences). We will use random-effects meta-analysis, stratification by effect measure type, and forest plot analysis to examine patterns of estimate concordance. Publication bias will be assessed through funnel plot analysis and tests for asymmetry.

**Implications:** This study will provide crucial insights into the validity and reliability of target trial emulation as a methodological approach. Findings will help establish evidence-based recommendations for conducting TTEs and identify conditions under which TTEs most reliably approximate RCT results. By systematically evaluating concordance between TTEs and RCTs across different clinical domains and methodological approaches, this study will strengthen the foundation for using real-world evidence in clinical decision-making when randomized trials are impractical or unethical.

***Keywords:*** Target trial emulation; Randomized controlled trials; Observational studies; Causal inference; Meta-epidemiology; Evidence synthesis

# 

# **Introduction**

Randomized controlled trials (RCTs) have long been considered the gold standard for establishing causal relationships in clinical research [(Hernan & Robins, 2025; McKenzie et al., 2019\)](https://www.zotero.org/google-docs/?aVyaqr). RCTs minimize selection bias through the randomization of study participants to treatment and comparator groups when allocation is properly concealed [(Schulz et al., 1995; Wood et al., 2008\)](https://www.zotero.org/google-docs/?eaWkGu). By assigning participants to study arms prospectively before outcomes occur, RCTs avoid the selection bias that can affect retrospective studies when participant inclusion depends on intervention-related outcomes, such as survivor bias [(Glesby & Hoover, 1996\)](https://www.zotero.org/google-docs/?yzs90x). Proper randomization creates study groups that are comparable on both measured and unmeasured baseline characteristics, effectively eliminating confounding bias [(Peto et al., 1976\)](https://www.zotero.org/google-docs/?uVD05M). However, RCTs face numerous challenges, including high costs [(Speich et al., 2018\)](https://www.zotero.org/google-docs/?WpTglD), lengthy implementation times, and limited generalizability to real-world settings [(Bothwell et al., 2016; Frieden, 2017\)](https://www.zotero.org/google-docs/?nVc8Kr). Target trial emulation (TTE), introduced by Hernán and Robins, has emerged as a powerful methodological framework that aims to bridge this gap by using observational data to emulate the key components of randomized trials [(Hernán & Robins, 2016; Hernán et al., 2016\)](https://www.zotero.org/google-docs/?3zTHdf).

The TTE approach has gained considerable attention in recent years, particularly due to its structured framework for addressing common sources of bias in observational studies [(Lodi et al., 2019\)](https://www.zotero.org/google-docs/?bTjCHT). This methodology requires explicit specification of the protocol elements that would have been used in a target trial, including eligibility criteria, treatment strategies, follow-up period, outcome definitions, and analysis plan [(Danaei et al., 2018\)](https://www.zotero.org/google-docs/?LCsJRK). By carefully emulating these components using observational data, researchers aim to approximate the causal inference capabilities of RCTs while leveraging the advantages of real-world evidence [(Franklin & Schneeweiss, 2017; Labrecque & Swanson, 2017\)](https://www.zotero.org/google-docs/?Qc4PIZ).

Multiple methodological and practical factors have contributed to the rising adoption of TTEs. The exponential growth in available healthcare databases and improved computational capabilities have made large-scale observational analyses more feasible [(Cowie et al., 2017; Hripcsak et al., 2015\)](https://www.zotero.org/google-docs/?mifOd1). Additionally, ethical considerations, practical constraints, and the need for rapid evidence generation in certain clinical scenarios have highlighted the importance of robust observational study designs [(Sherman et al., 2016\)](https://www.zotero.org/google-docs/?xhL0nj). The COVID-19 pandemic further emphasized this need, as TTEs provided valuable insights when traditional RCTs were challenging to conduct [(Bauchner & Fontanarosa, 2020\)](https://www.zotero.org/google-docs/?BcKImc).

However, despite the methodological rigor of TTE approaches, fundamental questions remain about their validity and reliability. While several studies have demonstrated successful applications of TTEs in various therapeutic areas [(Dickerman et al., 2019; García-Albéniz et al., 2017\)](https://www.zotero.org/google-docs/?UfUUqv), systematic evaluation of how well TTE results align with their corresponding target trials has been limited. The landmark RCT-DUPLICATE initiative provided the first comprehensive assessment by emulating 32 completed randomized trials using observational data, demonstrating an overall Pearson correlation of 0.82 between trial and emulation results, with higher concordance (r=0.93) achieved when trial designs could be closely emulated and weaker agreement (r=0.53) when substantial design differences existed [(Wang et al., 2023\)](https://www.zotero.org/google-docs/?dTJYwL). While RCT-DUPLICATE established proof-of-concept for TTE methodology under optimal conditions, important questions remain about the broader applicability of these findings across diverse clinical contexts. Previous meta-epidemiological studies have examined the relationship between observational studies and RCTs more broadly [(Hemkens et al., 2016; Toews et al., 2024\)](https://www.zotero.org/google-docs/?sOtOmM), but none have specifically focused on the unique methodological aspects of TTEs. Additionally, while the TARGET guideline for conducting and reporting TTEs is under development [(Hansford et al., 2023\)](https://www.zotero.org/google-docs/?vg7zPo), there remains limited evidence regarding which specific methodological choices in TTE design produce results most consistent with RCTs and how study characteristics influence estimate concordance [(Gomes et al., 2024; Hernán, 2018\)](https://www.zotero.org/google-docs/?xHZYi4).

This meta-epidemiological study aims to address these knowledge gaps by systematically evaluating the consistency between effect estimates from TTEs and their corresponding target trials. By analyzing a comprehensive dataset of published TTEs and their target RCTs, we seek to identify factors associated with better concordance and provide evidence-based recommendations for future TTE studies.

# **Objectives**

## **Primary Objective**

To assess the consistency between effect estimates derived from TTEs and their corresponding target RCTs.

## **Secondary Objectives**

1. To identify study-level characteristics and methodological factors associated with concordance between TTE and RCT effect estimates;  
2. To examine patterns of estimate consistency across different disease areas, intervention types, and outcome categories;  
3. To evaluate the relationship between methodological quality indicators and the degree of agreement between TTE and RCT results; and,  
4. To characterize the distribution of effect estimate differences and assess factors associated with directional discordance between TTEs and target trials.

# **Methods**

## **Study Design**

This is a meta-epidemiological study comparing effect estimates from published TTEs with their corresponding original RCTs.

## **Data Sources and Search Strategy**

### ***Initial Search***

The initial systematic search was conducted on December 31, 2024, utilizing Embase and Ovid MEDLINE databases. The search strategy employed the following terms: "trial and emulat\*", "target trial\*", "pseudotrial\*", and "emulated trial\*". After removing duplicates, 2,606 unique records were identified. The complete search strategy and results are documented in Appendix 1\.

### ***Living Update Methodology***

To maintain the currency of evidence, a living update framework will be implemented. Subsequent updates will utilize the PubMed database exclusively via the Entrez Programming Utilities (E-utilities) application programming interface (API). This approach was selected for its reproducibility, programmatic efficiency, and adherence to the NCBI’s guidelines for automated queries.

The living update search will maintain consistency with the original search terms while restricting results to publications after December 31, 2024\. The implementation utilizes Python with the *Biopython* package to access the E-utilities API, following established protocols for programmatic database access. Search parameters include:

* Database: PubMed  
* Search terms: "trial and emulat\*" OR "target trial\*" OR "pseudotrial\*" OR "emulated trial\*"  
* Date restriction: Publications after December 31, 2024  
* Result sorting: By relevance  
* Maximum retrievals per query: 100 records

### ***Abstract Screening Methodology***

Retrieved abstracts undergo an automated screening process utilizing the Google Gemini Pro (latest version at the time) large language model API. The screening algorithm evaluates each abstract against the following structured criteria:

* Confirmation of TTE methodology application;  
* Identification of comparison status with RCT(s);  
* Extraction of RCT identifiers where applicable;  
* Documentation of population, intervention, comparison, and outcome (PICO) elements;  
* Extraction of primary numerical results.

The screening process generates a standardized CSV output with the following data fields:

* is\_tte: Binary classification of TTE methodology presence;  
* is\_compared: Binary classification of RCT comparison presence;  
* rct\_name: Identification of compared RCT when applicable;  
* population: Study population characteristics;  
* intervention: Intervention protocol;  
* comparison: Comparator protocol;  
* outcome: Primary and secondary outcome measures;  
* answer: Quantitative results for each outcome.

Abstracts classified positively for TTE methodology undergo subsequent full-text review. For the full-text screening, after downloading the PDFs, Google Gemini will be used as the first reviewer with the same criteria as above.

### ***Eligibility Criteria***

Studies are included if they meet the following criteria:

* Explicitly utilize TTE methodology;  
* Compared their results with a previously conducted RCT;  
* Present original research (not methodological discussions, commentaries, or reviews);  
* Provide quantifiable effect estimates.

## **Variables Collected**

Our dataset encompasses a comprehensive set of variables extracted from published TTEs and their corresponding target RCTs. The variables are organized into two primary datasets: (1) study characteristics (Appendix 2\) and (2) PICO elements and effect estimates (Appendix 3).

The study characteristics variables (Appendix 2\) document key attributes of the included studies across six domains: publication metadata, research transparency, study context, methodological approach, sample characteristics, and target trial information. These variables facilitate the assessment of publication patterns, institutional affiliations, methodological rigor, and research transparency practices. The data capture both general publication information (e.g., author, year, DOI) and methodological details specific to TTE studies, including missing data handling methods, matching approaches, analytical techniques, and directed acyclic graph (DAG) usage.

The PICO elements and effect estimates variables (Appendix 3\) provide detailed information about the comparative findings between TTEs and their reference RCTs. These variables include the population, intervention, comparison, and outcome specifications from both the TTE and RCT studies, along with their respective effect estimates, confidence intervals, and sample sizes. The dataset also includes calculated metrics that quantify the concordance between TTE and RCT effect estimates, enabling systematic assessment of the agreement between these methodologies. All effect measures are documented with their point estimates and confidence intervals to enable comprehensive meta-analytical approaches.

## **Statistical Analysis Plan**

Our analytical approach encompasses multiple complementary methods to comprehensively evaluate concordance between TTE and RCT effect estimates, identify predictors of agreement, and characterize patterns of discordance across studies. All analyses will be conducted using R statistical software [(R Core Team, 2025\)](https://www.zotero.org/google-docs/?mbPIRF), with complete code provided in Appendix 4 to ensure reproducibility.

### ***Descriptive Analysis***

Our descriptive analysis will characterize the TTE literature across four key domains to inform subsequent concordance analyses and identify potential sources of heterogeneity.

#### **Publication Patterns and Methodological Evolution**

We will examine temporal trends in TTE adoption using frequency histograms by publication year since 2016\. Geographic distribution will be assessed through frequency tables of research institutions and data sources by region. Methodological evolution will be tracked using line plots showing temporal trends in DAG usage, quantitative bias analysis implementation, and transparency metrics.

#### **Study Characteristics and Methodological Approaches**

TTEs will be characterized using frequency tables and proportions with 95% confidence intervals (CIs, Wilson score method) for disease categories, intervention types, outcome measures, and data sources. Methodological approaches, including missing data handling, matching methods, statistical techniques, and estimand types, will be summarized in comprehensive tables. Covariate distribution will be visualized using box plots stratified by disease category and data source. For studies with multiple TTEs targeting the same RCT, we will select the primary analysis as specified by the authors.

#### **Target Trial Characteristics and TTE-RCT Relationships**

Target trial characteristics will be described using summary statistics and frequency tables for sample sizes, publication dates, and study settings. Temporal lag between RCT publication and TTE studies will be visualized using histograms and summary statistics. Sample size relationships will be examined using scatter plots on log-scale with correlation analysis.

#### **Transparency and Research Practices**

Research transparency will be evaluated using frequency tables for protocol registration rates, data sharing practices, code availability, funding disclosures, and conflict of interest declarations. Temporal trends will be visualized using stacked bar charts. Geographic and temporal patterns will be compared using chi-square tests and trend analysis.

#### **Statistical Considerations**

All analyses will account for potential clustering by research institution using the intracluster correlation assessment. Missing data patterns will be described using frequency tables, with complete case analysis for descriptive statistics. Variables showing substantial variation will be retained as potential predictors in concordance analyses.

### ***Primary Analysis***

The primary analysis will systematically evaluate differences between effect estimates derived from TTEs and their target RCTs using a stratified Bayesian approach, recognizing the fundamental differences between effect measure types. This analysis consists of two components: (1) stratified Bayesian meta-analysis by effect measure type (primary), and (2) detection of systematic patterns in estimate differences.

#### **Effect Estimate Pooling and Comparison**

Given the diversity of effect measures reported across studies (hazard ratios \[HRs\], odds ratios \[ORs\], risk ratios \[RRs\], risk differences \[RDs\], mean differences \[MDs\], and standardized mean differences \[SMDs\]), and their distinct statistical properties and clinical interpretations, we will conduct the primary analysis stratified by effect measure type. Ratio measures (HRs, ORs, RRs) have multiplicative properties and asymmetric sampling distributions requiring logarithmic transformation, while additive measures (RDs, MDs, SMDs) have symmetric distributions analyzed on their original scales. Furthermore, the methodological challenges in TTE implementation vary substantially across measure types: time-to-event outcomes face immortal time bias and censoring issues, binary outcomes encounter rare event and study design challenges, and continuous outcomes involve missing data and measurement considerations. This stratified approach ensures statistically appropriate analysis while providing clinically interpretable, measure-specific evidence about TTE performance.

#### **Ratio Measures Analysis**

For ratio measures (HRs, ORs, RRs), analysis will be conducted on the logarithmic scale to address their multiplicative nature. The difference between TTE and RCT estimates will be quantified as: ln(Δratio)=ln(θTTE)-ln(θRCT), where θ represents point estimates. The standard error (SE) of this log-difference will be derived using statistical error propagation principles. Since the TTE and RCT estimates are independent, their variances add:SEln(Δratio)=SEln(θTTE)2+SEln(θRCT)2.

The SEs for individual estimates will be derived from their reported confidence intervals. For a 95% CI, we use: SEln(θ)=ln(Upper CI) \- ln(Lower CI)2z0.975, where z0.9751.96 for a 95% CI. When CIs are asymmetric on the original scale, this approach appropriately captures the uncertainty after logarithmic transformation.

The 95% CI for the log-difference will be calculated as: ln(Δratio)z0.975SEln(Δratio).​ After computation on the logarithmic scale, results will be back-transformed to the original ratio scale for interpretability.

For studies reporting multiple effect estimates for the same PICO question (e.g., different matching methods or different sets of adjusted variables), we will prioritize the primary analysis as specified by the authors. When not explicitly stated, we will select the most adjusted model.

#### **Additive Measures Analysis**

For additive measures (RDs, MDs, SMDs), analysis will be conducted on the original scale using arithmetic differences: Δadditive=θTTE-θRCT. The SEs of difference will be calculated the same way as the ratio measures:  SEΔadditive=SEθTTE2+SEθRCT2.

For SMDs, we will convert all estimates to Hedges’ g to correct for small sample bias, particularly relevant in RCTs: g=d(1-34(n1+n2)-9), where d is Cohen’s d and n1 and n2 are the sample sizes of the two groups being compared.

#### **Bayesian Meta-Analytic Pooling Methods**

##### *Stratified Bayesian Meta-Analysis by Effect Measure Type*

For each effect measure type with sufficient data (≥3 studies), we will fit separate Bayesian random-effects meta-analysis models using Stan through the cmdstanr package in R. Each effect measure type will be analyzed independently, ensuring statistically appropriate treatment of their distinct properties.

For each effect measure type, the Bayesian model will be:

yiN(θi, sei2)

θiN(,2)

N(prior,σ)

N+(θ,σ)

where yi is the observed difference for study i, θi is the true study-specific difference,  is the overall mean difference, and  is the between-study standard deviation. Weakly informative priors will be specified: N(0,1) and N+(0,0.5), allowing the data to dominate posterior distributions while providing regularization.

##### *Stratified Meta-Analysis by Effect Measure Type*

Separate Bayesian hierarchical models will be fitted for each effect measure category (HRs, ORs, RRs, RDs, MDs, SMDs), acknowledging their distinct statistical properties and clinical interpretations. Each model will provide posterior distributions for measure-specific overall effects and between-study heterogeneity.

*Bayesian Hierarchical Meta-Regression for Combined Analysis*

To synthesize evidence across all effect measure types within a unified framework, we will implement a Bayesian hierarchical meta-regression model:

yiN(θi, sei2)

θiN(overall+βj\[i\],2)

overallN(0,1)

βjN(0,σβ)

N+(0,0.5)

σβN+(0,0.5)

where βj\[i\] is the effect for measure type j of study i, and σβ controls the variation in measure type effects. This model will accommodate dependency structures from multiple comparisons within studies while providing measure-specific effect estimates and overall pooled effects.

*Model Implementation and Diagnostics*

All Bayesian models will be implemented in Stan with four parallel chains, each running for 5,000 iterations including 2,000 warmup iterations. Convergence will be assessed using the potential scale reduction factor (R̂ \< 1.05), effective sample size (ESS \> 1,000), and visual inspection of trace plots. Model fit will be evaluated through posterior predictive checks comparing observed data to posterior predictive distributions.

*Bayesian Analysis of Agreement Measures*

Beyond analyzing direct differences, we will conduct Bayesian meta-analyses of agreement measures to quantify concordance between TTE and RCT estimates. For each agreement measure, we will fit appropriate Bayesian models:

1. Concordance correlation coefficient (CCC): CCCs will be analyzed using Fisher’s z-transformation with a Bayesian model:

ziN(ζi, sei2)

ζiN(z,z2)

zN(0,1)

zN+(0,0.5)

Results will be back-transformed to the CCC scale (-1 to 1\) for interpretation.

2. Mean absolute percentage error (MAPE): MAPE values will be analyzed on the log scale due to their positive support:

log(MAPEi)N(θi, sei2)

θiN(log,log2)

logN(0,1)

logN+(0,0.5)

3. Coverage probability: Coverage probabilities (proportion of TTE confidence intervals containing RCT point estimates) will be analyzed using a Bayesian binomial model:

xiB(ni, πi)

logit(πi)N(logit,logit2)

logitN(0,1.5)

logitN+(0,0.5)

*Posterior Inference and Interpretation*

From all Bayesian analyses, we will derive:

* Posterior means, medians, and modes for all parameters  
* 95% credible intervals (CrIs) for overall and subgroup effects  
* Posterior probabilities that absolute differences exceed clinically meaningful thresholds (e.g., P(|μ| \> 0.25) for ratio measures on log scale)  
* Predictive intervals for future TTE-RCT comparisons  
* Between-study heterogeneity estimates with full uncertainty quantification  
* Model comparison using widely applicable information criterion (WAIC) and leave-one-out cross-validation

##### *Sensitivity Analysis for Prior Specifications*

We will conduct comprehensive sensitivity analyses exploring alternative prior specifications:

* Skeptical priors concentrated around null effects: μ \~ Normal(0, 0.5)  
* Non-informative priors: μ \~ Uniform(-5, 5\)  
* Informative priors based on RCT-DUPLICATE findings when available  
* Alternative heterogeneity priors: τ \~ Gamma(2, 1\) and τ \~ Uniform(0, 2\)

##### *Handling Complex Dependency Structures*

For studies contributing multiple effect estimates, we will extend the basic hierarchical model to account for within-study correlation:

yi,jN(θi,j, sei,j2)

θiMVN(i,Σi)

iN(overall+Xiβ,τ2)

where yi,j represents the j-th comparison from study i, and Σi captures the within-study correlation structure. When correlation information is unavailable, we will implement sensitivity analyses across a range of plausible correlation values.

#### **Detection of Systematic Patterns**

##### *Outlier Detection*

Studies with unusually large discrepancies will be identified using Bayesian approaches. We will calculate posterior probabilities that individual study effects exceed specified thresholds: P(|θ\_i \- μ| \> 2τ | data), flagging studies with probabilities \> 0.95 for detailed investigation.

*Inlier Detection Using Likelihood Ratio Test*

Excessive similarity between effect estimates may indicate publication bias, particularly when TTEs showing large differences from target RCTs face challenges in the publication process. To detect this phenomenon, we will implement the likelihood ratio test methodology developed by [Falkenhagen et al. (2019)](https://www.zotero.org/google-docs/?UWLi95), which has been specifically designed to identify inlier-contaminated distributions.

This approach tests whether the distribution of standardized differences between TTE and RCT estimates follows a simple normal distribution (null hypothesis) or a mixture of two normal distributions with the same mean but different variances (alternative hypothesis).

Formally, for the standardized differences x=(x1, …, xn) between TTE and RCT estimates, we test:

H0:xi follows a normal distribution N(, 2\)

against the alternative hypothesis:

H1:xi follows a mixture distribution (1-)N(, 2)+N(, 2\)

where \< (the inlier component has smaller variance) and 0.5 (the inlier component represents at most half of the distribution).

The mixture density function under the alternative hypothesis is:

f,,,(x)=(1-)fN(, 2)(x)+fN(, 2)(x)

where fN(, 2)(x) is the density function of a normal distribution with mean  and variance 2:

fN(, 2)(x)=12e-(x-)222

The log-likelihood function for a sample x=(x1, …, xn) is:

l(x, (,,,))=i=1nlogf,,,(xi)

The maximum likelihood estimates of the parameters under the null hypothesis (0,0) and the alternative hypothesis (1,1,,) will be computed using numerical optimization techniques.

The likelihood ratio test statistic is then:

Λ(x)=2sup(,,,)l(x, (,,,))-sup(,)0l(x, (,,0,))

where \=(,,,)+\[0,0.05\]+|\< is the parameter space and \=(,,,)+{0}+|\< is the null parameter space.

The implementation in R will use the *stats4* package for maximum likelihood estimation:

\# Mixture model log-likelihood function

mixture\_loglik \<- function(mu, sigma, epsilon, delta, x) {

  f \<- function(x) {

    (1-epsilon) \* dnorm(x, mu, sigma) \+ epsilon \* dnorm(x, mu, delta)

  }

  sum(log(f(x)))

}

\# Normal distribution log-likelihood

normal\_loglik \<- function(mu, sigma, x) {

  sum(dnorm(x, mu, sigma, log=TRUE))

}

Since the asymptotic distribution of this test statistic does not follow standard chi-squared theory due to boundary conditions on the parameters, we will determine the null distribution through Monte Carlo simulation. The procedure is:

1. For each simulation s \= 1, 2, ..., S (S \= 10,000):  
   1. Generate a sample x(s)=x1(s),…,xn(s) of size n from N(0,1)  
   2. Calculate x(s)  
2. The critical value at significance level  is the 1--quantile of the empirical distribution of x(s)  
3. Reject H0 if (x)\>1-

In addition to the *P*\-value, we will report the estimated inlier parameters  (proportion of inliers) and  (relative concentration of inliers). A significant result with a substantial value of  would provide evidence for publication bias favoring TTEs that closely match their target RCTs.

#### **Funnel Plot Analysis**

To visually assess potential patterns of outliers and inliers, a funnel plot will be constructed. This will display:

1. Differences between TTE and RCT estimates on the horizontal axis  
2. Precision (inverse of the standard error) on the vertical axis  
3. Individual study points sized according to sample size  
4. Reference lines indicating:  
   1. Perfect agreement (difference \= 0\)  
   2. Predefined margins of agreement (±0.25 and ±0.5 on log scale for ratio measures)  
   3. 95% confidence intervals around the null difference (forming the “funnel”)

An asymmetric funnel plot may indicate systematic bias, while excessive clustering around the null difference beyond what would be expected by chance may indicate publication bias favoring concordant results.

To complement the visual assessment, we will conduct formal statistical tests for funnel plot asymmetry, including:

1. Egger's regression test: zi=b0+b1SEi+ei, where zi is the standardized difference and SEi is the standard error. A significant coefficient b1 indicates small-study effects.  
2. Modified Egger's test for detecting central tendency bias: zi=b0+b1SEi+ei​, where a negative and significant b1 would suggest excessive precision around the null difference.

*Integration of Outlier and Inlier Detection Results*

The results from these analyses will be integrated to provide a comprehensive assessment of potential biases in the TTE literature. This integrated approach accounts for:

1. Publication bias (through inlier detection)  
2. Methodological problems (through outlier detection)  
3. Small-study effects (through funnel plot analysis)

For studies identified as outliers, we will conduct sensitivity analyses excluding these studies to assess their impact on overall conclusions. For studies contributing to detected inlier patterns, we will examine their characteristics to identify potential methodological or contextual factors associated with excessive concordance between TTE and RCT estimates.

### ***Secondary Analyses***

Our secondary analyses will examine consistency patterns within specific subgroups defined by disease category, analytical method, data source type, sample size quartiles, and number of covariates. This will help identify conditions under which TTEs may be more or less reliable.

We will conduct sensitivity analyses to assess the robustness of our findings. This will include separate analyses excluding studies with high risk of bias, stratification by study quality indicators, and investigation of consistency across different effect measure types. We will also assess potential publication bias in the TTE literature.

The relationship between methodological quality indicators and estimate consistency will be thoroughly examined. This will include analysis of how the use of DAGs and protocol pre-registration affects the alignment between TTE and RCT results.

## **Analysis of Research Transparency**

Research transparency is a critical aspect of scientific rigor and reproducibility. Our dataset includes several key variables related to transparency that warrant systematic investigation:

### ***Conflict of Interest and Funding Disclosure***

* Patterns of COI disclosure, including proportions of studies with declared conflicts  
* Distribution of funding sources (public, private, industry, academic, mixed, none)  
* Relationship between funding sources and institutional affiliations  
* Association between funding sources and effect estimate consistency  
* Temporal trends in COI and funding transparency

### ***Protocol Registration***

* Rate of protocol registration across studies  
* Temporal trends in protocol registration  
* Relationship between protocol registration and estimate consistency  
* Quality of protocol documentation  
* Differences between registered and final analyses where available

***Data and Code Availability***

* Proportion of studies with publicly available datasets  
* Types of data repositories used  
* Code sharing practices and platforms  
* Completeness of shared materials  
* Barriers to accessing shared resources  
* Impact of data/code sharing on research quality

### ***Transparency Score Development***

We will develop a composite transparency score incorporating:

* Presence/absence of COI declarations  
* Completeness of funding information  
* Protocol registration status  
* Data availability  
* Code sharing practices  
* Quality of documentation

The transparency score will be used to:

* Track temporal trends in research transparency  
* Analyze geographical patterns in transparency practices  
* Assess relationships between transparency and methodological rigor  
* Examine associations between transparency and effect estimate consistency

## **Quality Control**

Quality control measures will include double data extraction for key variables by independent reviewers. Statistical analyses will be validated by an independent statistician to ensure accuracy and reliability. Multiple sensitivity analyses will be conducted to assess the robustness of our findings to various analytical choices.

# **Ethical Considerations**

This study involves analysis of published data and does not require ethical approval. Nevertheless, we will maintain high standards of research integrity throughout the study.

# **Dissemination Plan**

The results of this study will be published in peer-reviewed journals and presented at relevant scientific conferences. We will ensure that all findings, including negative results, are reported transparently and comprehensively.

# 

# **References**

[Bauchner, H., & Fontanarosa, P. B. (2020). Randomized Clinical Trials and COVID-19: Managing Expectations. *JAMA*, *323*(22), 2262\. https://doi.org/10.1001/jama.2020.8115](https://www.zotero.org/google-docs/?qXBOhJ)  
[Bothwell, L. E., Greene, J. A., Podolsky, S. H., & Jones, D. S. (2016). Assessing the Gold Standard—Lessons from the History of RCTs. *New England Journal of Medicine*, *374*(22), 2175–2181. https://doi.org/10.1056/NEJMms1604593](https://www.zotero.org/google-docs/?qXBOhJ)  
[Cowie, M. R., Blomster, J. I., Curtis, L. H., Duclaux, S., Ford, I., Fritz, F., Goldman, S., Janmohamed, S., Kreuzer, J., Leenay, M., Michel, A., Ong, S., Pell, J. P., Southworth, M. R., Stough, W. G., Thoenes, M., Zannad, F., & Zalewski, A. (2017). Electronic health records to facilitate clinical research. *Clinical Research in Cardiology*, *106*(1), 1–9. https://doi.org/10.1007/s00392-016-1025-6](https://www.zotero.org/google-docs/?qXBOhJ)  
[Danaei, G., García Rodríguez, L. A., Cantero, O. F., Logan, R. W., & Hernán, M. A. (2018). Electronic medical records can be used to emulate target trials of sustained treatment strategies. *Journal of Clinical Epidemiology*, *96*, 12–22. https://doi.org/10.1016/j.jclinepi.2017.11.021](https://www.zotero.org/google-docs/?qXBOhJ)  
[Dickerman, B. A., García-Albéniz, X., Logan, R. W., Denaxas, S., & Hernán, M. A. (2019). Avoidable flaws in observational analyses: An application to statins and cancer. *Nature Medicine*, *25*(10), 1601–1606. https://doi.org/10.1038/s41591-019-0597-x](https://www.zotero.org/google-docs/?qXBOhJ)  
[Falkenhagen, U., Kössler, W., & Lenz, H.-J. (2019). A Likelihood Ratio Test for Inlier Detection. In A. Steland, E. Rafajłowicz, & O. Okhrin (Eds.), *Stochastic Models, Statistics and Their Applications* (Vol. 294, pp. 351–359). Springer International Publishing. https://doi.org/10.1007/978-3-030-28665-1\_26](https://www.zotero.org/google-docs/?qXBOhJ)  
[Franklin, J. M., & Schneeweiss, S. (2017). When and How Can Real World Data Analyses Substitute for Randomized Controlled Trials? *Clinical Pharmacology & Therapeutics*, *102*(6), 924–933. https://doi.org/10.1002/cpt.857](https://www.zotero.org/google-docs/?qXBOhJ)  
[Frieden, T. R. (2017). Evidence for Health Decision Making—Beyond Randomized, Controlled Trials. *New England Journal of Medicine*, *377*(5), 465–475. https://doi.org/10.1056/NEJMra1614394](https://www.zotero.org/google-docs/?qXBOhJ)  
[García-Albéniz, X., Hsu, J., & Hernán, M. A. (2017). The value of explicitly emulating a target trial when using real world evidence: An application to colorectal cancer screening. *European Journal of Epidemiology*, *32*(6), 495–500. https://doi.org/10.1007/s10654-017-0287-2](https://www.zotero.org/google-docs/?qXBOhJ)  
[Glesby, M. J., & Hoover, D. R. (1996). Survivor treatment selection bias in observational studies: Examples from the AIDS literature. *Annals of Internal Medicine*, *124*(11), 999–1005. https://doi.org/10.7326/0003-4819-124-11-199606010-00008](https://www.zotero.org/google-docs/?qXBOhJ)  
[Gomes, M., Turner, A. J., Sammon, C., Dawoud, D., Ramagopalan, S., Simpson, A., & Siebert, U. (2024). Acceptability of Using Real-World Data to Estimate Relative Treatment Effects in Health Technology Assessments: Barriers and Future Steps. *Value in Health*, *27*(5), 623–632. https://doi.org/10.1016/j.jval.2024.01.020](https://www.zotero.org/google-docs/?qXBOhJ)  
[Hansford, H. J., Cashin, A. G., Jones, M. D., Swanson, S. A., Islam, N., Dahabreh, I. J., Dickerman, B. A., Egger, M., Garcia-Albeniz, X., Golub, R. M., Lodi, S., Moreno-Betancur, M., Pearson, S.-A., Schneeweiss, S., Sterne, J., Sharp, M. K., Stuart, E. A., Hernan, M. A., Lee, H., & McAuley, J. H. (2023). Development of the TrAnsparent ReportinG of observational studies Emulating a Target trial (TARGET) guideline. *BMJ Open*, *13*(9), e074626. https://doi.org/10.1136/bmjopen-2023-074626](https://www.zotero.org/google-docs/?qXBOhJ)  
[Hemkens, L. G., Contopoulos-Ioannidis, D. G., & Ioannidis, J. P. A. (2016). Agreement of treatment effects for mortality from routinely collected data and subsequent randomized trials: Meta-epidemiological survey. *BMJ*, i493. https://doi.org/10.1136/bmj.i493](https://www.zotero.org/google-docs/?qXBOhJ)  
[Hernán, M. A. (2018). The C-Word: Scientific Euphemisms Do Not Improve Causal Inference From Observational Data. *American Journal of Public Health*, *108*(5), 616–619. https://doi.org/10.2105/AJPH.2018.304337](https://www.zotero.org/google-docs/?qXBOhJ)  
[Hernán, M. A., & Robins, J. M. (2016). Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available: Table 1\. *American Journal of Epidemiology*, *183*(8), 758–764. https://doi.org/10.1093/aje/kwv254](https://www.zotero.org/google-docs/?qXBOhJ)  
[Hernan, M. A., & Robins, J. M. (2025). Randomized experiments. In *Causal Inference: What If* (pp. 13–26). Chapman & Hall/CRC. https://miguelhernan.org/whatifbook](https://www.zotero.org/google-docs/?qXBOhJ)  
[Hernán, M. A., Sauer, B. C., Hernández-Díaz, S., Platt, R., & Shrier, I. (2016). Specifying a target trial prevents immortal time bias and other self-inflicted injuries in observational analyses. *Journal of Clinical Epidemiology*, *79*, 70–75. https://doi.org/10.1016/j.jclinepi.2016.04.014](https://www.zotero.org/google-docs/?qXBOhJ)  
[Hripcsak, G., Duke, J. D., Shah, N. H., Reich, C. G., Huser, V., Schuemie, M. J., Suchard, M. A., Park, R. W., Wong, I. C. K., Rijnbeek, P. R., van der Lei, J., Pratt, N., Norén, G. N., Li, Y.-C., Stang, P. E., Madigan, D., & Ryan, P. B. (2015). Observational Health Data Sciences and Informatics (OHDSI): Opportunities for Observational Researchers. *Studies in Health Technology and Informatics*, *216*, 574–578.](https://www.zotero.org/google-docs/?qXBOhJ)  
[Labrecque, J. A., & Swanson, S. A. (2017). Target trial emulation: Teaching epidemiology and beyond. *European Journal of Epidemiology*, *32*(6), 473–475. https://doi.org/10.1007/s10654-017-0293-4](https://www.zotero.org/google-docs/?qXBOhJ)  
[Lodi, S., Phillips, A., Lundgren, J., Logan, R., Sharma, S., Cole, S. R., Babiker, A., Law, M., Chu, H., Byrne, D., Horban, A., Sterne, J. A. C., Porter, K., Sabin, C., Costagliola, D., Abgrall, S., Gill, J., Touloumi, G., Pacheco, A. G., … INSIGHT START Study Group and the HIV-CAUSAL Collaboration. (2019). Effect Estimates in Randomized Trials and Observational Studies: Comparing Apples With Apples. *American Journal of Epidemiology*, *188*(8), 1569–1577. https://doi.org/10.1093/aje/kwz100](https://www.zotero.org/google-docs/?qXBOhJ)  
[McKenzie, J. E., Brennan, S. E., Ryan, R. E., Thomson, H. J., Johnston, R. V., & Thomas, J. (2019). Chapter 3: Defining the criteria for including studies and how they will be grouped for the synthesis. In *Cochrane Handbook for Systematic Reviews of Interventions version 6.5 (updated August 2024\)*. John Wiley & Sons. www.training.cochrane.org/handbook](https://www.zotero.org/google-docs/?qXBOhJ)  
[Peto, R., Pike, M. C., Armitage, P., Breslow, N. E., Cox, D. R., Howard, S. V., Mantel, N., McPherson, K., Peto, J., & Smith, P. G. (1976). Design and analysis of randomized clinical trials requiring prolonged observation of each patient. I. Introduction and design. *British Journal of Cancer*, *34*(6), 585–612. https://doi.org/10.1038/bjc.1976.220](https://www.zotero.org/google-docs/?qXBOhJ)  
[R Core Team. (2025). *R: A Language and Environment for Statistical Computing*. R Foundation for Statistical Computing. https://www.R-project.org/](https://www.zotero.org/google-docs/?qXBOhJ)  
[Schulz, K. F., Chalmers, I., Hayes, R. J., & Altman, D. G. (1995). Empirical evidence of bias. Dimensions of methodological quality associated with estimates of treatment effects in controlled trials. *JAMA*, *273*(5), 408–412. https://doi.org/10.1001/jama.273.5.408](https://www.zotero.org/google-docs/?qXBOhJ)  
[Sherman, R. E., Anderson, S. A., Dal Pan, G. J., Gray, G. W., Gross, T., Hunter, N. L., LaVange, L., Marinac-Dabic, D., Marks, P. W., Robb, M. A., Shuren, J., Temple, R., Woodcock, J., Yue, L. Q., & Califf, R. M. (2016). Real-World Evidence—What Is It and What Can It Tell Us? *New England Journal of Medicine*, *375*(23), 2293–2297. https://doi.org/10.1056/NEJMsb1609216](https://www.zotero.org/google-docs/?qXBOhJ)  
[Speich, B., Von Niederhäusern, B., Schur, N., Hemkens, L. G., Fürst, T., Bhatnagar, N., Alturki, R., Agarwal, A., Kasenda, B., Pauli-Magnus, C., Schwenkglenks, M., & Briel, M. (2018). Systematic review on costs and resource use of randomized clinical trials shows a lack of transparent and comprehensive data. *Journal of Clinical Epidemiology*, *96*, 1–11. https://doi.org/10.1016/j.jclinepi.2017.12.018](https://www.zotero.org/google-docs/?qXBOhJ)  
[Toews, I., Anglemyer, A., Nyirenda, J. L., Alsaid, D., Balduzzi, S., Grummich, K., Schwingshackl, L., & Bero, L. (2024). Healthcare outcomes assessed with observational study designs compared with those assessed in randomized trials: A meta-epidemiological study. *Cochrane Database of Systematic Reviews*, *2024*(1). https://doi.org/10.1002/14651858.MR000034.pub3](https://www.zotero.org/google-docs/?qXBOhJ)  
[Wang, S. V., Schneeweiss, S., RCT-DUPLICATE Initiative, Franklin, J. M., Desai, R. J., Feldman, W., Garry, E. M., Glynn, R. J., Lin, K. J., Paik, J., Patorno, E., Suissa, S., D’Andrea, E., Jawaid, D., Lee, H., Pawar, A., Sreedhara, S. K., Tesfaye, H., Bessette, L. G., … Quinto, K. (2023). Emulation of Randomized Clinical Trials With Nonrandomized Database Analyses: Results of 32 Clinical Trials. *JAMA*, *329*(16), 1376–1385. https://doi.org/10.1001/jama.2023.4221](https://www.zotero.org/google-docs/?qXBOhJ)  
[Wood, L., Egger, M., Gluud, L. L., Schulz, K. F., Jüni, P., Altman, D. G., Gluud, C., Martin, R. M., Wood, A. J. G., & Sterne, J. A. C. (2008). Empirical evidence of bias in treatment effect estimates in controlled trials with different interventions and outcomes: Meta-epidemiological study. *BMJ (Clinical Research Ed.)*, *336*(7644), 601–605. https://doi.org/10.1136/bmj.39465.451748.AD](https://www.zotero.org/google-docs/?qXBOhJ)

**Appendix 1\.** Search strategy and number of records for the latest database search.

Database: Embase \<1974 to 2025 January 03\>, Ovid MEDLINE(R) and Epub Ahead of Print, In-Process, In-Data-Review & Other Non-Indexed Citations \<1996 to January 03, 2025\> 

Search Strategy: 

1  (trial and emulat\*).mp. (2647) 

2  target trial\*.mp. (2697) 

3  pseudotrial\*.mp. (10) 

4  emulated trial\*.mp. (150) 

5  1 or 2 or 3 or 4 (3998) 

6  remove duplicates from 5 (2606) 

7  limit 6 to dt=20241127-20241231 \[Limit not valid in Embase; records were retained\] (2439) 

8  limit 7 to dd=20241127-20241231 \[Limit not valid in Ovid MEDLINE(R); records were retained\] (61)

**Appendix 2\.** Study characteristics variables.

| Category | Variable | Description |
| :---- | :---- | :---- |
| **Publication Metadata** | Study ID | Unique identifier for each study |
|  | First author | First author surname |
|  | Year | Publication year |
|  | DOI | Digital object identifier |
|  | Preprint status | Whether publication is a preprint |
|  | Abstract presentation | Whether presented as conference abstract |
|  | Institution type | Academic, industry, government, mixed |
|  | Institution names | Names of affiliated institutions |
| **Research Transparency** | COI | Declared conflicts of interest |
|  | COI institutions | Institutions with potential conflicts |
|  | Funding | Funding sources |
|  | Funding institutions | Names of funding institutions |
|  | Protocol availability | Whether a protocol was published |
|  | Data URL | Link to publicly available data |
|  | Code URL | Link to publicly available code |
| **Study Context** | Disease | Specific disease studied |
|  | Disease category | Disease classification category |
|  | Data type | Claims, EHR, registry, survey, other |
|  | Data sources n | Number of data sources |
|  | Data geography | Geographic location(s) of data |
| **Methodological Approach** | Missing method | Method for handling missing data |
|  | Matching method | Method used for matching |
|  | Analysis method | Statistical analysis approach |
|  | Estimand | Type of estimand targeted |
|  | Design hypothesis | Study design hypothesis framework |
|  | DAG | Whether directed acyclic graph was used |
|  | QBA | Whether quantitative bias analysis was performed |
| **Sample Characteristics** | N covariates | Number of covariates used |
|  | Trts n | Number of treatments examined |
|  | Eligible sample | Characteristics of eligible population |
|  | N trt | Number in treatment group |
|  | N ctrl | Number in control group |
|  | N emulations | Number of emulations performed |
| **Target Trial Information** | Target trial name | Name of reference RCT |
|  | Target trial reg no | Registration number of reference RCT |
|  | Target trial DOI | DOI of reference RCT |

**Appendix 3\.** PICO elements and effect estimates variables.

| Category | Variable | Description |
| :---- | :---- | :---- |
| **Study Identifiers** | Study ID | Unique identifier for each study |
|  | First author | First author surname |
|  | Year | Publication year |
|  | DOI | Digital object identifier |
| **PICO Elements** | Population | Characteristics of study population |
|  | Intervention | Description of intervention |
|  | Comparison | Description of comparator |
|  | Outcome | Description of outcome measured |
|  | Intervention RCT | Intervention as defined in reference RCT |
|  | Comparison RCT | Comparison as defined in reference RCT |
| **Effect Measure Details** | Outcome type | Binary, continuous, time-to-event |
|  | Effect measure | HR, OR, RR, RD, MD, SMD |
| **RCT Effect Estimates** | RCT estimate | Point estimate from RCT |
|  | RCT lb | Lower bound of 95% CI from RCT |
|  | RCT ub | Upper bound of 95% CI from RCT |
| **TTE Effect Estimates** | TTE estimate | Point estimate from TTE |
|  | TTE lb | Lower bound of 95% CI from TTE |
|  | TTE ub | Upper bound of 95% CI from TTE |
| **Sample Sizes** | N trt RCT | Sample size in RCT treatment group |
|  | N ctrl RCT | Sample size in RCT control group |
|  | N trt TTE | Sample size in TTE treatment group |
|  | N ctrl TTE | Sample size in TTE control group |
| **Comparative Metrics** | TTE RCT diff estimate | Difference between TTE and RCT estimates |
| **Comparative Metrics** | TTE RCT diff lb | Lower bound of difference 95% CI |
| **Comparative Metrics** | TTE RCT diff ub | Upper bound of difference 95% CI |

