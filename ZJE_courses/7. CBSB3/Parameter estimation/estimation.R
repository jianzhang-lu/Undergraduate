# calculate chi-squared error between the model with 5 parameters (params) and data of a given subject (subj) 
# parameter 1 - utility function curvature (alpha) exp of normal distribution, mean = -1.5, SD = 2
# parameter 2 - sigmoidal steepness (beta) exp of normal distribution, mean = 1.5, SD = 1
# parameter 3 - effort cost baseline (b) – normal distribution, mean = 0, SD = 1
# parameter 4 - sprint stamina (epsilon_spr) square root of uniform distribution between 0 and 1
# parameter 5 - endurance stamina (epsilon_end) square root of uniform distribution between 0 and 1
# IMPORTANT: data should be loaded as a global variable before calling the function and devs computed

data <- read.csv(file = 'CBSB3_workshop/Parameter estimation/data.csv', header = FALSE)
devs <- c()

## computing the variance of each performance measure in the population
for (i in 1:12){
  devs <- c(devs, var(data[,i]))
  }

calc_error <- function(subj, params) {
  which = 0
  err = 0
  Evals = c(1, params[4], params[5], params[4]*params[5])
  xvals = c(0.2, 0.5, 1)
  for (E in Evals)
    for (x in xvals)
    {
      which = which + 1
      tau = params[3] + 2*(1-E)
      u = x^params[1] - tau
      psuccess = 1/(1 + exp(-params[2]*u))
      err = err + (psuccess-data[subj, which])^2/devs[which]
    }
  return(err)
}

# example - 4th set of parameters from estparams.csv
print(calc_error(4, c(0.061112, 30.724, 0.92239, 0.969, 0.99762)))

# Monte Carlo search + localized search
library(tidyverse)

estimate <- function(subj, n){
  # Original data with only distribution (for further adding values)
  first_est_ori <- data.frame('alpha' = rnorm(n, mean = -1.5, sd = 2),
                              'beta' = rnorm(n, mean = 1.5, sd = 1),
                              'b' = rnorm(n, mean = 0, sd = 1),
                              'epsilon_spr' = runif(n, 0, 1),
                              'epsilon_end' = runif(n, 0, 1))
  
  # Final data with modified distribution
  first_est <- data.frame('alpha' = exp(first_est_ori$alpha),
                          'beta' = exp(first_est_ori$beta),
                          'b' = first_est_ori$b,
                          'epsilon_spr' = sqrt(first_est_ori$epsilon_spr),
                          'epsilon_end' = sqrt(first_est_ori$epsilon_end))

  # Calculate chi-squares
  all_chi <- c()
  for (i in 1:n){
    chi_square <- calc_error(subj, c(t(first_est[i, ])))
    all_chi <- c(all_chi, chi_square)
  }
  
  # Add chi-square values for the first estimation
  first_est$chi <- all_chi
  first_est_ori$chi <- all_chi
  
  # Sort according to the chi-square values and retain the top 1% smallest.
  smaller_n <- round(0.01*n, 0)
  first_est_top <- arrange(first_est, chi)[1:smaller_n, -6]
  first_est_ori_top <- arrange(first_est_ori, chi)[1:smaller_n, -6]
  
  # Generate new sets for these old sets with a smaller range (20%)
  second_est_ori <- data.frame()
  for (i in 1:smaller_n){
    old_set <- c(first_est_ori_top[i, ])
    add1 <- data.frame('alpha' = rnorm(smaller_n, mean = 0, sd = 0.4),
                       'beta' = rnorm(smaller_n, mean = 0, sd = 0.2),
                       'b' = rnorm(smaller_n, mean = 0, sd = 0.2),
                       'epsilon_spr' = runif(smaller_n, 0, 0.2),
                       'epsilon_end' = runif(smaller_n, 0, 0.2))
    second_est_ori <- rbind(second_est_ori, old_set+add1)
  }
  
  # Modify the parameters for second_est_ori
  second_est <- data.frame('alpha' = exp(second_est_ori$alpha),
                           'beta' = exp(second_est_ori$beta),
                           'b' = second_est_ori$b,
                           'epsilon_spr' = sqrt(second_est_ori$epsilon_spr),
                           'epsilon_end' = sqrt(second_est_ori$epsilon_end))
  
  # Calculate chi-squares again
  all_chi2 <- c()
  for (i in 1:n){
    chi_square2 <- calc_error(subj, c(t(second_est[i, ])))
    all_chi2 <- c(all_chi2, chi_square2)
  }
  
  second_est$chi <- all_chi2
  # Generate the best parameter sets for one person 
  # parameter 4 and 5 should be smaller than 1.
  appro_second_est <- second_est %>% 
    filter(epsilon_spr < 1 & epsilon_end < 1)
  
  second_est_top <- arrange(appro_second_est, chi)[1, ]
  return(second_est_top)
}

parameters <- data.frame()
for (person in 1:27){
  parameters <- rbind(parameters, estimate(person, 10000))
}


# Test the correlation
my <- parameters
example <- read.csv('CBSB3_workshop/Parameter estimation/estparams.csv', header = F)
cor(my$alpha, example$V1)
cor(my$beta, example$V2)
cor(my$b, example$V3)
cor(my$epsilon_spr, example$V4)
cor(my$epsilon_end, example$V5)

write.csv(parameters, 'CBSB3_workshop/Parameter estimation/My_parameter.csv')


