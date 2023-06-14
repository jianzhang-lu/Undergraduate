library(tidyverse)
library(ggpubr)
library(Cairo)

setwd("CBSB3_workshop/Project/Results")
groups = c('H', 'Hc', 'HL', 'L', 'Lc', 'LH')
type = 'painting' # painting quote

for(group in groups){
  Param.df <- read.csv(paste0("Step3/", type, "/", group, "/Paras.csv"))
  
  ## 处理expe data
  expe_data <- read.csv(paste0("../experiment_data/", type, "_summary.csv"))[, c(2, 5:16, 21:27, 30:31)]
  expe_data_before <- filter(expe_data, type == group, afterbreak == 0)[, c(-21, -22)]
  expe_data_after <- filter(expe_data, type == group, afterbreak == 1)[, c(-21, -22)]
  
  expe_summary_before <- expe_data_before %>%
    group_by(ID) %>%
    summarise_all(mean)
  
  expe_summary_after <- expe_data_after %>%
    group_by(ID) %>%
    summarise_all(mean)
  
  ## 处理model data
  model_data <- read.csv(paste0("Step3/", type, "/", group, "/allresult_processed.csv"))[, c(1, 4, 13:27, 30:33)]
  if(length(unique(model_data$Subject)) < 500){
    success <- unique(model_data$Subject)
    all <- unique(Param.df$Subject)
    fail <- setdiff(all, success)
    Param.df <- Param.df[-fail, ]
  }

  model_summary <- model_data %>%
    group_by(Subject, afterbreak) %>%
    summarise_all(mean)
  
  model_summary <- as.data.frame(model_summary)
  
  ### 改名字 便于匹配
  colnames(model_summary)[c(15, 16, 18:21)] <- c('payoff', 'accuracy', 
                                                 'dwmean_1', 'dwmean_2',
                                                 'dwmean_3', 'dwmean_4')
  match <- match(colnames(expe_summary_before)[-1], colnames(model_summary)[-c(1, 2)])
  
  model_summary_before <- model_summary %>%
    filter(afterbreak == 0) %>% 
    select(-c(1, 2)) %>%
    select(all_of(match))
  
  model_summary_after <- model_summary %>%
    filter(afterbreak == 1) %>% 
    select(-c(1, 2)) %>%
    select(all_of(match))
  
  # 针对before和after分别处理
  ## 计算experiment data的方差
  before_devs <- c()
  after_devs <- c()
  for (i in 2:20){
    before_devs <- c(before_devs, var(expe_summary_before[, i]))
    after_devs <- c(after_devs, var(expe_summary_after[, i]))
  }
  
  PM_expe_before <- expe_summary_before[, -1] %>%
    summarise_all(mean)
  
  PM_expe_after <- expe_summary_after[, -1] %>%
    summarise_all(mean)
  
  # Weight等待确认
  weight <- c(0.1, 1, 1, 0.5,
              1, 1, 1, 1,
              0.01, 0.01, 0.01, 0.01,
              1, 1, 1, 1,
              1, 1, 1)
  
  # weight <- c(1, 1, 1, 1,
  #             1, 1, 1, 1,
  #             1, 1, 1, 1,
  #             1, 1, 1, 1,
  #             1, 1, 1)
  
  # data1是model_summary_before 或者 model_summary_after
  # data2是PM_expe_before 或者 PM_expe_after
  # devs是before_devs或者after_devs
  
  calc_error <- function(n, data1, data2, devs){
    errors <- c()
    PM_model <- data1[n, ]
    for(i in 1:19){
      error <- weight[i] * (as.vector(t(((PM_model[, i]-data2[, i])^2)/devs[i])))
      errors <- c(errors, error)
    }
    return(errors)
  }
  
  ## Before break
  before_errors <- c()
  PM_error_before <- data.frame()
  
  for(n in 1:nrow(model_summary_before)){
    one_error <- calc_error(n, model_summary_before, PM_expe_before, before_devs)
    before_errors <- c(before_errors, sum(one_error))
    PM_error_before <- rbind(PM_error_before, one_error)
    colnames(PM_error_before) <- colnames(model_summary_before)
  }
  
  ## After break
  after_errors <- c()
  PM_error_after <- data.frame()
  
  for(n in 1:nrow(model_summary_after)){
    one_error <- calc_error(n, model_summary_after, PM_expe_after, after_devs)
    after_errors <- c(after_errors, sum(one_error))
    PM_error_after <- rbind(PM_error_after, one_error)
    colnames(PM_error_after) <- colnames(model_summary_after)
  }
  
  ## Draw a plot to show the distribution of errors
  plot_before <- data.frame("Errors" = before_errors)
  plot_after <- data.frame("Errors" = after_errors)
  
  ggplot(plot_before, aes(x = Errors)) +
    geom_density(color = 'red', linewidth = 1.5)
  
  ggplot(plot_after, aes(x = Errors)) +
    geom_density(color = "blue", linewidth = 1.5)
  
  ## Find the top 20 minimal parameter
  before_rank <- order(before_errors)[1:20]
  after_rank <- order(after_errors)[1:20]
  
  before_para <- Param.df[before_rank, ][, -1]
  after_para <- Param.df[after_rank, ][, -1]
  
  
  # ##### 如果到最后一步 则直接输出最小的parameter set
  # before_top <- Param.df[which.min(before_errors), ]
  # after_top <- Param.df[which.min(after_errors), ]
  
  
  ## Generate another Monte Carlo sets
  second_before <- data.frame()
  second_after <- data.frame()
  
  for(i in 1:20){
    first_before <- c(before_para[i, ])
    first_after <- c(after_para[i, ])
    
    add <- data.frame(a_schema = rep(0, 10),
                      h_schema = rep(0, 10),
                      Beta_N = runif(10, -0.06, 0.06),
                      Beta_Var= rep(0, 10),
                      a_generic  = rep(0, 10),
                      h_generic = rep(0, 10),
                      Beta_gN = runif(10, -0.1, 0.1),
                      Beta_gVar = rep(0, 10),
                      w = runif(10, -0.08, 0.08),
                      Phi = runif(10, -10, 10),
                      decay_speed = runif(10, -0.02, 0.02),
                      decay_speed_thres = runif(10, -0.01, 0.01),
                      thres_item_inter  = rep(0, 10),
                      thres_item_final = runif(10, -49, 49),
                      thres_schema = runif(10, -4.725, 4.725),
                      theta_shift = round((runif(10, -7.6, 7.6)), 0),
                      timevar = rep(0, 10),
                      modeltimestep = rep(0, 10))
    
    second_before <- rbind(second_before, first_before+add)
    second_after <- rbind(second_after, first_after+add)
  }
  
  
  final_second_before <- second_before %>%
    filter(Beta_N < 0.7 & Beta_N > 0.1 & 
           Beta_gN < 1 & Beta_gN > 0.001 &
           w < 0.9 & w > 0.1 & 
           Phi > 1 & Phi < 100 & 
           decay_speed < 0.999 & decay_speed > 0.8 &
           decay_speed_thres < 0.999 & decay_speed_thres > 0.9 &
           thres_item_final > 7.8 & thres_item_final < 500 & 
           thres_schema > 7.75 & thres_schema < 55 &
           theta_shift > 1 & theta_shift < 77)
  
  final_second_after <- second_after %>%
    filter(Beta_N < 0.7 & Beta_N > 0.1 & 
             Beta_gN < 1 & Beta_gN > 0.001 &
             w < 0.9 & w > 0.1 & 
             Phi > 1 & Phi < 100 & 
             decay_speed < 0.999 & decay_speed > 0.8 &
             decay_speed_thres < 0.999 & decay_speed_thres > 0.9 &
             thres_item_final > 7.8 & thres_item_final < 500 & 
             thres_schema > 7.75 & thres_schema < 55 &
             theta_shift > 1 & theta_shift < 77)
  
  final_second_before$Subject <- 1:nrow(final_second_before)
  final_second_after$Subject <- 1:nrow(final_second_after)
  
  final_second_before <- select(final_second_before, 19, 1:18)
  final_second_after <- select(final_second_after, 19, 1:18)
  
  ## 输出文件
  output_before <- paste0("Step3/", type, "_2/", group, "/bef_Paras.csv")
  output_after <- paste0("Step3/", type, "_2/", group, "/aft_Paras.csv")
  
  write.csv(final_second_before, output_before, row.names = F)
  write.csv(final_second_after, output_after, row.names = F)
}

