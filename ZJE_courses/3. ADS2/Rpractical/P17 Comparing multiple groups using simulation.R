library(tidyverse)

# Import and plot the data
data <- read.csv("D:/R_document/ADS_practical/drug_trial.csv")
data$treatment <- factor(data$treatment, levels = c("drugA","drugB","placebo"))
ggplot(data, aes(x = treatment, y = pain)) +
  geom_boxplot(aes(color = treatment))

# Do the simulation
same_group <- c()
different_group <- c()
for(i in 1:1000){
  sample_index <- sample(1:nrow(data), 2, replace = F)
  sample1 <- data[sample_index[1],]
  sample2 <- data[sample_index[2],]
  pain_diff <- abs(sample1$pain - sample2$pain)
  if (sample1$treatment == sample2$treatment){
    same_group <- c(same_group, pain_diff)
  }
  else{
    different_group <- c(different_group, pain_diff)
  }
}

class_result <- c(rep("same group", length(same_group)), 
                  rep("different group", length(different_group)))
pain_result <- c(same_group, different_group)
result <- data.frame("group" = class_result, "difference" = pain_result)
ggplot(result, aes(x = factor(group, levels = c("same group", "different group")), 
                   y = difference)) +
  geom_boxplot(aes(fill = group)) +
  labs(x = NULL)
mean(same_group)
mean(different_group)

# Run a test to find out!
hist(same_group)
hist(different_group)
shapiro.test(same_group)$p
shapiro.test(different_group)$p
## The p-value is small enough, therefore, we can not accept H0 hypothesis.
wilcox.test(same_group, different_group)$p.value
