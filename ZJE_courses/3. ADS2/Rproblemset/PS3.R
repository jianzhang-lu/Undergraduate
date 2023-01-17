# Sampling from a population

library(tidyverse)
population <- rnorm(1e6, 100, 5)
round(mean(population), 2)
sample(population, 5, replace = T)
frame <- replicate(n = 1000, sample(population, 5, replace = T))
sample_mean <- apply(frame, MARGIN = 2, FUN = mean)
sample_sd <- apply(frame, MARGIN = 2, FUN = sd)
hist(sample_mean, main = "the sample mean", col = "green")
hist(sample_sd, main = "the sample sd", col = "red")
mean_of_means <- mean(sample_mean)
mean_of_sd <- mean(sample_sd)


# Breakfast and student performance
# Getting information about sensitive topics

# about 24.67% 