library(tidyverse)

# Question 1.

a <- replicate(10000, mean(runif(26, 0, 100)))
mean(a < 40)
index <- seq(1, 10000)
data <- data.frame("index" = index, "mean" = a)

ggplot(data, aes(x = mean, y = ..density..)) +
  geom_point(size = 1, stat = "density") +
  labs(x = "mean")

ggplot(data, aes(mean))+
  geom_freqpoly()

ggplot(data, aes(mean))+
  geom_density()

hist(data$mean, xlab = "mean")

# Question 2

b <- replicate(10000, mean(runif(26, 0, 80)))
mean(b > a)
names(data)[2] = "a_mean"
data$b_mean = b
ggplot(data) +
  geom_density(aes(x = a_mean), color = "red") +
  geom_density(aes(x = b_mean), color = "blue") +
  labs(x = "mean")

# Question 3

score <- pnorm(64, mean = 50, sd = 10)*100

q_score <- function(score){
  return(pnorm(score, 50, 10)*100)
}

Lscore = c(64, 63, 62, 59)
Sscore = c(70, 63, 61, 56)
Lscore_new <- q_score(Lscore)
Sscore_new <- q_score(Sscore)
mean(Lscore_new)
mean(Sscore_new)

all_score <- c(Lscore_new, Sscore_new)
data3 <- data.frame("score" = all_score, "group" = rep(c("L", "S"), c(4, 4)))
ggplot(data3) +
  geom_boxplot(aes(x = factor(group), y = score, fill = group)) +
  labs(x = "group")

# Question 4


unlucky <- q_score(replicate(1, rnorm(26, 40, 8)))
data4 <- apply(unlucky, 2, mean)

lucky <- q_score(replicate(9999, rnorm(26, 50, 10)))
data5 <- apply(lucky, 2, mean)
mean(data4 > data5)

min <- min(data5)
mean(data4 < min)


# 其他任意一个班级的得分信息(mean)
varies <- function(size) {
  new_score <- rnorm(size, 50, 10) %>% q_score ()
  return(mean(new_score))
}

simulate <- function(){
  score_pool <- replicate(9999, varies(sample(c(5:40), 1)))
  unlucky_score <- mean(q_score(rnorm(sample(c(5:40), 1), 40, 8)))
  return(unlucky_score < min(score_pool))
}

result <- mean(replicate(10000, simulate()))

