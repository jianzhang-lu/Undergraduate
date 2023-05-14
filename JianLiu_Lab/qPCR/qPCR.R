library(tidyverse)
library(ggsignif)
library(ggpubr)

# 1. 预处理
data <- read.csv("Lab/qPCR/qPCR_SRTP.csv", sep = '\t')
colnames(data)[3] <- "18S"
data$Group <- factor(data$Group, levels = c("gControl", "gSMAD4"))

## 两种内参分别处理
data <- na.omit(data[, c(1, 3, 4)])

# 2. 先分别取control和treatment组的内参
control <- filter(data, Group == 'gControl')
exper <- filter(data, Group == 'gSMAD4')
control_internal <- control$`18S`
exper_internal <- exper$`18S`

# 3. 计算δCT: 目的基因CT值-对应的内参CT值
control$AIM2 <- control$AIM2 - control_internal
exper$AIM2 <- exper$AIM2 - exper_internal

# 4. 计算2^-δCT
control$AIM2 <- 2^(-control$AIM2)
exper$AIM2 <- 2^(-exper$AIM2)

# 5. 对照组2^-δCT取均值得到mean 2^-δCT
mean_delta_CT <- mean(control$AIM2)

# 6. 计算δδCT: 每一个2^-δCT / mean 2^-δCT
control$AIM2 <- control$AIM2/mean_delta_CT
exper$AIM2 <- exper$AIM2/mean_delta_CT

# 7. 整理成最后的data并计算SE
data_final <- data.frame('value' = c(control$AIM2, exper$AIM2),
                         'group' = rep(c('gControl', 'gSMAD4'), each = 5))

ggbarplot(data_final, x = "group", y = "value", 
          add = "mean_se", width = 0.5,
          color = "group", fill = "group", palette = "npg",
          position = position_dodge(0.1)) +
  scale_y_continuous(breaks = seq(0, 10, 1)) +
  stat_compare_means(method = "t.test", label.x = 0.6, label.y = 8, size = 6) +
  labs(title = '18S as internal control') +
  theme(legend.position = "right", 
        plot.title = element_text(hjust = 0.5, size = 20))
  

