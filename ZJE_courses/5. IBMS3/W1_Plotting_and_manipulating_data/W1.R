library(reshape2)
library(tidyverse)
metab <- read.csv("D:/R_document/IBMS3_workshop/W1_Plotting_and_manipulating_data/metab.csv")

# 1. Just some tries.
table(metab$Sex, metab$Treatment)
quantile(metab$Concentration)
quantile(metab$Age, probs = c(0.3, 0.7))
range(metab$Age)
plot(metab$Concentration, 
     pch = 'x', cex = 0.7, cex.axis = 0.8, 
     las = 0, ylab = "Concentration")

# 2. The par function.
man <- subset(metab, metab$Sex == 'M')
woman <- subset(metab, metab$Sex == 'F')
par(mfrow = c(2,1))
plot(man$Concentration, 
     pch = 20, cex = 0.7, cex.axis = 0.8, 
     las = 1, ylab = "Concentration", xlab = 'Man', ylim = c(-100, 800))
plot(woman$Concentration, 
     pch = 20, cex = 0.7, cex.axis = 0.8, 
     las = 1, ylab = "Concentration", xlab = 'Woman', ylim = c(-100, 800))

# 3. Plot with colors.
par(mfrow = c(1,1))
colors <- rep('darkgreen', nrow(metab))
colors[metab$Sex == 'F'] <- 'purple'
colors = ifelse(metab$Sex == 'F', 'purple', 'darkgreen')

plot(metab$Concentration, col = colors, 
     bty = "n", pch = 20, cex = 0.7, cex.axis = 0.8,
     las = 1, ylab = "Concentration")
legend("topright", legend = c("Men", "Women"), 
       fill = c("darkgreen", "purple"), cex = 0.7)

# 4. Remove the wrong one
wrong <- which(metab$Concentration < 0)
metab <- metab[-wrong, ]

# 5. Generate one plot
colors = ifelse(metab$Sex == 'F', 'orange', 'blue')
types = ifelse(metab$Sex == 'F', 20, 1)

plot(metab$Concentration, col = colors, 
     bty = "n", pch = types, cex = 1, cex.axis = 0.8, lwd = 1,
     las = 1, ylab = "Concentration")
legend("topright", legend = c("Men", "Women"), 
       col = c('blue', 'orange'), cex = 0.7, pch = c(1, 19))
abline(h = mean(man$Concentration), col = 'blue', lwd = 2)
abline(h = mean(woman$Concentration), col = 'orange', lwd = 2)

# 6. Grouping data
metab$Treatment <- factor(metab$Treatment, 
                          levels = c('CTRL', 'A', 'B'))
boxplot(Concentration ~ Treatment, metab, las = 1, 
        ylim = c(0, 1000), pch = 20, ylab = "Concentration")

boxplot(Concentration ~ Treatment + Sex, metab, las = 1, 
        ylim = c(0, 1000), pch = 20, ylab = "Concentration")

boxplot(Concentration ~ Sex + Treatment, metab, las = 1, 
        ylim = c(0, 1000), pch = 20, ylab = "Concentration")

ggplot(metab, aes(x = Treatment, y = Concentration)) +
  geom_boxplot(aes(fill = Sex))

# 7. Add points to the plot.
boxplot(Concentration ~ Treatment, metab, pch = 20)
stripchart(Concentration ~ Treatment, metab, 
           add = TRUE, vert = TRUE, pch = 20, cex = 0.8,
           method = "jitter", jitter = 0.1)

# 8. Histograms
hist(metab$Concentration, col = "black", las = 1, 
     main = "Concentration of metabolite",
     xlab = "Concentration")

## Method 1 to specify the number of columns. (显示拆分成几段)
hist(metab$Concentration, col = "black", las = 1, 
     breaks = 100, main = "Concentration of metabolite",
     xlab = "Concentration")

## Method 2 to specify the number of columns. (显示各个端点)
hist(metab$Concentration, col = "black", las = 1, 
     breaks = seq(0, 1000, 50), main = "Concentration of metabolite",
     xlab = "Concentration")

# 9. Bar-plot.
males <- metab$Concentration[metab$Sex == "M"]
females <- metab$Concentration[metab$Sex == "F"]
mean.M <- mean(males)
mean.F <- mean(females)
sd.M <- sd(males)
sd.F <- sd(females)

## Important: bar-plots returns the x position of each bar
bp <- barplot(c(Men = mean.M, Women = mean.F), 
              col = c("green", "orange"), ylim = c(0, 600), 
              las = 1, ylab = "Concentration")
### As same as:
bp <- barplot(c(mean.M, mean.F), names.arg = c('Men', 'Women'), 
              col = c("green", "orange"), ylim = c(0, 600), 
              las = 1, ylab = "Concentration")

arrows(x0 = bp, y0 = c(mean.M - sd.M, mean.F - sd.F), 
       x1 = bp, y1 = c(mean.M + sd.M, mean.F + sd.F),
       angle = 90, code = 3)

# 10. Deal with missing data
neurons <- read.csv("D:/R_document/IBMS3_workshop/W1_Plotting_and_manipulating_data/neurons.csv")
typeof(neurons$counts)
summary(neurons)
which(is.na(neurons$counts))

## 原包方法 aggregate
attach(neurons)
aggregate(neurons[,5], by = list(region), FUN = mean)
## tidyverse方法
neurons %>% group_by(region) %>%
  summarise(count_avg = mean(counts), count_sum = sum(counts))

## Complex method
neurons2 <- neurons[complete.cases(neurons), ]
## Simple method
neurons2 <- na.omit(neurons)

ggplot(neurons, aes(x = age, y = counts)) +
  geom_point() +
  geom_smooth(method = 'lm', formula = y~x, se = F)
## list omission: 只要有NA就删除
cor(neurons[, c(3,5)], use = 'complete.obs')

## Pairwise omission: 
cor(neurons[, c(3,5)], use = 'pairwise.complete.obs')

# 11. Converting between wide and long data.
lizard <- read.csv("D:/R_document/IBMS3_workshop/W1_Plotting_and_manipulating_data/lizard.csv")

## reshape2::melt
lizard.long <- melt(lizard, id.vars = "Lizard", 
                    variable.name = "Location", 
                    value.name = "Counts")

## tidyverse::gather
gather(lizard, 2:6, key = 'Location', value = 'Counts')

boxplot(Counts ~ Location, lizard.long, 
        las = 2, ylab = "Number of lizards")

boxplot(Counts ~ Location, lizard.long, 
        las = 2, ylab = "Number of lizards", xlab = "")
mtext("Location", side = 1, line = 4)

# The last practice.
BP <- read.csv("D:/R_document/IBMS3_workshop/W1_Plotting_and_manipulating_data/BP.csv")
BP.long <- gather(BP, 2:3, key = 'Drug', value = 'FC')
nrow(BP)
sum(BP$Sex == 'M')
sum(BP$Sex == 'F')
old <- filter(BP, Age > 50)
nrow(old)
sum(old$Sex == 'F')

ggplot(BP.long, aes(x = Sex, y = FC)) +
  geom_boxplot(aes(fill = Sex))

BP.long$state <- ifelse(BP.long$Age > 50, 'Older', 'Younger')
ggplot(BP.long, aes(x = state, y = FC)) +
  geom_boxplot(aes(fill = state))

## Box-plot
ggplot(BP.long, aes(x = Drug, y = FC)) +
  geom_boxplot(aes(fill = Drug)) +
  labs(y = 'Fold Change') +
  theme(axis.title.y = element_text(size = 12))

## Bar-plot
drug1 <- BP.long$FC[BP.long$Drug == "Drug1"]
drug2 <- BP.long$FC[BP.long$Drug == "Drug2"]
mean.1 <- mean(drug1)
mean.2 <- mean(drug2)
sd.1 <- sd(drug1)
sd.2 <- sd(drug2)

bp <- barplot(c(mean.1, mean.2), names.arg = c('Drug1', 'Drug2'), 
              col = c("green", "orange"), 
              las = 1, ylab = "Fold Change", width = 0.5, 
              xlim = c(0, 2), ylim = c(0, 1.8))

arrows(x0 = bp, y0 = c(mean.1 - sd.1, mean.2 - sd.2), 
       x1 = bp, y1 = c(mean.1 + sd.1, mean.2 + sd.2),
       angle = 90, code = 3)

## Histogram
par(mfrow = c(1,2))
hist(drug1, col = 'green', las = 1, 
     xlab = "Drug1", main = "FC of Drug1")

hist(drug2, col = 'orange', las = 1, 
     xlab = "Drug2", main = "FC of Drug2")

BP[BP$ID == 'OV019', ]


