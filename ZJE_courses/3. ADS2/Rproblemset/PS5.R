library (tidyverse)
roll <- function(x){
  roll_data <- replicate(n = 1000, sum(sample(6, x, replace = T)))
  hist(roll_data, main = c("Sample size ", x), 
       xlab = "data")
  sum_of_1sd <- sum(roll_data < mean(roll_data) + sd(roll_data) &
                      roll_data > mean(roll_data) - sd(roll_data))
  prob_of_1sd <- sum_of_1sd/1000 
  
  sum_of_2sd <- sum(roll_data < mean(roll_data) + 2*sd(roll_data) &
                      roll_data > mean(roll_data) - 2*sd(roll_data))
  prob_of_2sd <- sum_of_2sd/1000
  
  sum_of_3sd <- sum(roll_data < mean(roll_data) + 3*sd(roll_data) &
                      roll_data > mean(roll_data) - 3*sd(roll_data))
  prob_of_3sd <- sum_of_3sd/1000
  result <- c(prob_of_1sd, prob_of_2sd, prob_of_3sd)
  return (result)
}
result3 <- roll(3)
result4 <- roll(4)
result5 <- roll(5)

##########################################################################

BeanMachine <- function(number, layers){
  a <- replicate(number, sum(sample(c(0, 1), layers, replace = T)))
  return (a)
} # 0代表向左，1代表向右。可能出现的值：0 1 2 3 4 5 6 7 8

BeanMachine2 <- function(number, layers){
  a <- replicate(number, sum(sample(c(0, 0, 0, 0, 1), layers, replace = T)))
  return (a)
}
result <- BeanMachine(1000, 8)
result2 <- BeanMachine2(1000, 8)

hist(result, main = "BeanMachine", xlab = "position", xlim = c(0,8),
     ylim = c(0,300), breaks = seq(-0.5 ,8.5 ,1), col = "skyblue")

hist(result2, main = "BeanMachine2", xlab = "position", xlim = c(0,8),
     ylim = c(0,400), breaks = seq(-0.5 ,8.5 ,1), col = "skyblue")


result_frame <- data.frame("result" = result)
result_frame2 <- data.frame("result" = result2)

ggplot(result_frame, aes(x = result)) +
  geom_bar(fill = "skyblue") +
  labs(title = "BeanMachine", x = "position") +
  scale_x_continuous(breaks = seq(0,8,1))

ggplot(result_frame2, aes(x = result)) +
  geom_bar(fill = "skyblue") +
  labs(title = "BeanMachine2", x = "position") +
  scale_x_continuous(breaks = seq(0,8,1))

