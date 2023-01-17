fieldA <- c(10.2, 10.7, 15.5,10.4, 9.9, 10.0, 16.6, 15.1, 15.2, 13.8, 14.1, 11.4, 11.5, 11.0)
fieldB <- c(8.1, 8.5, 8.4, 7.3, 8.0, 7.1, 13.9, 12.2, 13.4, 11.3, 12.6, 12.6, 12.7, 12.4, 11.3, 12.5)
var.test(fieldA, fieldB)
t.test(fieldA, fieldB, var.equal = T, alternative = "greater")

data <- read.table("ADS_practical/mice_weights.txt", header = T, sep = ",")
var.test(data$before, data$after)
t.test(data$before, data$after, var.equal = T, paired = T)
