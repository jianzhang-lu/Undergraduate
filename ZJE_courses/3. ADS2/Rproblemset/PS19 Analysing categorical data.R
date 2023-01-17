library(tidyverse)

# 1
favorite <- c(40, 32, 48, 57, 23)
chisq.test(favorite, p = rep(0.2, 5))
## The p_value is 0.001, so we reject H0, the company should not produce the 
## same amount of ice cream with different flavours.

# 2
## H0: There is no difference about people's favorite among different flavours.
X <- replicate(n = 5, rnorm(10000, 0, 1), simplify = T)
X_square <- X^2
sum <- apply(X_square, 1, sum)
chi_square <- (32-40)^2/32 + (32-40)^2/48 + (57-40)^2/57 + (23-40)^2/23
p_sim <- mean(sum >= chi_square)
p_real <- chisq.test(favorite)$p.value

# 3 
## df = 4
random <- rchisq(10000, 4)
plot(density(random), main = "The distribution of chi-square with df=4")

# 4, 5
WT_matrix <- matrix(c(40,34,9,7), nrow = 2, byrow = T)
                    
KO_matrix <- matrix(c(20,25,15,20), nrow = 2, byrow = T)
                  
data <- array(c(WT_matrix, KO_matrix), dim = c(2,2,2),
              dimnames = list(c("Alive", "Dead"), 
                              c("Male", "Female"), 
                              c("WT", "KO")))
print(data)

# 6
summary(as.table(data))

# 7
## Redesign the data.
data_new <- data.frame("operation" = rep(c("WT", "KO"), each = 4),
                       "gender" = rep(c("Male", "Female"), each = 2, 2),
                       "situation" = rep(c("Alive", "Dead"), 4),
                       "number" = c(40, 9, 34, 7, 20, 15, 25, 20))
ggplot(data_new, aes(x = gender, y = number)) +
  geom_point(aes(color = operation, size = situation))

ggplot(data_new, aes(x = gender, y = number)) + 
  geom_bar(stat = "identity", position = "dodge", aes(fill = operation)) +
  facet_grid(.~situation)

ggplot(data_new, aes(x = situation, y = number)) +
  geom_point(aes(color = situation), size = 2) +
  facet_grid(operation~gender)

# Additional exercise
## H0: The survival of mice is independent on geneX and sex.
## Reshape the data. (WT, Male) as A; (WT, Female) as B; (KO, Male) as C; (KO, Female) as D.
new_data2 <- matrix(c(40,34,20,25,9,7,15,20), nrow = 2, byrow = T, 
                    dimnames = list(c("Alive", "Dead"), c("A", "B", "C", "D")))
chisq.test(new_data2)

## Therefore, we accept HA. The survival of mice is dependent on geneX and sex.