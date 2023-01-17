library(tidyverse)
library(modelr)
library(ggpubr)
library(corrplot)

data <- heights
# Converting height from inches to cm
data$height <- heights$height * 2.54

# Converting weight from pounds to kg
data$weight <- heights$weight * 0.453592
head(data, 4)
data <- na.omit(data)

# Use plots to visualize the data
ggplot(data) +
  geom_point(aes(x = weight, y = height)) +
  labs(x = "weight in kg", y = "height in cm")

# Pearson’s correlation coefficient
cor(data$height, data$weight)
cor.test(data$height, data$weight)

# Test each of the assumptions for this data
model <- lm(data$weight ~ data$height)
plot(model, 2)
plot(model, 1)
resid(model)
residuals(model)
hist(resid(model))

# Intepret the result
summary(model)

# Plot the data
## ggscatter
ggscatter(data, x = "weight", y = "height", add = "reg.line",
          add.params = list(color = "blue", fill = "lightgray"),
          conf.int = T) +
  labs(x = "weight in (kg)", y = "height in (cm)")

## corrplot
corrplot(cor(data[,-c(5,6)]), order = "AOE",
         method = "ellipse", type = "upper", tl.pos = "d")
corrplot(cor(data[,-c(5,6)]), order = "AOE", add = T,
         method = "number", type = "lower", tl.pos = "n", diag = F)

corrplot(cor(data[,-c(5,6)]), order = "AOE", method = "color", 
         addCoef.col = "black", type = "upper", col = rev(COL2("RdBu",200)))

## outliers
cooksd <- cooks.distance(model)
plot(cooksd, pch = "*", cex = 2, main = "Influential outliers by Cook's distance",
     ylab = "Cook's distance")
abline(h = 4/nrow(data), col = "red")
