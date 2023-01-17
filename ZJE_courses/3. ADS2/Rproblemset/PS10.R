library(tidyverse)

weight <- read.table("ADS_practical/barley.txt", sep = "\n", header = F)
weight <- weight$V1

t.test(weight, mu = 50, alternative = "less")
hist(weight, breaks = 20, xlab = "weight")

cal <- function(vector){
  res <- t.test(vector, mu = 50, alternative = "two.sided")$p.value
  return(res <= 0.05)
}

result_set <- c()
for (i in 2:50){
  weight_new <- replicate(10000, sample(weight, i, replace = F))
  result <- mean(apply(weight_new, 2, cal))
  result_set <- c(result_set, result)
}

min(which(result_set == 1))
finally <- data.frame("number" = 2:50, "result" = result_set)
