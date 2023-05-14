library(tidyverse)
library(lme4)
library(emmeans)

# 1. Binary data
babyfood <- read.csv("IBMS3_workshop/W5_Categorical and bounded data/babyfood.csv")
babyfood$food <- factor(babyfood$food, levels = c("Breast", "Bottle", "Mix"))
model <- glm(cbind(disease, nondisease) ~ sex + food, 
             family = binomial(link = logit),
             data = babyfood)
summary(model)
exp(confint(model))
drop1(model)

# 2. Percentages
smoking <- read.csv("IBMS3_workshop/W5_Categorical and bounded data/smoking.csv")
ggplot(smoking, aes(x = Age, y = Dead)) +
  geom_point(aes(color = Smoker)) +
  geom_line(aes(color = Smoker), linewidth = 1) +
  scale_x_continuous(breaks = seq(40, 100, 10)) +
  scale_y_continuous(limits = c(0, 100), breaks = seq(0, 100, 20))

smoking$AgeAdj <- smoking$Age - 40
model.2 <- glm(cbind(Dead, Alive) ~ AgeAdj + Smoker,
               family = binomial(link="logit"), 
               data = smoking)
summary(model.2)

pred.age <- 40:100
smokers <- list(AgeAdj = pred.age - 40,
                Smoker = rep("Y", length(pred.age)))
nonsmokers <- list(AgeAdj = pred.age - 40,
                   Smoker = rep("N", length(pred.age)))

pr.smokers <- predict(model.2, type = "response",
                      newdata = smokers) * 100
pr.nonsmoker <- predict(model.2, type = "response",
                        newdata = nonsmokers) * 100

ggplot() +
  geom_point(data = smoking, aes(x = Age, y = Dead, color = Smoker)) +
  geom_line(aes(x = pred.age, y = pr.nonsmoker), color = 'red', linewidth = 1) +
  geom_line(aes(x = pred.age, y = pr.smokers), color = 'blue', linewidth = 1) +
  scale_x_continuous(breaks = seq(40, 100, 10)) +
  scale_y_continuous(limits = c(0, 100), breaks = seq(0, 100, 20))

## Use a bad solution: linear model
smoking$PercDead <- smoking$Dead/(smoking$Dead+smoking$Alive)
model.lm <- lm(PercDead ~ AgeAdj + Smoker, data = smoking)
summary(model.lm)

predict(model.2, list("AgeAdj" = 80, "Smoker" = "Y"), type = "response")
predict(model.lm, list("AgeAdj" = 80, "Smoker" = "Y"))

# 3. Count data
lizards <- read.csv("IBMS3_workshop/W5_Categorical and bounded data/lizards.csv")
model.3 <- glm(Count ~ Species * Location, 
               data = lizards, 
               family = poisson(link = log))

mixed.model <- glmer(Count ~ Species * Location + (1 | Location/Plot), 
                     data = lizards, 
                     family = poisson(link = log))

summary(model.3)
summary(mixed.model)
exp(confint(model.3))

marginals <- emmeans(model.3, ~ Species * Location)
pairs(marginals, by = "Species", type = "response")


