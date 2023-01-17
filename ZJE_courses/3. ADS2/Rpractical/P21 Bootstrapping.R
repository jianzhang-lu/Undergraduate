library(tidyverse)
# Q1
## Plot the data.
data <- read.table("ADS_practical/Reporter_assay_4-1-15.txt", header = T)
ggplot(data, aes(x = Category, y = ave)) +
  geom_boxplot(aes(fill = Category))

## Generate the first bootstrap sample.
active <- filter(data, Epigenetic_status == "Active")
repressed <- filter(data, Epigenetic_status == "Repressed")
median_diff <- median(active$ave) - median(repressed$ave)

length_active <- nrow(active)
length_repressed <- nrow(repressed)
bootstrap_active <- median(sample(data$ave, length_active, replace = T))
bootstrap_repressed <- median(sample(data$ave, length_repressed, replace = T))
bootstrap_median <- bootstrap_active - bootstrap_repressed

## Generate a large number of bootstraps.
boot <- function(num){
  bootstrap_medians <- c()
  for (i in 1:num){
  bootstrap_active <- median(sample(data$ave, length_active, replace = T))
  bootstrap_repressed <- median(sample(data$ave, length_repressed, replace = T))
  bootstrap_median <- bootstrap_active - bootstrap_repressed
  bootstrap_medians <- c(bootstrap_medians, bootstrap_median)
  }
  return(bootstrap_medians)
}
medians1 <- boot(1000)
hist(medians1)
abline(v = median_diff, col = 'red', lwd = 2)

## Make a statistical inference.
p_value <- mean(medians1 >= median_diff)

## Explore the number of replicates.
replicates <- data.frame("replicate" = rep(seq(100,1000,100), each = 100),
                         "q_values" = -100)
q_values <- c()

for (i in seq(100,1000,100)){
  for (replicate in 1:100){
    medians <- boot(i)
    q_value <- mean(medians >= median_diff)
    q_values <- c(q_values, q_value)
  }
}
replicates$q_values <- q_values

ggplot(replicates, aes(x = factor(replicate), y = q_values)) +
  geom_boxplot(aes(fill = factor(replicate))) +
  labs(x = replicate)

## Repeat this procedure by looking at the Transcription_status variable.

# Q2
## Plot the data.
data2 <- read.csv("ADS_practical/coronavirus.csv", header = T)
data2$percentage <- data2$New/data2$Total

ggplot(data2, aes(x = Country, y = percentage)) +
  geom_point() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

## Generate a first bootstrap sample.
total <- 80796
new <- 18
old <-  total - new
obs_sample <- c(rep("new", new), rep("old", old))
summary(factor(obs_sample))
table(obs_sample)

bootstrap_sample <- sample(obs_sample, length(obs_sample), replace = T)
summary(factor(bootstrap_sample))

## Generate a confidence interval by bootstrapping many times.
boot2 <- function(num){
  boot_results <- c()
  for(i in 1:num){
    boot_sample <- sample(obs_sample, length(obs_sample), T)
    new_length <- sum(boot_sample == "new")
    boot_results <- c(boot_results, new_length)
  }
  return(boot_results)
}

result2 <- boot2(1000)
lower <- quantile(result2, 0.025)
higher <- quantile(result2, 0.975)

per_real <- new/total
per_lower <- as.numeric(lower/total)
per_higher <- as.numeric(higher/total)

## Repeat this bootstrapping for the entire dataset.
data2$upper <- 0
data2$lower <- 0

generate_sample <- function(new, total){
  old <- total - new
  dataset <- c(rep("new", new), rep("old", old))
  return(dataset)
}

boot3 <- function(sample){
  boot_results <- c()
  for(i in 1:100){
    boot_sample <- sample(sample, length(sample), T)
    new_length <- sum(boot_sample == "new")
    boot_results <- c(boot_results, new_length)
  }
  return(boot_results)
}

for (i in 1:nrow(data2)){
  dataset <- generate_sample(data2[i,3], data2[i,2])
  results <- boot3(dataset)
  data2[i,5] <- quantile(results, 0.975)/data2[i,2]
  data2[i,6] <- quantile(results, 0.025)/data2[i,2]
}

## Explore the differences across countries.
ggplot(data2, aes(x = Country, y = percentage)) +
  geom_point() +
  geom_errorbar(aes(ymin = lower, ymax = upper), width = 0.3) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))
  


