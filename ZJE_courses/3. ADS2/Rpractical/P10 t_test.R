library(tidyverse)
temp <- read.csv("ADS_practical/OrionTemp.csv")
summary(temp)
sample <- sample(temp$Temperature, 10, replace = F)
t.test(sample, mu = 37, alternative = "two.sided")

# formula (two-sides)
ts <- (mean(sample)-37)/(sd(sample)/sqrt(10))
p_value <- pt(ts, df = 9, lower.tail = T)*2

xlab <- seq(-10,10,1)
ylab <- dt(xlab, df = 9)
data <- data.frame("x" = xlab, "y" = ylab)
ggplot(data, aes(x,y)) +
  geom_smooth(stat = "identity")
pt(c(-10,10), df = 9)

mul_sample <- function() {
  sample_one <- sample(temp$Temperature, 10, replace = F)
  result <- t.test(sample_one, mu = 37, alternative = "two.sided")$p.value
  return(result)
}

rrr <- replicate(5, mul_sample())

# simulation

count_result <- c()
for(i in 1:500) {
  set_pvalue <- replicate(i, mul_sample())
  count <- sum(set_pvalue <= 0.05)
  count_result <- c(count_result, count)
}


data4 <- data.frame("Number" = 1:500, "Num" = count_result)
ggplot(data4, aes(x=Number, y=Num)) +
  geom_point() +
  geom_smooth()


# Finally
mul_sample <- function() {
  sample_one <- sample(temp$Temperature, 10, replace = F)
  result <- t.test(sample_one, mu = 37, alternative = "two.sided")$p.value
  return(result)
}


finally_set <- c()
for (i in 5:100){
  p_value = c()
  for (j in 1:100){
    sample_one2 <- sample(temp$Temperature, i, replace = F)
    result2 <- t.test(sample_one2, mu = 37, alternative = "two.sided")$p.value
    p_value <- c(p_value, result2)
  }
  finally <- sum(p_value <= 0.05)/100
  finally_set <- c(finally_set, finally)
}

plot(finally_set)