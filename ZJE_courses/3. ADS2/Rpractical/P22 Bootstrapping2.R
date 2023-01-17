library(tidyverse)

# 1. Are women better than men at quidditch?
## Plot the data
data <- read.csv("ADS_practical/quidditch_league.csv")
ggplot(data, aes(x = gender, y = points)) +
  geom_boxplot(aes(fill = gender)) +
  geom_point()


## H0: Mean in woman is equal to man
## HA: Mean in woman is not equal to man
## Permutation test
## Bootstrap or wilcox.test

Female <- data[data$gender == "F", "points"]
Male <- data[data$gender == "M", "points"]
pool <- c(Female, Male)
real_mean <- abs(mean(Female) - mean(Male))
boot_means <- c()

for (i in 1:10000){
  boot_sample <- sample(pool, length(pool), F)
  boot_female <- boot_sample[1:length(Female)]
  boot_male <- boot_sample[(length(Female)+1):length(pool)]
  boot_mean <- abs(mean(boot_female) - mean(boot_male))
  boot_means <- c(boot_means, boot_mean)
}

hist(boot_means, 10)
abline(v = real_mean, col = "red", lwd = 3)
p_value <- mean(boot_means >= real_mean)
wilcox.test(Female, Male, alternative = "greater", exact = F)

# 2. Does this depend on who is a woman and a man though?
boot_gender <- function(data){
  boot_genders <- c()
  for(i in 1:nrow(data)){
    gender_prob <- data$prob_male[i]
    boot_gender <- sample(c("M", "F"), 1, F, 
                          prob = c(gender_prob, 1-gender_prob))
    boot_genders <- c(boot_genders, boot_gender)
  }
  return(boot_genders)
}

for(i in 1:1000){
  data$gender <- boot_gender(data)
  Female <- data[data$gender == "F", "points"]
  Male <- data[data$gender == "M", "points"]
  pool <- c(Female, Male)
  boot_sample <- sample(pool, length(pool), F)
  boot_female <- boot_sample[1:length(Female)]
  boot_male <- boot_sample[(length(Female)+1):length(pool)]
  boot_mean <- abs(mean(boot_female) - mean(boot_male))
  boot_means <- c(boot_means, boot_mean)
}

hist(boot_means, 10)
abline(v = real_mean, col = "red", lwd = 3)
p_value <- mean(boot_means >= real_mean)


