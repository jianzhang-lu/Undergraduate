library(tidyverse)

# 1. Overplotting.

data <- diamonds
ggplot(data, aes(x = carat, y = price, color = cut)) +
  geom_point()

## 1.1 To make it better. (size and transparency)
ggplot(data, aes(x = carat, y = price, color = cut)) +
  geom_point(size = 0.1, alpha = 1/5)

## 1.2 change the shape of dots.
ggplot(data, aes(x = carat, y = price, color = cut)) +
  geom_point(shape = 18)


# 2. Rewrite the code.

ggplot(data, aes(x = carat)) + 
  geom_area(stat = "bin", binwidth = 0.1) +
  scale_y_continuous(breaks = seq(0, 10000, 2000), limits = c(0, 10500)) +
  scale_x_continuous(breaks = seq(0, 3, 0.5), limits = c(0,3))

ggplot(data, aes(x = carat)) + 
  geom_point(aes(size = ..density..), stat = "bin", binwidth = 0.1) +
  scale_x_continuous(breaks = seq(0, 3, 0.5), limits = c(0, 3))

# 3. Build plots layer by layer

## 3.1 Plot the following boxplot from the dataset “diamonds”.

base <- ggplot(data, aes(x = clarity, y = carat, color = cut)) +
  geom_boxplot()

## 3.2 

ggplot(data, aes(x = clarity, y = carat, color = cut)) +
  geom_boxplot() +
  geom_smooth(aes(group = cut), method = "lm", se = F)
  
sm <- geom_smooth(aes(group = cut), method = "lm", se = F)
## 3.3 Faceting the plot by cut, color and cut~color.

Facet1 <- facet_wrap(~cut)
Facet2 <- facet_wrap(~color)
Facet3 <- facet_grid(cut~color)

base + Facet1
base + Facet2
base + Facet3 + color

## 3.4 Add another layer to add a title to the plot using labs

title <- labs(title = "Carat vs clarity box plot")

## 3.5 Change the color

color <- scale_color_brewer(palette = "Dark2")

## 3.6 Save the plot
save <- ggsave("Test.png")



# 4. Scale the y axis

## 4.1 Transform the y-axis scle to log10(carat)

base2 <- base + scale_y_continuous(trans = "log10")
base3 <- base2 + ylab("log10(carat)")

## 4.2 Redo the boxplot with log10(y).

base4 <- ggplot(data, aes(x = clarity, y = log10(carat), color = cut)) +
  geom_boxplot()

## 4.3 Add a layer of linear 

base3 + sm
sm2 <- geom_smooth(aes(x = clarity, group = cut, y = log10(carat)), method = "lm", se = F)
base3 + sm2

## 4.4 change the range of y-axis.

base6 <- base + scale_y_continuous(limits = c(0.3, 3.0), trans = "log10") +
  ylab("log10(carat)")

# 5. Jitter plot and scales.

## 5.1 Make the layer
sample <- data[sample(nrow(data), 100, replace = F), ]
ggplot(sample, aes(x = clarity, y = carat)) +
  geom_jitter(aes(size = carat, color = price)) +
  geom_boxplot()

## 5.2 reset the color scale

ggplot(sample, aes(x = clarity, y = carat)) +
  geom_jitter(aes(size = carat, color = price)) +
  geom_boxplot() +
  scale_color_gradient(low = "red", high = "green", limit = c(10000, 15000))

## 5.3 reset the size scale

ggplot(sample, aes(x = clarity, y = carat)) +
  geom_jitter(aes(size = carat, color = price)) +
  scale_size_continuous(limits = c(1.2, 2)) +
  geom_boxplot()

# 6. Position

data5 = data
new_level <- rev(attributes(data$cut)$levels)
data5$cut <- factor(data5$cut, levels = new_level)

ggplot(data5, aes(x = clarity, fill = cut)) +
  geom_bar(position = "stack") + 
  scale_y_continuous(limits = c(0,14000), breaks = seq(0,12000,2000))

ggplot(data5, aes(x = clarity, fill = cut)) +
  geom_bar(position = "fill")

ggplot(data, aes(x = clarity, fill = cut)) +
  geom_bar(position = "dodge") + 
  scale_y_continuous(limits = c(0,5200), breaks = seq(0,5000,1000))


