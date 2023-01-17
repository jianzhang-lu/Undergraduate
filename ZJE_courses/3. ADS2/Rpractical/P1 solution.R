#### ADS2 Practical 1 sample solution




### Heights of students in a virtual classroom

## Can you "create" a group of 100 people with this property in R?
student=c(rnorm(55,158.5,6),rnorm(45,172,7))

## How can you verify whether you did this (approximately) correctly?
# Compare the results below to the pre-defined means and sds in the question
# because the numbers you have generated are totally random
# the results you got might not be identical to those in the question
# as long as they are not hugely different then you are approximately correct
mean(student[1:55]);sd(student[1:55]) # female group
mean(student[56:100]);sd(student[56:100]) # male group

## Draw box plots (place the two groups on the same plot)
df=data.frame('student'=student,'gender'=rep(c('female','male'),times=c(55,45)))
boxplot(df$student~df$gender,xlab='Gender',ylab='Student height',main='Male height VS Female height')

## How tall is the tallest student in your simulated class? How tall is the shortest student? How many
## students are taller than you are?
max(df$student);min(df$student) # tallest and shortest
length(which(df$student>177)) #  which() will give you a location vector of the students who are taller than you




### Revisiting the birthday problem

## Write a command that creates a group of 26 students, and assigns a day of the year to each of them as
## their birthday
bday=sample(365,26,replace=T)

## Are there shared birthdays in this group? How could you find out?
length(bday)-length(unique(bday)) # unique() will give you a new vector which only contains non-duplicated elements from the original vector

## This gives you an answer for your particular group of students, but how would you go about computing
## the overall probability of a shared birthday for n=26
# replicate the sampling process for 1000 times and combine the data as a matrix
# apply() is very similar to the 'for' loop, margin=2 means we apply a function (calculation) for each column in the matrix
# mean() will calculate the average of a vector, hence the overall probability for n=26 groups
# %>% is a pipe operator, it will pass the previous result to the next command
library(tidyverse)
replicate(n=1000,sample(365,26,replace=T)) %>%
 apply(MARGIN=2,function(x) (length(x)-length(unique(x)))/26) %>% mean()

## How about computing and plotting the probabilities of shared birthdays
## from n=1 to n=50
prob=lapply(1:50,function(i) sample(365,i,replace=T)) %>% 
 lapply(function(x) (length(x)-length(unique(x)))/length(x)) %>%
 unlist()
plot(1:50,prob,xlab='Class size',ylab='probability of a shared birthday',
     main='Birthday problem')

