library(nlme)
library(tidyverse)
library(emmeans)

# 1. Repeated Measure Design
bromocriptine <- read.csv("IBMS3_workshop/W4_Mixed-effects models/bromocriptine.csv")
bromocriptine$Group <- factor(bromocriptine$Group, 
                              levels = c("CTRL", "Bromo1", "Bromo10"),
                              labels = c('Control', 'Bromocriptine (1mg)', 'Bromocriptine (10mg)'))

## Reproduce graphs
data1 <- bromocriptine %>% 
  group_by(Time, Group) %>% 
  summarise('PRL_mean' = mean(PRL))

ggplot(data1, aes(x = Time, y = PRL_mean)) +
  geom_line(aes(color = Group)) +
  geom_point() +
  labs(col = 'Treatment')

ggplot(bromocriptine, aes(x = Time, y = PRL)) +
  geom_line(aes(color = Group, group = Mouse), size = 0.7) +
  theme(legend.position = "bottom")

ggplot(filter(bromocriptine, Time == 0), aes(x = Group, y = PRL)) +
  geom_boxplot(aes(fill = Group)) +
  geom_point()

## Design the model
model_group <- lme(PRL ~ Group * Time, 
                   data = bromocriptine, 
                   random = ~ Group - 1 | Mouse)
summary(model_group)
coef_group <-  coef(model_group)

model_time <- lme(PRL ~ Group * Time, 
                  data = bromocriptine, 
                  random = ~ Time - 1 | Mouse)
summary(model_time)
coef_time <-  coef(model_time)

plot(model_time, pch = 20)
head(random.effects(model_time))

par(mfrow = c(2, 1))
hist(random.effects(model_time)$Time, main = "", col = "black", xlab = "Random effects",
     las = 1)
hist(resid(model_time), main = "", col = "black", xlab = "Residuals", las = 1)

plot(PRL ~ Time, bromocriptine, subset = bromocriptine$Mouse == 1, 
     t = "l", las = 1, bty = "n")
lines(PRL ~ Time, bromocriptine, subset = bromocriptine$Mouse == 6, 
      col = "blue")

abline(a = 17.24, b = 3.96, lty = "dashed") # Mouse 1
abline(a = 17.24, b = 1.91, lty = "dashed") # Mouse 6


## Post-hoc analysis
marginals <- emmeans(model_time, ~Group * Time, cov.reduce = range)
pairs(marginals, by = "Time")

### Very useful to test all times
marginals.2 <- emmeans(model_time, ~Group * Time, cov.reduce = unique)
pairs(marginals.2, by = "Time")


# 2. Nested design
Oats <- Oats
summary(Oats)
ggplot(Oats, aes(x = nitro, y = yield)) +
  geom_line(aes(color = Block), size = 0.7) +
  facet_wrap(vars(Variety)) +
  theme(legend.position = "bottom")

model.oats <- lme(yield ~ nitro * Variety, 
                  data = Oats, 
                  random = ~1 | Block/Variety)
summary(model.oats)

model.oats.2 <- lme(yield ~ nitro + Variety, 
                    data = Oats, 
                    random = ~1 | Block/Variety)
summary(model.oats.2)

model.oats.3 <- lme(yield ~ nitro + Variety, 
                    data = Oats, 
                    random = ~1 | Block/Variety/nitro)
summary(model.oats.3)

