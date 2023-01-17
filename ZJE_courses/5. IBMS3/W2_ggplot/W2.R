library(tidyverse)
metab <- read.csv("D:/R_document/IBMS3_workshop/W2_ggplot/metab.csv")
ggplot(data = metab, aes(x = Concentration)) +
  geom_histogram(binwidth = 20)

ggplot(data = metab, aes(x = Concentration)) +
  geom_histogram(bins = 200)

ggplot(metab, aes(x = Treatment, y = Concentration)) +
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(width = 0.1)

ggplot(metab, aes(x = Treatment, y = Concentration)) +
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(width = 0.1, aes(col = Age), size = 0.8)

# Challenge:
ggplot(metab, aes(x = Concentration, fill = Sex)) +
  geom_histogram(position = 'dodge')

ggplot(metab, aes(x = Concentration, col = Sex)) +
  geom_density()

# Faceting
ggplot(metab, aes(x = Treatment, y = Concentration)) +
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(width = 0.1, size = 0.5) +
  facet_grid(.~Sex) # facet_grid(cols = vars(Sex))

ggplot(metab, aes(x = Treatment, y = Concentration)) +
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(width = 0.1, size = 0.5) +
  facet_wrap(~Sex)

metab$AgeCateg <- ifelse(metab$Age <= 60, "Young", "Old")

ggplot(metab, aes(Treatment, Concentration)) +
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(width = 0.1, size = 0.5) +
  facet_grid(vars(AgeCateg), vars(Sex))


ggplot(data = metab, aes(x = Treatment, y = Concentration)) + 
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(width = 0.1, size = 0.5) + 
  facet_grid(AgeCateg ~ .)

# More complex features
library(ggpmisc)
ggplot(data = metab, aes(x = Age, y = Concentration)) +
  geom_point(aes(col = Sex), size = 0.5) +
  geom_smooth(aes(col = Sex), method = 'lm', se = F) +
  stat_poly_eq(aes(label = paste(..eq.label.., ..adj.rr.label.., sep = '~~~~'), 
                   color = Sex), formula = y~x, parse = T, label.x = 0.6)


library(ggpubr)
ggscatter(metab, x = 'Age', y = 'Concentration', add = 'reg.line',
          add.params = list(color = 'red'), size = 0.5)



