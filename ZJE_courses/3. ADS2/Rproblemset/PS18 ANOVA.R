# Q1 Residuals are normally distributed.
mean1 <- 10
mean2 <- 15
mean3 <- 18
group1 <- mean1 + rnorm(50, mean = 0, sd = 3)
group2 <- mean2 + rnorm(50, mean = 0, sd = 4)
group3 <- mean3 + rnorm(50, mean = 0, sd = 5)

data1 <- data.frame("class" = rep(c("A", "B", "C"), each = 50), 
                    "number" = c(group1, group2, group3))
model1 <- aov(data = data1, number~class)
hist(resid(model1), main = "residuals")
shapiro.test(resid(model1))
plot(model1, 2)

group4 <- mean1 + rnorm(200, mean = 0, sd = 3)
group5 <- mean2 + rnorm(200, mean = 0, sd = 4)
group6 <- mean3 + rnorm(200, mean = 0, sd = 5)

data2 <- data.frame("class" = rep(c("A", "B", "C"), each = 200), 
                    "number" = c(group4, group5, group6))
model2 <- aov(data = data2, number~class)
hist(resid(model2), main = "residuals")
shapiro.test(resid(model2))
plot(model2, 2)

# Q2 Residuals are not normally distributed.
group7 <- mean1 + sample(1:100,50)
group8 <- mean2 + sample(1:100,50)
group9 <- mean3 + sample(1:100,50)

data3 <- data.frame("class" = rep(c("A", "B", "C"), each = 50), 
                    "number" = c(group7, group8, group9))
model3 <- aov(data = data3, number~class)
hist(resid(model3), main = "residuals")
shapiro.test(resid(model3))
plot(model3, 2)

# Q3 
mean1 <- 10
mean2 <- 15
mean3 <- 18
group1 <- mean1 + rnorm(50, mean = 0, sd = 10)
group2 <- mean2 + rnorm(50, mean = 0, sd = 10)
group3 <- mean3 + rnorm(50, mean = 0, sd = 10)

data1 <- data.frame("class" = rep(c("A", "B", "C"), each = 50), 
                    "number" = c(group1, group2, group3))
model1 <- aov(data = data1, number~class)
hist(resid(model1), main = "residuals")
shapiro.test(resid(model1))
plot(model1)

# Q4
mean1 <- 10
mean2 <- 15
mean3 <- 18
group1 <- mean1 + rnorm(50, mean = 0, sd = 5)
group2 <- mean2 + rnorm(50, mean = 0, sd = 20)
group3 <- mean3 + rnorm(50, mean = 0, sd = 30)

data1 <- data.frame("class" = rep(c("A", "B", "C"), each = 50), 
                    "number" = c(group1, group2, group3))
model1 <- aov(data = data1, number~class)
hist(resid(model1), main = "residuals")
shapiro.test(resid(model1))
plot(model1)

# Q5 Do a normal-QQ plot using model in Q4.
q_standard <- function(number, mean, sd){
  quantiles <- (number-mean)/sd
  return(quantiles)
}

plot(model1, 1)
data <- data1$number
data_group1 <- data[1:50] 
data_group2 <- data[51:100] 
data_group3 <- data[101:150] 
standardized <- c(q_standard(data_group1, 10, 5), 
                 q_standard(data_group2, 15, 20),
                 q_standard(data_group3, 18, 30))

q_theoretical <- function(num){
  final <- qnorm(seq(0.001, 0.999, length.out = num))
  return(final)
}

theoretical <- q_theoretical(150)
plot(theoretical, sort(standardized), main = "Normal Q-Q",
     ylab = "Standardized residuals", xlab = "Theoretical Quantiles")



