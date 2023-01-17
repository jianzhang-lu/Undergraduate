library(tidyverse)
library(ggpmisc)

# 1. Simple Regression
pressure <-  read.csv("IBMS3_workshop/W3_ANOVA/pressure.csv")
ggplot(pressure, aes(x = Weight, y = Response)) +
  geom_point(aes(color = Sex))

model <- lm(Response ~ Weight, data = pressure)
summary(model) # Response = -0.65 * Weight + 11.78 + error
confint(model)
ggplot(pressure, aes(x = Weight, y = Response)) +
  geom_smooth(method = 'lm', formula = y~x, se = T) +
  geom_point() +
  stat_poly_eq(aes(label = paste(..eq.label.., 
                                 ..adj.rr.label.., 
                                 sep = '~~~~')),
               color = 'red',
               label.x = 100,
               formula = y~x,
               parse = T,
               geom = 'label')

# 2. Multiple Regression
model.2 <- lm(Response ~ Weight + Age, data = pressure)

## Check the assumptions of the model by using diagnostic plots.
## 1. Residuals are normally distributed.
plot(model.2, 2, pch = 20)
## 2. Errors are independent and homoscedasticity.
plot(model.2, 1, pch = 20, lwd = 2)

summary(model.2)
confint(model.2)
anova(model.2)

# 3. Qualitative predictors and dummy variables
ggplot(pressure, aes(x = Weight, y = Response)) +
  geom_boxplot(aes(fill = Sex))
model.3 <- lm(Response ~ Weight + Age + Sex, data = pressure)
summary(model.3)
predict(model.3, data.frame(Weight = 82, Age = 50, Sex = 'M'))

# 4. Choosing a model
anova(model, model.2)
anova(model.2, model.3)
drop1(model.3, test = "F")

# 5. Interactions between factors
foxes <- read.csv("IBMS3_workshop/W3_ANOVA/fox.csv")
foxes$RodentAvail <- factor(foxes$RodentAvail, levels = c("Low", "Medium", "High"))

ggplot(foxes, aes(Age, LitterSize)) +
  geom_point()

ggplot(foxes, aes(RodentAvail, LitterSize)) +
  geom_boxplot(outlier.color = 'red') +
  geom_jitter(width = 0.1)

ggplot(foxes, aes(Location, LitterSize)) +
  geom_boxplot(outlier.color = 'red') +
  geom_jitter(width = 0.1)

model <- lm(LitterSize ~ Age + Location + RodentAvail, data = foxes)
summary(model)

foxes <- unite(foxes, RodentAvail, Location, col = 'combine', sep = ' ', remove = F)
ggplot(foxes, aes(combine, LitterSize)) +
  geom_boxplot()

ggplot(foxes, aes(RodentAvail, LitterSize)) +
  geom_boxplot(aes(fill = Location))

model.2 <- lm(LitterSize ~ Age + Location + RodentAvail + RodentAvail:Location, data = foxes)
model.2 <- lm(LitterSize ~ Age + Location * RodentAvail, data = foxes)
summary(model.2)
anova(model, model.2)

## Interaction plots
library(emmeans)
par(mar = c(4, 4, 1, 4), cex = 0.5, cex.lab = 1, cex.axis = 1)
emmip(model.2, RodentAvail ~ Location)
emmip(model.2, Location ~ RodentAvail)

## In different levels of Rodent-Avail, 
## the comparison between coastal and inland.
marginals <- emmeans(model.2, ~ Location * RodentAvail)
pairs(marginals, by = "RodentAvail")
pairs(marginals, by = "Location")

## All possible comparisons
marginals_all <- emmeans(model.2, pairwise ~ Location * RodentAvail)


# 6. Finally test
neuron <- read.csv("IBMS3_workshop/W3_ANOVA/nerveConduction.csv")
ggplot(neuron, aes(Diameter, Velocity)) +
  geom_point(aes(color = Myelination))

ggplot(neuron, aes(Diameter, Velocity)) +
  geom_boxplot(aes(fill = Myelination))

ggplot(neuron, aes(Myelination, Velocity)) +
  geom_boxplot(aes(fill = Sex))

ggplot(neuron, aes(Sex, Velocity)) +
  geom_boxplot(aes(fill = Sex))

model.1 <- lm(Velocity ~ Diameter + Myelination, data = neuron)
summary(model.1)

model.2 <- lm(Velocity ~ Sex + Diameter + Myelination, data = neuron)
summary(model.2)
anova(model.1, model.2) # Model.2 is not good

model.3 <- lm(Velocity ~ Myelination * Diameter, data = neuron)
summary(model.3)
anova(model.1, model.3) # Model.3 is better

model.4 <- lm(Velocity ~ Myelination * Sex + Diameter, data = neuron)
summary(model.4)
emmip(model.4, Myelination ~ Sex) # Interactions are not obvious

# Model5: Ignore the main effect
model.5 <- lm(Velocity ~ Myelination : Diameter, data = neuron)
summary(model.5)
anova(model.3, model.5)
