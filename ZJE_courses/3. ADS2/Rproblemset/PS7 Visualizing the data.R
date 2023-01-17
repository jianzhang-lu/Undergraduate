library(tidyverse)

#1. Import the GDP dataset and clean the data.

data_row <- read.csv("ADS_practical/GDP(2).csv")
data_new <- gather(data = data_row, key = "Year", value = "GDP", 2:60, convert = T)
data_new$Year <- as.numeric(gsub("X", "", data_new$Year))

data_new <- na.omit(data_new)
data_new <- drop_na(data_new)

data2 <- data_new %>% 
  filter(CountryName %in% c("Germany", "France", "Italy", "Greece")) %>%
  filter(Year %in% c("1960", "1970", "1980", "1990", "2000", "2010", "2018"))

data2$CountryName <- data2$CountryName <- as.factor(data2$CountryName)
summary(data2)

#2. Trend of GDP growth in the three countries.

ggplot(data2, aes(x = Year, y = GDP, color = CountryName)) +
  geom_point(size = 2) +
  geom_line() +
  labs(title = "GDP trends in the countries") +
  geom_text(aes(label = GDP), hjust = 0.1)


ggplot(data2, aes(x = Year, y = GDP, color = CountryName)) +
  geom_point(size = 2) +
  geom_line() +
  labs(title = "GDP trends in the countries") +
  geom_text(aes(label = GDP), hjust = 0.1) +
  facet_wrap(~CountryName, ncol = 4) 

  
ggplot(data2, aes(x = Year, y = GDP, color = CountryName)) +
  geom_smooth(method = "loess") +
  geom_point() 

ggplot(data2, aes(x = Year, y = GDP, fill = CountryName)) +
  geom_area(position = "fill")
  

ggplot(data2, aes(x = Year, y = GDP, fill = CountryName)) +
  geom_bar(stat = "identity", position = "dodge")


#3. Optional: Map the GDP.

data3 <- data2 %>% filter(Year == 2018)

library(maps)
eu_map <- map_data("world", region = c("France","Germany","Italy","Greece"))

names(eu_map)[5] = "CountryName"
ggplot(eu_map, aes(x = long, y = lat, group = group, fill = CountryName)) + 
  geom_polygon()


GDP_map <- left_join(eu_map, data3, by = "CountryName")
ggplot(GDP_map, aes(x = long, y = lat, group = group, fill = GDP)) +
  geom_polygon()


ggplot(GDP_map, aes(x = long, y = lat, group = group, fill = GDP)) +
  geom_polygon() +
  labs(title = "2018 GDP in eu countries") + 
  scale_fill_gradient(low = "blue", high = "red", 
                      breaks = c(1e+12, 2e+12, 3e+12), 
                      labels = c("1 Trillion", "2 Trillion", "3 Trillion"))

