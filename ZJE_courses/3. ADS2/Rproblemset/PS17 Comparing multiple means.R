library(tidyverse)

data <- read.csv("D:/R_document/ADS_practical/jellybeans.csv")
color <- unique(data$colour)
data$colour <- factor(data$colour, levels = color)
color[1] <- "white"
color[6] <- "aquamarine"
color[16] <- "#c6aeaa"
color[18] <- "#adb4c9"
color[20] <- "#FFDAB9"
# ggplot 删除坐标轴文本
ggplot(data, aes(x = colour, y = score)) +
  geom_boxplot(aes(fill = colour), size = 0.6) +
  theme(axis.text.x = element_blank()) +
  labs(title = "Jelly beans") +
  scale_fill_manual(values = color)

ggplot(data, aes(x = colour, y = score)) +
  geom_boxplot(aes(fill = colour), size = 0.6) +
  theme(axis.text.x = element_text(angle = 45, size = 10, vjust = 0.5)) +
  labs(title = "Jelly beans") +
  scale_fill_manual(values = color)

## I choose yellow and mauve
yellow <- data[data$colour == "yellow", "score"]
mauve <- data[data$colour == "mauve", "score"]
hist(yellow)
hist(mauve)
t.test(yellow, mauve)$p.value

# Do the simulation again
same_group <- c()
different_group <- c()
for(i in 1:100000){
  sample_index <- sample(1:nrow(data), 2, replace = F)
  sample1 <- data[sample_index[1],]
  sample2 <- data[sample_index[2],]
  score_diff <- abs(sample1$score - sample2$score)
  if (sample1$colour == sample2$colour){
    same_group <- c(same_group, score_diff)
  }
  else{
    different_group <- c(different_group, score_diff)
  }
}

class_result <- c(rep("same group", length(same_group)), 
                  rep("different group", length(different_group)))
score_result <- c(same_group, different_group)
result <- data.frame("group" = class_result, "difference" = score_result)
ggplot(result, aes(x = factor(group, levels = c("same group", "different group")), 
                   y = difference)) +
  geom_boxplot(aes(fill = group)) +
  labs(x = NULL)

# Run a test to find out!
hist(same_group)
hist(different_group)
## The p-value is small enough, therefore, we can not accept H0 hypothesis.
wilcox.test(same_group, different_group)$p.value
