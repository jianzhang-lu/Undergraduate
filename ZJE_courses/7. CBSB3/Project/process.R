library(tidyverse)
library(corrgram)
library(Cairo)

setwd("CBSB3_workshop/Project/")
quote_input <- read.csv("input_data/quote_schemainfo2.csv")
paint_input <- read.csv("input_data/painting_schemainfo2.csv")

quote_summary <- read.csv("experiment_data/quote_summary.csv")
paint_summary <- read.csv("experiment_data/painting_summary.csv")

quote_fam <- na.omit(read.csv("quotes_fam.csv"))
paint_fam <- na.omit(read.csv("painting_fam.csv"))

colnames(paint_fam)[-1] <- gsub('pre_', '', colnames(paint_fam)[-1], fixed = F)
colnames(paint_fam)[-1] <- gsub('_F', '', colnames(paint_fam)[-1], fixed = F)

# 将ID前面的组名去掉
quote_summary$ID <- gsub('[a-zA-Z]+', '', quote_summary$ID, fixed = F)
paint_summary$ID <- gsub('[a-zA-Z]+', '', paint_summary$ID, fixed = F)

paint_group <- unique(paint_summary[, c(1, 30)])
quote_group <- unique(quote_summary[, c(1, 30)])

## paint
paint_fam <- merge(paint_fam, paint_group, by.x = 'X', by.y = 'ID', all.y = T)
paint_fam <- na.omit(paint_fam)
table(paint_fam$type)

paint_fam_final <- paint_fam %>% 
  group_by(type) %>%
  summarise_at(-1, mean)

for(i in 2:16){
  data <- paint_fam_final[, i]
  paint_fam_final[, i] <- (data-min(data))/(max(data)-min(data))
}

t_paint <- t(paint_fam_final)
colnames(t_paint) <- t_paint[1, ]
t_paint <- t_paint[-1, ]

name <- paint_input$author
t_paint <- t_paint[match(name, rownames(t_paint)), ]

type <- colnames(t_paint)
for(i in type){
  paint_input$familirarity <- t_paint[, i]
  path <- paste0('paint_', 'fam_', i, '.csv')
  write.csv(paint_input, path)
}

## quote
colnames(quote_input)[4] <- 'familirarity'
quote_fam <- merge(quote_fam, quote_group, by = 'ID', all.y = T)
quote_fam <- na.omit(quote_fam)
table(quote_fam$type)

quote_fam_final <- quote_fam %>% 
  group_by(type) %>%
  summarise_at(-1, mean)

for(i in 2:16){
  data <- quote_fam_final[, i]
  quote_fam_final[, i] <- (data-min(data))/(max(data)-min(data))
}

t_quote <- t(quote_fam_final)
colnames(t_quote) <- t_quote[1, ]
t_quote <- t_quote[-1, ]

type <- colnames(t_quote)
for(i in type){
  quote_input$familirarity <- t_quote[, i]
  path <- paste0('quote_', 'fam_', i, '.csv')
  write.csv(quote_input, path)
}


## Correct the data
schema_paint <- paint_summary[, c(16:19, 24:26, 29:30)]
pay_paint <- paint_input[, 1:2] 

for(i in 1:nrow(schema_paint)){
  schema <- as.vector(t(schema_paint[i, 1:4]))
  
  # 1. 处理accuracy
  if(length(unique(schema)) == 1){
    schema_paint[i, 6] = 1
  }
  else if(length(unique(schema) == 2) & sum(table(schema) > 2) == 1){
    schema_paint[i, 6] = 0.5
  }
  else{
    schema_paint[i, 6] = 0
  }
  
  # 2. 处理payoff
  pay <- pay_paint[schema, 2]
  schema_paint[i, 5] = sum(pay)/4
  
  # 3. 处理performance
  accuracy = schema_paint[i, 6]
  
  ## break前是high risk
  if((schema_paint[i, 9] %in% c('H', 'Hc', 'HL')) & schema_paint[i, 8] == 0){
    if(accuracy == 1){
      schema_paint[i, 7] = sum(pay) * 3
    }
    else{
      schema_paint[i, 7] = sum(pay)
    }
  }
  ## break前是low risk
  else if((schema_paint[i, 9] %in% c('L', 'Lc', 'LH')) & schema_paint[i, 8] == 0){
    if(accuracy == 1){
      schema_paint[i, 7] = sum(pay) * 3
    }
    else if(accuracy == 0.5){
      schema_paint[i, 7] = sum(pay) * 2
    }
    else{
      schema_paint[i, 7] = sum(pay)
    }
  }
  
  ## break后是high risk
  else if((schema_paint[i, 9] %in% c('H', 'Hc', 'LH')) & schema_paint[i, 8] == 1){
    if(accuracy == 1){
      schema_paint[i, 7] = sum(pay) * 3
    }
    else{
      schema_paint[i, 7] = sum(pay)
    }
  }
  
  ## break后是low risk
  else if((schema_paint[i, 9] %in% c('L', 'Lc', 'HL')) & schema_paint[i, 8] == 1){
    if(accuracy == 1){
      schema_paint[i, 7] = sum(pay) * 3
    }
    else if(accuracy == 0.5){
      schema_paint[i, 7] = sum(pay) * 2
    }
    else{
      schema_paint[i, 7] = sum(pay)
    }
  }
}

paint_summary[, 24:26] <- schema_paint[, 5:7]
write.csv(paint_summary, "experiment_data/painting_summary.csv")


# Correlation matrix
quote_summary <- read.csv("experiment_data/quote_summary.csv")
paint_summary <- read.csv("experiment_data/painting_summary.csv")

paint_bef <- filter(paint_summary, afterbreak == 0)[, c(5:16, 21:27)]
paint_aft <- filter(paint_summary, afterbreak == 1)[, c(5:16, 21:27)]

quote_bef <- filter(quote_summary, afterbreak == 0)[, c(4:15, 20:26)]
quote_aft <- filter(quote_summary, afterbreak == 1)[, c(4:15, 20:26)]

Cairo::CairoPNG(filename = "Results/Correlation_paint_before.png", 
                width = 7, height = 7, units = "in", dpi = 300) 

corrplot::corrplot(corr = cor(paint_bef), method = 'color', type = 'upper',
                   order = "original", addCoef.col = 'black', number.cex = 0.5)

dev.off() 

Cairo::CairoPNG(filename = "Results/Correlation_paint_after.png", 
                width = 7, height = 7, units = "in", dpi = 300) 

corrplot::corrplot(corr = cor(paint_aft), method = 'color', type = 'upper',
                   order = "original", addCoef.col = 'black', number.cex = 0.5)

dev.off()


Cairo::CairoPNG(filename = "Results/Correlation_quote_before.png", 
                width = 7, height = 7, units = "in", dpi = 300) 

corrplot::corrplot(corr = cor(quote_bef), method = 'color', type = 'upper',
                   order = "original", addCoef.col = 'black', number.cex = 0.5)

dev.off() 

Cairo::CairoPNG(filename = "Results/Correlation_quote_after.png", 
                width = 7, height = 7, units = "in", dpi = 300) 

corrplot::corrplot(corr = cor(quote_aft), method = 'color', type = 'upper',
                   order = "original", addCoef.col = 'black', number.cex = 0.5)

dev.off()
