library(tidyverse)
library(RcppRoll)

download.file(
  "https://github.com/hugocarlos/covid-19-data/blob/master/public/data/owid-covid-data.csv?raw=true",
  "owid-covid-data.txt")

covid <- read.csv("ADS_practical/owid-covid-data.txt")

# Selecting some columns
subcovid <- covid %>%
  select(iso_code, location, date, new_cases, new_deaths, new_cases_per_million,
         total_cases_per_million, new_vaccinations, people_fully_vaccinated,
         aged_65_older, aged_70_older, gdp_per_capita, extreme_poverty,
         cardiovasc_death_rate, diabetes_prevalence, life_expectancy,
         human_development_index)

# To date format
subcovid$date <- as.Date(subcovid$date)

# Setting one country
one_country <- "France"

# Write the function
generate_rolling_avg <- function(data, country, column, days_num){
  range_days_in_one_country <- 
    range(data$date[which(subcovid$location == one_country)])
  
  # Identifying the dates present in subcovid
  dates_included <- seq(range_days_in_one_country[1], 
                        range_days_in_one_country[2], by="days")
  
  # Calculating 7-day rolling mean
  variable_means <- sapply(dates_included[-(1:6)], function(end_of_the_week){
    # end_of_the_week <- dates_included[7]
    x_days_cases <- sapply(-6:0, function(y){
      # y <- -6
      data[which(data$location == country & 
                       data$date == (end_of_the_week + y)), column]
    })
    mean(x_days_cases)
  })
  variable_means_df <- data.frame(Dates = dates_included[-(1:6)],
                                  new_variable_avg = variable_means)
}

# Calculating the 7-days window average for new cases of COVID-19
cases_means_df <- generate_rolling_avg(subcovid, one_country, "new_cases", 7)

# Merging cases_means_df to subcovid
subcovid$new_cases_avg <- NA
for(i in 1:nrow(cases_means_df)){
  # i <- 1
  subcovid$new_cases_avg[which(subcovid$location == one_country &
                                 subcovid$date == cases_means_df$Dates[i])] <-
    cases_means_df$new_variable_avg[i]
}

# Plot 1
ggplot() +
  geom_bar(stat = "identity",
           aes(x = subcovid$date[which(subcovid$location == one_country)],
               y = subcovid$new_deaths[which(subcovid$location == one_country)],
               colour = "New deaths")) +
  geom_point(aes(x = subcovid$date[which(subcovid$location == one_country)],
                 y = subcovid$new_cases[which(subcovid$location == one_country)],
                 colour = "New cases"), size = 0.7) +
  # geom_line(aes(x = cases_means_df$Dates,
  # y = cases_means_df$avg_mean,
  geom_line(aes(x = subcovid$date[which(subcovid$location == one_country)],
                y = subcovid$new_cases_avg[which(subcovid$location == one_country)],
                colour = "7-day rolling average")) +
  labs(x = "Date", y = "Cases") +
  ggtitle(paste0("COVID-19 Cases and Deaths in ", one_country)) +
  theme(legend.position = c(0.2, 0.8),
        legend.title = element_blank(),
        legend.background = element_blank(),
        legend.key = element_rect(fill = NULL, color = NULL))


# Plot 2

# Finding all the days from 2021, as they probably contain vaccination data.
dates_from_2021 <- seq(as.Date("2021-01-01"), (Sys.Date() - 1), by = "days")

one_country <- "Israel"
# Re-calculating the vector with 7-day rolling average of new COVID-19 cases
cases_means_df <- generate_rolling_avg(subcovid, one_country, "new_cases", 7)
download.file(
  "https://raw.githubusercontent.com/hugocarlos/public_scripts/master/teaching/WBpopulation.csv",
  "WBpopulation.csv")
population <- read.csv("ADS_practical/WBpopulation.csv", header = TRUE, sep = "\t")

# Calculating the percentage of the population fully vaccinated
Israel_population <- population$X2020[which(population$Country.Name == one_country)]
subcovid$share_fully_vaccinated <- subcovid$people_fully_vaccinated * 100 / Israel_population

# Merging cases_means_df to subcovid
subcovid$new_cases_avg <- NA
for(i in 1:nrow(cases_means_df)){
  # i <- 1
  subcovid$new_cases_avg[which(subcovid$location == one_country &
                                 subcovid$date == cases_means_df$Dates[i])] <-
    cases_means_df$new_variable_avg[i]
}

subcovid %>%
  filter(location == one_country) %>%
  filter(date >= dates_from_2021[1] & date < dates_from_2021[90]) %>%
  #  filter(date >= dates_from_2021[1] & date < dates_from_2021[length(dates_from_2021)]) %>%
  ggplot() +
  geom_point(aes(x = date, y = share_fully_vaccinated*200,
                 colour = "Share of people fully vaccinated")) +
  geom_point(aes(x = date, y = new_cases_avg, colour = "New COVID-19 cases (7-day avg)")) +
  scale_y_continuous(name = "Number of cases",
                     sec.axis = sec_axis(~./200, name = "% of total population vaccinated",
                                         labels = function(b){
                                           paste0(b, "%")
                                         })) +
  xlab("Date") +
  theme(axis.title.y = element_text(color = "cyan4"),
        axis.title.y.right = element_text(color = "tomato"),
        legend.position = "bottom")

# Plot 3
covid_onecountry <- subcovid[which(subcovid$location == "Israel" &
                                     subcovid$date >= as.Date("2021-02-15") &
                                     subcovid$date < as.Date("2021-04-01")), ]
# Calculating the Correlation Coefficient
cor(covid_onecountry$new_cases_avg,
    covid_onecountry$share_fully_vaccinated,
    use = "complete.obs")
## [1] -0.9166231

lm_Israel <- lm(new_cases_avg ~ share_fully_vaccinated, covid_onecountry)
plot(x = covid_onecountry$share_fully_vaccinated, y = covid_onecountry$new_cases_avg,
     xlab = "New COVID-19 cases (7-day avg)",
     ylab = "% of population fully vaccinated")
abline(lm_Israel, col = "red")
summary(lm_Israel)

# Tasks
subcovid <- na.omit(subcovid)
library(corrplot)
corrplot(cor(subcovid[,c(4:9,18,19)]), order = "AOE",
         method = "ellipse", type = "upper", tl.pos = "d", tl.cex = 0.8)
corrplot(cor(subcovid[,c(4:9,18,19)]), order = "AOE", add = T,
         method = "number", type = "lower", tl.pos = "n", diag = F)

corrplot(cor(subcovid[,c(4:9, 18,19)]), order = "AOE", method = "color", 
         addCoef.col = "black", type = "upper", col = rev(COL2("RdBu",200)))

# Choose a country
subcovid <- covid %>%
  select(iso_code, location, date, new_cases, new_deaths, new_cases_per_million,
         total_cases_per_million, new_vaccinations, people_fully_vaccinated,
         aged_65_older, aged_70_older, gdp_per_capita, extreme_poverty,
         cardiovasc_death_rate, diabetes_prevalence, life_expectancy,
         human_development_index) %>%
  filter(location == "Ukraine")
subcovid$date <- as.Date(subcovid$date)

ggplot(subcovid) +
  geom_point(aes(x = date, y = new_cases))



