library(tidyverse)

transfer <- function(pixel_number){
  row <- pixel_number %/% 28 + 1
  column <- pixel_number %% 28
  if(column == 0){
    column = 28
    row = row - 1
  }
  return(c(row,column))
}

xs <- c()
ys <- c()
for(i in 1:784){
  coordinate <- transfer(i)
  xs <- c(xs, coordinate[1])
  ys <- c(ys, coordinate[2])
}


data <- read.csv("ADS_practical/mnist_test.csv", header = F)[1:1000,]
data$sample <- 1:1000
colnames(data)[1] <- 'number'
data_long <- gather(data, 2:785, key='pixel', value='indensity')
data_long$x <- rep(ys, each = 1000)
data_long$y <- rep(rev(xs), each = 1000)


# ggplot(data_long, aes(x = x, y = y)) + 
#   geom_tile(aes(fill = indensity)) +
#   facet_wrap(vars(sample, number), nrow = 4) +
#   theme_classic() +
#   coord_fixed()

agg_data <- aggregate(data_long[,c(4)], 
                      by=list(data_long$number, data_long$x, data_long$y),
                      FUN = mean)
colnames(agg_data) <- c("number","x","y","indensity")

ggplot(agg_data, aes(x = x, y = y)) + 
  geom_tile(aes(fill = indensity)) +
  facet_wrap(vars(number)) +
  theme_classic() +
  coord_fixed()

## Find features
features <- unique(data_long[,c(1,2)])

feature_x <- data_long %>% 
  group_by(sample, y) %>% 
  summarise("indensity" = mean(indensity))

feature_y <- data_long %>% 
  group_by(sample, x) %>% 
  summarise("indensity" = mean(indensity))

for(i in 1:28){
  index <- filter(feature_x, y==i)$indensity
  features[,i+2] <- index
}

for(i in 1:28){
  index <- filter(feature_y, x==i)$indensity
  features[,i+30] <- index
}

feature_long <- gather(features, 3:58, key='feature', value='indensity')
feature_long$feature <- rep(1:56, each = 1000)
gather_feature <- feature_long %>% 
  group_by(number, feature) %>% 
  summarise('average' = mean(indensity)) 

ggplot(gather_feature) +
  geom_line(aes(x = feature, y = average, color = factor(number))) +
  facet_wrap(vars(factor(number)))
