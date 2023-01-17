# Week 11: Practical. 
# Xianghua LI. 2021/11/18
# Modified based on Chaochen WANG 2019 code for the same lesson. 

library(ggplot2) # in case that you want to play with it. 
library(dplyr) 

#### Task 1.The effort of Vitamin C on toothgrowth in pig.
data("ToothGrowth")
# let's look at the data first
? ToothGrowth
head(ToothGrowth)
summary(ToothGrowth)


# 1.1 with VC, is the tooth length different from 8.5? 

t.test(ToothGrowth$len, mu=8.5)
## Which type of t.test did we perform? 
## What is your conclusion? 


# 1.2 does the delivery method matter? 
# There are two types of the delivery methods VC and OJ. 
# This is a two-sample t-test. We need to decide whether we should set the var.equal TRUE or FALSE. 
var.test(len ~ supp, data= ToothGrowth) 
t.test(len ~ supp, data = ToothGrowth, var.equal =T)

##### What if we divide them to dosage groups? 

TG <- filter(ToothGrowth, dose == 0.5) # change the dose group and see the difference
var.test(len ~ supp, data= TG)
t.test(len ~ supp, data = TG, var.equal =T)

TG <- filter(ToothGrowth, dose == 1) # change the dose group and see the difference
var.test(len ~ supp, data= TG)
t.test(len ~ supp, data = TG, var.equal =T)

TG <- filter(ToothGrowth, dose == 2) # change the dose group and see the difference
var.test(len ~ supp, data= TG)
t.test(len ~ supp, data = TG, var.equal =T)

#### Task 2. 
data("iris")
?iris
table(iris$Species)

var.test( Sepal.Length ~ Species,data=iris[iris$Species%in% c('setosa', 'versicolor'), ])

t.test(Sepal.Length ~ Species, data=iris[iris$Species%in% c('setosa', 'versicolor'), ],var.equal = FALSE)


#### Task 3. The treatment on blood pressure
bp <- read.table ("~/ADS2_9/blood_pressure.txt",header = T,row.names = 1, sep='\t')
head(bp)
t.test(bp$bp_before,bp$bp_after,paired = T)

#### Optional task 4. Building our own t.test 

### 4. 1.	One sample t-test. The input includes a numeric vector X and a theoretical mean.  
one_sample_t_2_tail <- function (x, mu){
  n=length(x)
  var=sqrt((1/(n-1))*sum((x-mean(x))^2))
  t.value <- (mean(x)-mu)/var*sqrt(n)
  p.value <- 2*pt(-abs(t.value), df=length(x)-1)
  return(list("t_val"= t.value, "p.val" = p.value))
}  
# let's test 
x= c(1,2,3,4)
one_sample_t_2_tail(x, 2)
# let's compare to the R built-in t.test
t.test(x, mu=2)


### 4. 2.	Two-sample independent t-test of two numeric vectors X and Y. 
two_sample_t_2_tail <- function (x, y, equal_var){ 
  
  if (equal_var==1) { # equal variance assumption, student t-test 
    dfx=length(x)-1
    dfy=length(y)-1
    dftotal=dfx+dfy
    var.pool=sqrt(((dfx/dftotal)*(sum((x-mean(x))^2)/(dfx)))+((dfy/dftotal)*(sum((y-mean(y))^2)/(dfy))))
    var.difference=sqrt((var.pool^2/length(x))+(var.pool^2/length(y)))
    t.value <- (mean(x)-mean(y))/var.difference
    p.value <- 2*pt(-abs(t.value), df=length(x) + length(y) -2) 
    dftotal=dfx+dfy
    
  }  else if (equal_var==0) { # not equal variance , welsh t-test
    t.value <- (mean(x)-mean(y))/sqrt(var(x)/length(x)+var(y)/length(y))
    df = round((var(x)/length(x) + var(y)/length(y))^2/(var(x)^2/length(x)^2/(length(x)-1) +var(y)^2/length(y)^2/(length(y)-1)))
    p.value <- 2*pt(-abs(t.value), df=df) #two-tailed
  }
  
  return(list("t_val"= t.value, "p.val" = p.value))
}  

# let's test
x= c(1,2,3,4) 
y= c(1,2,3,4,5, 0)
var.test(x,y) # equal var 
two_sample_t_2_tail(x,y, 1)
# built-in t-test
t.test(x, y)

y2= c(0.01,4,5,100 )
var.test(x, y2)
two_sample_t_2_tail(x,y2, 0)
t.test(x, y2, var.equal = FALSE)

### 4. 3.	Paired sample t-test of two numeric vectors X and Y. 

paired_sample_t_2_tail <- function (x, y){
  if (length(x)!= length(y)) {
    return('Error: Lengths of the two vectors are NOT the same.')
  } else {
    d <- x - y
    n=length(d)
    var=sqrt((1/(n-1))*sum((d-mean(d))^2))
    t.value <- (mean(d))/var*sqrt(n)
    p.value <- 2*pt(-abs(t.value), df=length(x)-1) #two-tailed
    return(list("t_val"= t.value, "p.val" = p.value))
  }
}  
# test
paired_sample_t_2_tail(x, y2)
t.test(x, y2, paired = TRUE)
paired_sample_t_2_tail(x, y)
