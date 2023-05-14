# STEP2: Determine the fixed and flexible parameters
library(tidyverse)
library(ggpubr)
library(Cairo)

setwd("CBSB3_workshop/Project/Results")
## 1. 确定要循环的次数和参数范围
# subjectnum = 5000
# Param.df <- data.frame(Subject = 1:subjectnum,
#                        a_schema = runif(subjectnum, 0.01, 10),
#                        h_schema = runif(subjectnum, 10, 3000),
#                        Beta_N = runif(subjectnum, 0.1, 0.7),
#                        Beta_Var= runif(subjectnum, 0.1, 0.4),
#                        a_generic  = runif(subjectnum, 0.01, 10),
#                        h_generic = runif(subjectnum, 10, 3000),
#                        Beta_gN = runif(subjectnum, 0.001, 1),
#                        Beta_gVar = runif(subjectnum, 0.001, 1),
#                        w = runif(subjectnum, 0.1, 0.9),
#                        Phi = runif(subjectnum, 1, 100),
#                        decay_speed = runif(subjectnum, 0.8, 0.999),
#                        decay_speed_thres = runif(subjectnum, 0.9, 0.999),
#                        thres_item_inter  = runif(subjectnum, 0.01, 7.75),
#                        thres_item_final = runif(subjectnum, 7.8, 500),
#                        thres_schema = runif(subjectnum, 7.75, 63),
#                        theta_shift = runif(subjectnum, 1, 77),
#                        timevar = runif(subjectnum, 0.0001, 10),
#                        modeltimestep = runif(subjectnum, 0.001, 0.31))

Param.df <- read.csv("Step1/L/Paras.csv")

## 2. 处理模型结果 将break前后分开
model_data <- read.csv("Step1/L/allresult_processed.csv")[, c(1, 4, 13:27, 30:33)]

### 检查数据是否是跑了subjectnum次 不是的话意味着有参数卡了 需要进一步检查缩小范围
length(unique(model_data$Subject))
success <- unique(model_data$Subject)
all <- unique(Param.df$Subject)
fail <- setdiff(all, success)
Param.df <- Param.df[-fail, ]

model_summary <- model_data %>%
  group_by(Subject, afterbreak) %>%
  summarise_all(mean)
  

model_summary_before <- filter(model_summary, afterbreak == 0)
model_summary_after <- filter(model_summary, afterbreak == 1)


## 3. 为每个参数计算r-value 共18个参数 每个参数有38个r-value(19个PM before & after)
paras <- colnames(Param.df)[-1]
PMs <- colnames(model_summary)[-c(1, 2)]
PM_break_names <- paste0(rep(PMs, each = 2), c('_before', '_after'))
paras_cors <- c()

### all_cors列表包含了所有参数的38个r-value，可以用来后续查看哪个PM的r-value最大
all_cors <- list()

for(i in 2:19){
  para <- Param.df[, i]
  cors <- c()
  for(j in 3:21){
    PM_before <- model_summary_before[, j]
    PM_after <- model_summary_after[, j]
    cor_before <- abs(cor(para, PM_before))
    cor_after <- abs(cor(para, PM_after))
    cors <- c(cors, cor_before, cor_after)
  }

  all_cors[[paras[i-1]]] <- data.frame('Parameters' = PM_break_names,
                                       'Correlations' = cors)
  mean_cor <- mean(cors)
  paras_cors <- c(paras_cors, mean_cor)
}


### 汇总data
Para_cor_final <- data.frame('Parameters' = paras,
                             'Correlations' = paras_cors)
### 从大到小排序
Para_cor_final <- arrange(Para_cor_final, desc(Correlations))

## (Extra) 4. 可以选取其中几个r-value很大参数的可视化一下
top_para <- Para_cor_final$Parameters[1]
filename <- paste0('Step2/Correlation_', top_para, '.png')
top_PM <- arrange(all_cors[[top_para]], desc(Correlations))$Parameters[1]

### X轴：top parameter
X <- Param.df[, top_para]

### Y轴自定义
Y <- model_summary_after[, 'OB_2']


### Y轴：top PM
### 切分字符串 把OB_4_after分成OB_4和after
if(tail(str_split(top_PM, '_')[[1]], 1) == 'before'){
  Y <- model_summary_before[, str_replace(top_PM, '_before', '')]
}else{
  Y <- model_summary_after[, str_replace(top_PM, '_after', '')]
}

data <- data.frame("X" = X,
                   "Y" = Y)
colnames(data) <- c(top_para, top_PM)

### 画图 保存
Cairo::CairoPNG(filename = filename, width = 7, height = 7, units = "in", dpi = 300) 
ggscatter(data, x = top_para, y = top_PM, add = 'reg.line', size = 1,
          add.params = list(color = 'blue', fill = 'lightgray')) +
  stat_cor(method = 'pearson', size = 5)
dev.off() 


## 5. 确定所有fixed parameter values
fixed_paras <- c("a_schema", "h_schema", "Beta_Var", "a_generic",
                 "h_generic", "Beta_gVar", "thres_item_inter", 
                 "timevar", "modeltimestep")
fixed_values <- Param.df[, fixed_paras]


### 得到experiment的PM平均值
expe_data <- read.csv("../experiment_data/painting_summary.csv")[, c(2, 5:16, 21:27)]
expe_summary <- expe_data %>%
  group_by(ID) %>%
  summarise_all(mean)

PM_expe <- expe_summary[, -1] %>%
  summarise_all(mean)

### 计算experiment的PM方差
devs <- c()
for (i in 2:20){
  devs <- c(devs, var(expe_summary[, i]))
}

dev_df <- data.frame('PMs' = colnames(expe_summary)[-1],
                     'Variances' = devs)

Cairo::CairoPNG(filename = "Step2/PM_variance.png", width = 7, height = 7, units = "in", dpi = 300) 
ggplot(dev_df, aes(x = factor(PMs, levels = colnames(expe_summary)[-1]), 
                              y = Variances)) +
  geom_bar(stat = 'identity') +
  labs(x = 'PMs') +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5, size = 10),
        axis.title.x = element_text(size = 15),
        axis.title.y = element_text(size = 15))
  
dev.off()

### 得到model的PM平均值
model_summary <- model_data[, -2] %>%
  group_by(Subject) %>%
  summarise_all(mean) %>%
  select(-1)

### 改名字 便于匹配
colnames(model_summary)[c(13, 14, 16:19)] <- c('payoff', 'accuracy', 
                                               'dwmean_1', 'dwmean_2',
                                               'dwmean_3', 'dwmean_4')
match <- match(colnames(PM_expe), colnames(model_summary))
model_summary <- select(model_summary, all_of(match))


## 6. 调整PM的weight，让所有PM的error分布比较均匀
# weight <- c(0.1, 1, 1, 0.5,
#             1, 1, 1, 1,
#             0.01, 0.01, 0.01, 0.01,
#             1, 1, 1, 1,
#             1, 1, 1)

weight <- c(1, 1, 1, 1,
            1, 1, 1, 1,
            1, 1, 1, 1,
            1, 1, 1, 1,
            1, 1, 1)

PM_error <- data.frame()

### Function to calculate chi-square
### 这里的n指的是取得的第几组参数 比如n=1就是第一行参数

calc_error <- function(n){
  errors <- c()
  PM_model <- model_summary[n, ]
  for(i in 1:19){
    error <- weight[i] * (as.vector(t(((PM_model[, i]-PM_expe[, i])^2)/devs[i])))
    errors <- c(errors, error)
  }
  return(errors)
}

### 对所有run得到的结果计算error 取最小的value
errors <- c()
for(n in 1:nrow(model_summary)){
  one_error <- calc_error(n)
  errors <- c(errors, sum(one_error))
  PM_error <- rbind(PM_error, one_error)
  colnames(PM_error) <- colnames(model_summary)
}

min_index <- which.min(errors)
fixed_result <- fixed_values[min_index, ]

### Fixed_result即为fixed parameter values

### 查看每个PM的error 
PM_error_long <- gather(PM_error, 1:19, key = 'PMs', value = 'Error')

# With all weight equal
# 记得改输出名字是before还是after！！！！！

Cairo::CairoPNG(filename = "Step2/PM_error_after.png", width = 7, height = 7, units = "in", dpi = 300) 
ggplot(PM_error_long, aes(x = factor(PMs, levels = colnames(PM_error)), 
                          y = Error)) +
  geom_boxplot(outlier.shape = NA) +
  scale_y_continuous(limits = c(0, 100)) +
  labs(x = 'PMs') +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, size = 10),
        axis.title.x = element_text(size = 15),
        axis.title.y = element_text(size = 15))
dev.off() 

## 7. 画图证明fixed parameter情况下model和experiment差别
min_fix_para <- fixed_result
min_model <- model_summary[min_index, ]
min_exp <- PM_expe
fix_data <- cbind(t(min_model), t(min_exp))
colnames(fix_data) <- c('Model', 'Experiment')
long_fix_data <- gather(data.frame(fix_data), 'Model', 'Experiment', key = 'Form', value = 'PMs')
long_fix_data$Form <- factor(long_fix_data$Form, levels = c('Experiment', 'Model'))
long_fix_data$PM <- rownames(fix_data)


Cairo::CairoPNG(filename = "Step2/difference.png", width = 7, height = 7, units = "in", dpi = 300) 
ggplot(long_fix_data, aes(x = Form, y = PMs)) +
  geom_point(aes(color = PM), size = 2) +
  geom_line(aes(group = PM), linewidth = 0.7) +
  labs(title = 'Difference between experiment and model data') +
  theme(plot.title = element_text(hjust = 0.5))
dev.off() 


### Plot the error bar
model_error <- model_summary[, c(1, 9:12)]
expe_error <- PM_expe[, c(1, 9:12)]
for(i in 1:ncol(expe_error)){
  model_error[, i] = abs(model_error[, i] - as.vector(t(expe_error[, i])))
}

error_bar_long <- gather(model_error, key = 'PMs', value = 'Difference')

Cairo::CairoPNG(filename = "Step2/Error_bar.png", width = 7, height = 7, units = "in", dpi = 300) 
ggbarplot(error_bar_long, x = "PMs", y = "Difference", 
          add = "mean_sd", width = 0.5, 
          add.params = list(color = "black", size = 1),
          color = "PMs", fill = "PMs", palette = "npg",
          position = position_dodge(0.1))
dev.off() 


### Plot the experimental data (e.g. for OB_1,2,3,4 or for dwell times) 
### and then typical model data on the same graph
data.2 <- expe_summary[, c(2:5)]
data.3 <- expe_summary[, c(10:13)]
data.4 <- gather(data.2, key = 'PMs', value = 'Values')
data.5 <- gather(data.3, key = 'PMs', value = 'Values')
data.4$Type <- 'Experiment'
data.5$Type <- 'Experiment'


data.6 <- model_data[, -2] %>%
  group_by(Subject) %>%
  summarise_all(mean)

data.7 <- data.6[, c(6:9)]
data.8 <- data.6[, c(17:20)]
colnames(data.8) <- colnames(data.3)
data.9 <- gather(data.7, key = 'PMs', value = 'Values')
data.10 <- gather(data.8, key = 'PMs', value = 'Values')
data.9$Type <- 'Model'
data.10$Type <- 'Model'

data_first <- rbind(data.4, data.9)
data_last <- rbind(data.5, data.10)
  
ggplot(data_first, aes(x = PMs, y = Values)) +
  geom_boxplot(aes(fill = Type))

ggplot(data_last, aes(x = PMs, y = Values)) +
  geom_boxplot(aes(fill = Type))
