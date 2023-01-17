library(tidyverse)
data <- read.csv("D:/R_document/ADS_practical/drug_trial.csv")

# Do the test before ANOVA
## Test the normality of residuals
model <- aov(data = data, pain~treatment)
shapiro.test(resid(model))$p.value ### p = 0.42, normally distributed.

## Test the equality of variances
plot(model, 1) ### The heights of each columns are similar.

# Run the ANOVA
summary(model) ### The p-value is less than 0.05. HA is true.

# Run the post-hoc test
TukeyHSD(model) ## A-B, placebo-B have significant differences.

mouse <- read.csv("D:/R_document/ADS_practical/mouse_experiment.csv")
ggplot(mouse, aes(x = genotype, y = weight_gain)) +
  geom_boxplot(aes(fill = diet)) +
  labs(y = "weight gain in g")

model2 <- aov(data = mouse, weight_gain~diet*genotype)
shapiro.test(resid(model2))$p.value
plot(model2, 1)
summary(model2)
# The interaction p-value is 0.003, so we choose interactive ANOVA is right.
# Both the genotype and the diet have impacts on the weight
TukeyHSD(model2)
