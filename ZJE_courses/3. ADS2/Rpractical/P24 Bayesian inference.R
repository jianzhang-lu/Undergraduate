library(tidyverse)
# Is the Guinness factory adding enough barley?
bayesian <- data.frame('P1' = rep(seq(0.1, 1, 0.1), 10),
                       'P2' = rep(seq(0.1, 1, 0.1), each = 10))
bayesian$factor <- bayesian$P1/bayesian$P2

ggplot(bayesian, aes(x = P1, y = P2)) +
  geom_point(aes(size = factor)) +
  scale_x_continuous(breaks = seq(0.1, 1, 0.1)) +
  scale_y_continuous(breaks = seq(0.1, 1, 0.1))


# A dice game: 1 for 6, 0 for others
samples <- list()
for(i in 1:6){
  sample <- c(rep(1, i), rep(0, 6-i))
  samples[[i]] <- sample
}

results <- c()
for(H in 1:6){
  probs <- c()
  sample <- samples[[H]]
  for(i in 1:10000){
    dice_data <- sample(sample, 20, T)
    prob <- sum(dice_data) == 7
    probs <- c(probs, prob)
  }
  results <- c(results, mean(probs))
}