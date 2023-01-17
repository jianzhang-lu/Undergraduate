# 1. Width of the sampling distribution and sample size.

## What’s the standard deviation of the sampling distribution.

library(tidyverse)
sample_size <- c(5 : 100)
population <- rnorm(1e6, 100, 5)
sample_sd <- function(n){
  replicate(1000, sample(population, n, replace = T)) %>%
    apply(MARGIN = 2, mean) %>%
    sd()
}
new_data <- data.frame("size" = sample_size)
sd <- apply(new_data, MARGIN = 1, sample_sd)
new_data$sd <- sd
plot(new_data$size, new_data$sd, xlab = "sample size", 
     ylab = "sd of sampling distribution")
ggplot(data = new_data, aes(size, sd)) +
  geom_point() +
  labs(x ="sample size", y = "sd of sampling distribution") +
  scale_x_continuous(breaks = seq(5, 100, 5))

# 2. Rolling dice

## Roll a six-faced dice in R

roll <- sample(c(1 : 6), 1)

## Roll your dice 1000 time and visualise the outcome 

roll_data <- replicate(n = 1000, sample(6, 1))
hist(roll_data, main = "Roll 1000 times data", xlab = "number", 
     col = "green", ylim = c(1,200))
table(roll_data)
barplot(c(189, 152, 171, 168, 151, 169), 
        names.arg = c(1,2,3,4,5,6), ylim = c(1,200), col = "green")

## optimize the hist

hist(roll_data, main = "Roll 1000 times data", xlab = "number", col = "green", 
      ylim = c(1,200), breaks = c(0.5 : 6.5))
roll_new_data = data.frame("number" = roll_data)
ggplot(data = roll_new_data) +
  geom_bar(aes(x = number), fill = "green", color = "red") +
  scale_x_continuous (breaks = c(1:6)) + 
  ylim(c(0, 200))

## roll 2 dice.

roll_two_data <- replicate(n = 1000, sum(sample(6, 2, replace = T)))
hist(roll_two_data, breaks = c(1.5 : 12.5))
sum_of_1sd <- sum(roll_two_data < mean(roll_two_data) + sd(roll_two_data) &
      roll_two_data > mean(roll_two_data) - sd(roll_two_data))
prob_of_1sd <- sum_of_1sd/1000 

sum_of_2sd <- sum(roll_two_data < mean(roll_two_data) + 2*sd(roll_two_data) &
                    roll_two_data > mean(roll_two_data) - 2*sd(roll_two_data))
prob_of_2sd <- sum_of_2sd/1000

sum_of_3sd <- sum(roll_two_data < mean(roll_two_data) + 3*sd(roll_two_data) &
                    roll_two_data > mean(roll_two_data) - 3*sd(roll_two_data))
prob_of_3sd <- sum_of_3sd/1000
# normal distribution


# 3. Dragon wingspans

## Import the file and visualise the data 

dragon <- read.csv("ADS_practical/dragons.csv")
ggplot(dragon, aes(x = c(1:500), y = wingspan)) +
  geom_point()
plot(x = c(1:500), y = dragon$wingspan)

## Create a sampling distribution 

new_dragon_data <- replicate(10000, sample(dragon$wingspan, 10, replace = F))
means <- apply(new_dragon_data, 2, mean)
hist(means, main = "Sampling distribution", xlim = c(0,10), col = "skyblue")
means_frame <- data.frame(means)
ggplot(data = means_frame) +
  geom_histogram(aes(x = means), color = "red", fill = "skyblue", 
                 binwidth = 0.9) +
  labs(title = "Sampling distribution", y = "Frequency")
