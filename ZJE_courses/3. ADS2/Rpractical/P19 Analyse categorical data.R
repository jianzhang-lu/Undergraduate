library(tidyverse)

# 1. Simulation of the probability of goodness-of-fit test
X <- replicate(n = 4, rnorm(1000, 0, 1), simplify = T)
X_square <- X^2
sum <- apply(X_square, 1, sum)
plot(density(sum), main = "Chi-Square Distribution", 
     ylim = c(0,0.5), xlim = c(0,8),
     xlab = "Simulation with 1000 datapoints")

X2 <- replicate(n = 4, rnorm(10000, 0, 1), simplify = T)
X2_square <- X2^2
sum2 <- apply(X2_square, 1, sum)
plot(density(sum2), main = "Chi-Square Distribution", 
     ylim = c(0,0.5), xlim = c(0,8),
     xlab = "Simulation with 10000 datapoints")

### In this case, Chi-square is 8.1.
p_value_sim <- mean(sum2 >= 8.1)
p_value_real <- chisq.test(c(13, 10, 5, 3), p = rep(0.25, 4))$p.value

# 2. Chi-square distribution and degree of freedom
df <- c(1,2,3,4,6,9)
value <- c()
for (i in 1:length(df)){
  small_value <- rchisq(10000, df[i])
  value <- c(value, small_value)
}
data <- data.frame("df" = rep(df, each = 10000), "value" = value)
ggplot(data = data, aes(x = value)) +
  geom_density(aes(color = factor(df)), size = 1)

# 3. Chi-square test of homogeneity
## Input the matrix.
data3 <- matrix(c(1,0,0,2,3,2,0,0,3,3,0,1,6,5,5,0), nrow = 4, byrow = T,
                dimnames = list(c("Severe","Mild","Sporadic","Never"),
                                c("Spring","Summer","Fall","Winter")))

rownames(data3) <- factor(rownames(data3), 
                          levels = c("Never","Sporadic","Mild","Severe"))
## Visulize the data.
barplot(data3, col = c("red", "orange", "skyblue", "green"), main = "boxplot")
legend("topright", legend = c("Severe","Mild","Sporadic","Never"), 
       fill = c("red", "orange", "skyblue", "green"), cex = 0.7, text.width = 1,
       x.intersp = 0.3, y.intersp = 0.5)

mosaicplot(t(data3), color = c("orange", "green", "orange", "green"), 
           main = "mosaics", cex.axis = 1)

newdata <- data.frame("season" = rep(c("Spring","Summer","Fall","Winter"), 4),
                      "allergy" = rep(c("Severe","Mild","Sporadic","Never"), each = 4),
                      "number" = c(1,0,0,2,3,2,0,0,3,3,0,1,6,5,5,0))

ggplot(newdata, aes(x = season, y = allergy, size = number)) +
  geom_point(shape = 21, aes(color = season, fill = season)) +
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_size_area(max_size = 15) +
  labs(title = "balloons")

## Perform chi-square test
chisq.test(data3)

# 4. Chi-square test and Fisher’s exact test
data4 <- matrix(c(7,2,3,7), nrow = 2, byrow = T,
                dimnames = list(c("Alive","Dead"), c("WT","KO")))

chisq.test(data4, correct = F)
chisq.test(data4, correct = T)
fisher.test(data4) 
wilcox.test(data3, exact = F)
fisher.test(data3)

