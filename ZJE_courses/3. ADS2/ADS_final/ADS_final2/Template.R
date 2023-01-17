## 画图工具
# 标题居中
theme(plot.title = element_text(hjust = 0.5))

# 坐标轴标度相同
coord_fixed()

# 横坐标标签换方向
theme(axis.text.x = element_text(angle = 90, hjust = 1))

# 画误差线
geom_errorbar(aes(ymin = lower, ymax = upper), width = 0.3)

## ANOVA 模拟
same_group <- c()
different_group <- c()
for(i in 1:1000){
  sample_index <- sample(1:nrow(data), 2, replace = F)
  sample1 <- data[sample_index[1],]
  sample2 <- data[sample_index[2],]
  pain_diff <- abs(sample1$pain - sample2$pain)
  if (sample1$treatment == sample2$treatment){
    same_group <- c(same_group, pain_diff)
  }
  else{
    different_group <- c(different_group, pain_diff)
  }
}

class_result <- c(rep("same group", length(same_group)), 
                  rep("different group", length(different_group)))
pain_result <- c(same_group, different_group)
result <- data.frame("group" = class_result, "difference" = pain_result)
ggplot(result, aes(x = factor(group, levels = c("same group", "different group")), 
                   y = difference)) +
  geom_boxplot(aes(fill = group)) +
  labs(x = NULL)
mean(same_group)
mean(different_group)

## ANOVA model

# Do the test before ANOVA
# 1. Test the normality of residuals
model <- aov(data = data, y~x)
shapiro.test(resid(model))$p.value ### p = 0.42, normally distributed.

## 2. Test the equality of variances
plot(model, 1) ### The heights of each columns are similar.

# 3. Run the ANOVA
summary(model) 

# 4. Run the post-hoc test
TukeyHSD(model) 

model2 <- aov(data, weight_gain~diet*genotype) #都是列名
shapiro.test(resid(model2))$p.value
plot(model2, 1)
summary(model2)
TukeyHSD(model2)

## 线性回归
# Pearson’s correlation coefficient
cor(data$height, data$weight)
cor.test(data$height, data$weight)

# Test each of the assumptions for this data
model <- lm(data$weight ~ data$height)
plot(model, 2)
plot(model, 1)
hist(resid(model))

# Intepret the result
summary(model)

# 画图outlier图
cooksd <- cooks.distance(model)
plot(cooksd, pch = "*", cex = 2, ylab = "Cook's distance")
abline(h = 4/nrow(data), col = "red")

# 画图corrplot
# 画图corrplot
corrplot(cor(data), order = "AOE",
         method = "ellipse", type = "upper", tl.pos = "d")
corrplot(cor(data), order = "AOE", add = T,
         method = "number", type = "lower", tl.pos = "n", diag = F)

corrplot(cor(data), order = "AOE", method = "color", 
         addCoef.col = "black", type = "upper", col = rev(COL2("RdBu",200)))

# 画图ggscatter
ggscatter(data, x = "weight", y = "height", add = "reg.line",
          add.params = list(color = "blue", fill = "lightgray"),
          conf.int = T)

geom_smooth(method = "lm", formula = y~x, se = F)
abline(model)

# 图上标表达式
library(ggpmisc)
stat_poly_eq(aes(label = paste(..eq.label.., ..adj.rr.label.., sep = '~~~~')),
             color = 'red',
             label.x = 0.25,
             geom = 'label',
             formula = y~x+I(x^2),
             parse = T)

# 图上标相关系数和p值
stat_cor(data, method = 'pearson')

## bootstrap两种情况
# permutation test
Female <- data[data$gender == "F", "points"]
Male <- data[data$gender == "M", "points"]
pool <- c(Female, Male)
real_mean <- abs(mean(Female) - mean(Male))

boot_means <- c()
for (i in 1:10000){
  boot_sample <- sample(pool, length(pool), F)
  boot_female <- boot_sample[1:length(Female)]
  boot_male <- boot_sample[(length(Female)+1):length(pool)]
  boot_mean <- abs(mean(boot_female) - mean(boot_male))
  boot_means <- c(boot_means, boot_mean)
}

hist(boot_means, 10)
abline(v = real_mean, col = "red", lwd = 3)
p_value <- mean(boot_means >= real_mean)
wilcox.test(Female, Male, alternative = "greater", exact = F)

# case resampling
data$upper <- 0
data$lower <- 0
generate_sample <- function(new, total){
  old <- total - new
  dataset <- c(rep("new", new), rep("old", old))
  return(dataset)
}

boot <- function(sample){
  boot_results <- c()
  for(i in 1:100){
    boot_sample <- sample(sample, length(sample), T)
    new_length <- sum(boot_sample == "new")
    boot_results <- c(boot_results, new_length)
  }
  return(boot_results)
}

for (i in 1:nrow(data)){
  dataset <- generate_sample(data[i,3], data[i,2])
  results <- boot(dataset)
  data[i,5] <- quantile(results, 0.975)/data2[i,2]
  data[i,6] <- quantile(results, 0.025)/data2[i,2]
}

## Explore the differences across countries.
ggplot(data2, aes(x = Country, y = percentage)) +
  geom_point() +
  geom_errorbar(aes(ymin = lower, ymax = upper), width = 0.3) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))