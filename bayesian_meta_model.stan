
data {
  int<lower=0> N;                    // number of studies
  int<lower=0> K;                    // number of effect measure types
  vector[N] y;                       // observed differences
  vector<lower=0>[N] se;             // standard errors
  array[N] int<lower=1,upper=K> measure;   // effect measure type indicator
}

parameters {
  vector[K] mu;                      // mean effect for each measure type
  vector<lower=0>[K] tau;            // between-study SD for each measure type
  vector[N] theta;                   // study-specific effects
}

model {
  // Priors
  mu ~ normal(0, 1);
  tau ~ normal(0, 0.5);
  
  // Hierarchical model
  for (n in 1:N) {
    theta[n] ~ normal(mu[measure[n]], tau[measure[n]]);
    y[n] ~ normal(theta[n], se[n]);
  }
}

generated quantities {
  vector[K] mu_exp;                  // exponentiated effects for ratio measures
  vector[K] tau_squared;             // tau squared
  
  for (k in 1:K) {
    mu_exp[k] = exp(mu[k]);
    tau_squared[k] = tau[k]^2;
  }
}

