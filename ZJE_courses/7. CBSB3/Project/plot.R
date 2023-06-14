library(tidyverse)
library(ggpubr)
library(Cairo)

data <- read.csv("CBSB3_workshop/Project/Final.csv")[, c(1, 4, 8, 10, 11, 12, 13, 15, 16, 17)]
data$group <- as.factor(data$group)

data1 <- data[, -1]
data1$state <- rep(c('Before', 'After'), 12)
data1_bef <- filter(data1, state == 'Before')
data1_after <- filter(data1, state == 'After')

data2 <- data[, -1]
data2$type <- rep(c('Painting', 'Quote'), each = 12)




data1_long <- gather(data1, -10, key = 'Parameters', value = 'Values')
data2_long <- gather(data2, -10, key = 'Parameters', value = 'Values')

data1_long$state <- factor(data1_long$state, levels = c('Before', 'After'))
Cairo::CairoPNG(filename = "CBSB3_workshop/Project/Results/Step3/group.png", width = 7, height = 7, units = "in", dpi = 300) 
ggplot(data1_long, aes(x = state, y = Values)) +
  geom_boxplot(aes(fill = Parameters)) +
  theme(text = element_text(size = 15)) +
  labs(title = '(A)')
dev.off()

Cairo::CairoPNG(filename = "CBSB3_workshop/Project/Results/Step3/type.png", width = 7, height = 7, units = "in", dpi = 300) 
ggplot(data2_long, aes(x = type, y = Values)) +
  geom_boxplot(aes(fill = Parameters)) +
  theme(text = element_text(size = 15)) +
  labs(title = '(B)')
dev.off()


data_long <- gather(data, -1, key = 'Parameters', value = 'Values')


data_long_set1 <- filter(data_long, Parameters == 'Beta_N')
data_long_set1$group <- factor(data_long_set1$group, 
                              levels = data_long_set1$group)

data_long_set2 <- filter(data_long, Parameters == 'Beta_gN')
data_long_set2$group <- factor(data_long_set2$group, 
                              levels = data_long_set2$group)

data_long_set3 <- filter(data_long, Parameters == 'w')
data_long_set3$group <- factor(data_long_set3$group, 
                              levels = data_long_set3$group)

data_long_set4 <- filter(data_long, Parameters == 'Phi')
data_long_set4$group <- factor(data_long_set4$group, 
                              levels = data_long_set4$group)

data_long_set5 <- filter(data_long, Parameters == 'decay_speed')
data_long_set5$group <- factor(data_long_set5$group, 
                              levels = data_long_set5$group)

data_long_set6 <- filter(data_long, Parameters == 'decay_speed_thres')
data_long_set6$group <- factor(data_long_set6$group, 
                              levels = data_long_set6$group)

data_long_set7 <- filter(data_long, Parameters == 'thres_item_final')
data_long_set7$group <- factor(data_long_set7$group, 
                              levels = data_long_set7$group)

data_long_set8 <- filter(data_long, Parameters == 'thres_schema')
data_long_set8$group <- factor(data_long_set8$group, 
                              levels = data_long_set8$group)

data_long_set9 <- filter(data_long, Parameters == 'theta_shift')
data_long_set9$group <- factor(data_long_set9$group, 
                               levels = data_long_set9$group)


Cairo::CairoPNG(filename = "CBSB3_workshop/Project/Results/Step3/Beta_N.png", width = 7, height = 7, units = "in", dpi = 300) 
ggplot(data_long_set1, aes(x = group, y = Values)) +
  geom_point(size = 2) +
  theme(text = element_text(size = 15), 
        axis.text.x = element_text(angle = 90, hjust = 1, 
                                   vjust = 0.5, size = 10)) +
  labs(y = 'Beta_N', title = "(C)")
dev.off()

Cairo::CairoPNG(filename = "CBSB3_workshop/Project/Results/Step3/w.png", width = 7, height = 7, units = "in", dpi = 300) 
ggplot(data_long_set3, aes(x = group, y = Values)) +
  geom_point(size = 2) +
  theme(text = element_text(size = 15), 
        axis.text.x = element_text(angle = 90, hjust = 1, 
                                   vjust = 0.5, size = 10)) +
  labs(y = 'w', title = '(D)')
dev.off()

Cairo::CairoPNG(filename = "CBSB3_workshop/Project/Results/Step3/decay_speed.png", width = 7, height = 7, units = "in", dpi = 300) 
ggplot(data_long_set5, aes(x = group, y = Values)) +
  geom_point(size = 2) +
  theme(text = element_text(size = 15), 
        axis.text.x = element_text(angle = 90, hjust = 1, 
                                   vjust = 0.5, size = 10)) +
  labs(y = 'decay_speed', title = '(E)')
dev.off()


Cairo::CairoPNG(filename = "CBSB3_workshop/Project/Results/Step3/thres_schema.png", width = 7, height = 7, units = "in", dpi = 300) 
ggplot(data_long_set8, aes(x = group, y = Values)) +
  geom_point(size = 2) +
  theme(text = element_text(size = 15), 
        axis.text.x = element_text(angle = 90, hjust = 1, 
                                   vjust = 0.5, size = 10)) +
  labs(y = 'thres_schema', title = '(F)')
dev.off()
