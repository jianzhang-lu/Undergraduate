# This R code is by Xianghua Li for ADS2 Week 10 practicals, modified from Chaochen Wang 2019 code. 
set.seed(10000) # this way, we could replicate the random generation of the points. 

##question 1
#1.1
ps.10 <- replicate(1e5, t.test(rnorm(10,178,10), mu=175, alternative = "greater")$p.value) 
# in the code above, 
# Step1:(rnorm) Generating a normal distribution, with 10 (n) values with the mean= 178 (mu), with the standard deviation of 10 (sd).  
# Step2:(t.test) performing the one-sample, one-tail t-test, comparing the mean of these values with 175, and returning the p.value. 
# Step3:(replicate) Doing Step1 & Step2 1e5 (100,000) times. This takes quite a while and storing all the p values in a vector.   

beta.10 <- mean(ps.10 > 0.05) # this is beta value: Type II errors where it incorrectly accepted the null hypothesis. 
power.10 <- 1- beta.10 # This is our power

#1.2
ps.50 <- replicate(1e5, t.test(rnorm(50,178,10), mu=175, alternative = "greater")$p.value) # we only need to change the 'n'
beta.50 <- mean(ps.50 > 0.05)
power.50 <- 1- beta.50

#1.3
power.t.test(n=10, delta = 3, sd =10, sig.level = 0.05, type = "one.sample", alternative = "one.sided")
power.t.test(n=50, delta = 3, sd =10, sig.level = 0.05, type = "one.sample", alternative = "one.sided")

Ns <- seq(5, 100, by = 5)# simulate different sample sizes
Pows <- c() # Create a vector to store the powers

for (n in Ns) { # for each n value, calculating power and storing. This is a loop-structure. 
  power <- power.t.test(n=n, delta = 3, sd =10, sig.level = 0.05, type = "one.sample", alternative = "one.sided")$power
  Pows <- c(Pows, power)
}
plot(Ns, Pows, type = "b")

## question 2
#2.1
ps.drug <- replicate(1e5, t.test(rnorm(10, 130, 30), rnorm(10, 117, 30), alternative = "great")$p.value) 
# As in the practice 1.1, 
# Step1:(rnorm) Generating a normal distribution, but this time with two groups. Each group with the same number of values, and the same sd, but different mu. 
# Step2:(t.test) performing the two-sample, one-tail t-test, and returning the p.value. 
# Step3:(replicate) Doing Step1 & Step2 1e5 (100,000) times. This takes quite a while and storing all the p values in a vector.   


beta.drug <- length(which(ps.drug > 0.05))/length(ps.drug)
power.drug <- 1- beta.drug # simulation-based. 
power.t.test(n=10, delta = 13, sd =30, sig.level = 0.05, type = "two.sample", alternative = "one.sided") # R function-based. 

#2.2
power.t.test(delta = 13, sd =30, sig.level = 0.05, power=0.8, type = "two.sample", alternative = "one.sided")
#2.3
power.t.test(delta = 13, sd =30, sig.level = 0.05, power=0.8, type = "paired", alternative = "one.sided")
#2.4
alphas <- seq(0.01, 0.05, by=0.01)
Ns <- c()
for (alpha in alphas) {
  n <- power.t.test(delta = 13, sd =30, sig.level = alpha, power=0.8, type = "paired", alternative = "one.sided")$n
  Ns <- c(Ns, n)
}
plot(alphas, Ns, type="b")

Pows <- seq(0.5, 0.9, by=0.05)
Ns <- c()
for (pow in Pows){
  n <- power.t.test(delta = 13, sd =30, sig.level = 0.05, power=pow, type = "paired", alternative = "one.sided")$n
  Ns <- c(Ns, n)
  
}
plot(Pows, Ns, type = "b")
