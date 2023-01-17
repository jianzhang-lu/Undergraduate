# 1 Remember R ?

library(tidyverse)

## 1.1 read the csv file
chicago <- read.csv("D:/R文件/ADS_practical/Chicago2013.csv")

## 1.2 examine the data
head(chicago)
chicago[1:5 , 2]
filter(chicago, Country == "MEX")
chicago[chicago$Country == "MEX", ]
chicago[chicago$Age >= 50,]

## 1.3 tell what countries the athletes are from and how many there are
##     from each country?

table(chicago$Country)

chicago %>% group_by(Country) %>%
  summarize(number = n())

chicago %>% 
  count(Country)

count(chicago, Country)

## 1.4 draw a histogram of finishing times
ggplot(data = chicago, aes(x = Time)) +
  geom_histogram(color = "green", fill = "red") +
  labs(
    title = "histogram use ggplot",
    x = "times(/h)")

hist(chicago$Time, main = "histogram use normal method", xlab = "time/h", col = "green", breaks = 20)

## 1.5 Select 10 people at random from the dataset 
##  and draw a histogram of their finishing times
random_number <- sample(nrow(chicago), 10, replace = F)
chicago2 <- chicago[random_number, ]
hist(chicago$Time, main = "histogram2 use normal method", xlab = "time/h", col = "green", breaks = 20)

# 2 Heights of students in a virtual classroom

## 2.1 create a group of 100 people with this property in R
men_height <- rnorm(45, mean = 172, sd = 7)
women_height <- rnorm(55, 158.5, 6)
group <- c(men_height, women_height)
data1 <- data.frame(height = men_height, sex = "man")
data2 <- data.frame(height = women_height, sex = "women")
data <- rbind(data1, data2)
boxplot(data$height ~ data$sex)
ggplot (data, aes(x = sex, y = height))+
  geom_boxplot()

## 2.2 draw box plots of the men and the women
all_men_height <- tibble(men = men_height)
all_women_height <- tibble(women = women_height)
ggplot(data = all_men_height, aes(y = men)) +
 geom_boxplot(color = "blue", fill = "red") +
  labs(title = "the boxplot of men height")

ggplot(data = all_women_height, aes(y = women)) +
  geom_boxplot(color = "blue", fill = "red") +
  labs(title = "the boxplot of women height")

boxplot(men_height, col = "green", main = "the boxplot of men height")
boxplot(women_height, col = "red", main = "the boxplot of women height") 

## 2.3 How tall is the tallest student in your simulated class? 
##     How tall is the shortest student? 
##     How many students are taller than you are?(my height is about 172.3cm)

tallest <- max(group)
shortest <- min(group)
length(group[group > 172.3])

# 3 Birthday problem

## 3.1 Write a command that creates a group of 26 students, 
##    and assigns a day of the year to each of them as their birthday.
students_number <- c(1:26)
birthday <- sample(1:365, 26, replace = T)
birthday_list <- data.frame(students_number = students_number, birthday = birthday)

## 3.2 Are there shared birthdays in this group?
length(birthday)  # 26
length(unique(birthday))  # 25 

## 3.3 how would you go about computing
##     the overall probability of a shared birthday for n=26?

count = 0
for (i in 1:10000){
  birthday <- sample(1:365, 26, replace = T)
  if (length(birthday) != length(unique(birthday))){
    count = count + 1
  }
}
probability_for_26 <- count/10000

## (bonus) 3.4 How about computing and plotting the probabilities of shared birthdays
##            from n=1 to n=50?

probability_ideal <- function(n){
  p_different_ideal <- prod((366 - n) : 365)/365 ^ n
  p_ideal <- 1 - p_different_ideal
  return(p_ideal)
}
size <- c(1:50)
probability_of_birthday_ideal <- data.frame(size = size, p_ideal = 0)
for (i in 1:50){
    probability_of_birthday_ideal[i, 2] = probability_ideal(i)
}
plot(x = probability_of_birthday_ideal$size, 
     y = probability_of_birthday_ideal$p,
     main = "Birthday problem (ideal)", 
     xlab = "class size", 
     ylab = "probability of a shared birthday")


probability_estimated <- function(n){
  count = 0
  for (i in 1:10000){
    birthday_estimated <- sample(1:365, n, replace = T)
    if (length(birthday_estimated) != length(unique(birthday_estimated))){
      count = count + 1
    }
  }
  p_estimated <- count/10000
}
size2 <- c(1:50)
probability_of_birthday_estimated <- data.frame(size = size2, p_estimated = 0)
for (i in 1:50){
  probability_of_birthday_estimated[i, 2] = probability_estimated(i)
}
plot(x = probability_of_birthday_estimated$size, 
     y = probability_of_birthday_estimated$p,
     main = "Birthday problem (estimated)", 
     xlab = "class size", 
     ylab = "probability of a shared birthday")


