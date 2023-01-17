library(tidyverse)

# Q1
data <- ToothGrowth
summary(data)
## a
p1 <- t.test(data$len, mu = 8.5, alternative = "two.sided")$p.value

## b
var.test(data = data, data$len~data$supp)
p2 <- t.test(data$len~data$supp, var.equal = T)$p.value
dose0.5 <- data[data$dose == 0.5, ]
dose2 <- data[data$dose == 2, ]
dose1 <- data[data$dose == 1, ]
var.test(data = dose0.5, len ~ supp)$p.value
var.test(data = dose1, len ~ supp)$p.value
var.test(data = dose2, len ~ supp)$p.value
p3 <- t.test(dose0.5$len ~ dose0.5$supp)$p.value
p4 <- t.test(dose1$len ~ dose1$supp)$p.value
p5 <- t.test(dose2$len ~ dose2$supp)$p.value


# Q2

data2 <- iris
subdata_v <- filter(iris, iris$Species == "versicolor")
subdata_s <- filter(iris, iris$Species == "setosa")
var.test(subdata_s$Petal.Length, subdata_v$Petal.Length)
p6 <- t.test(subdata_s$Petal.Length, subdata_v$Petal.Length, var.equal = F)$p.value

# Q3
setwd("D:/R文件/ADS_practical/")
data3 <- read.table("blood_pressure.txt", header = T)
p7 <- t.test(data3$bp_before, data3$bp_after, paired = T)$p.value


