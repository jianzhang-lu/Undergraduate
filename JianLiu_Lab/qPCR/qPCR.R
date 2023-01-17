library(tidyverse)
library(ggsignif)
se <- function(x){
  sd(x)/sqrt(length(x))
}

data <- read.csv("D:/R_document/实验室/RNA_relative/datalab.csv")
colnames(data)[1] <- "Group"
data[3:9] <- 2^(-data[3:9])
data2 <- data
data3 <- data
data2$Group <- factor(data2$Group, levels = c("2M","14M"))

mean_index <- c()
for(i in 3:9){
  smean <- mean(data[,i][1:4], na.rm = T)
  mean_index <- c(mean_index, smean)
}

for(j in 3:9){
  for(i in 1:4){
    data2[,j][i+4] <- data2[,j][i+4]/mean_index[j-2]
    data2[,j][i] <- data2[,j][i]/mean_index[j-2]
    }
}

sdata <- list()
for(i in 1:7){
  sdata[[i]] <- data.frame("Group" = c("2M", "14M"), 
                        "value" = c(mean(data2[,i+2][1:4], na.rm = T), mean(data2[,i+2][5:8], na.rm = T)))
  sdata[[i]]$Group <- factor(sdata[[i]]$Group, levels = c("2M","14M"))
}

p_value <- list()
for(i in 1:7){
  p_value[[i]] <- t.test(data2[,i+2][1:4], data2[,i+2][5:8])$p.value
}

se1 <- list()
se2 <- list()
for(i in 1:7){
  se1[[i]] <- se(na.omit(data2[,i+2][1:4]))
  se2[[i]] <- se(na.omit(data2[,i+2][5:8]))
}

sd(data2$PLAU[1:4])
sd(data2$PLAU[5:8], na.rm = T)
power.t.test(delta = abs(mean(data2$PLAU[1:4], na.rm = T)-mean(data2$PLAU[5:8], na.rm = T)),
             sig.level = 0.05,
             power = 0.8,
             type = "two.sample",
             sd = 1.849668,
             alternative = "two.sided")


p1 <- ggplot(sdata[[1]], aes(x = Group, y = value)) +
  geom_bar(aes(fill = Group), stat = "identity", width = 0.3) +
  geom_errorbar(ymax = c(sdata[[1]]$value[1] + se1[[1]], sdata[[1]]$value[2]+se2[[1]]), 
                ymin = c(sdata[[1]]$value[1] - se1[[1]], sdata[[1]]$value[2]-se2[[1]]), 
                width = 0.15) +
  geom_signif(comparisons = list(c("2M","14M")), 
              annotations = paste0("p=", round(p_value[[1]],3)),
              y_position = 4.8) +
  labs(title = "小鼠肺组织中CXCL10的相对表达量", 
       x = "CXCL10", y = "Relative RNA Level", fill = "CXCL10") +
  scale_y_continuous(limits=c(0,5))
ggsave("CXCL10.png",p1)


  
p2 <- ggplot(sdata[[2]], aes(x = Group, y = value)) +
  geom_bar(aes(fill = Group), stat = "identity", width = 0.3) +
  geom_errorbar(ymax = c(sdata[[2]]$value[1] + se1[[2]], sdata[[2]]$value[2]+se2[[2]]), 
                ymin = c(sdata[[2]]$value[1] - se1[[2]], sdata[[2]]$value[2]-se2[[2]]), 
                width = 0.15) +
  geom_signif(comparisons = list(c("2M","14M")), 
              annotations = paste0("p=", round(p_value[[2]],3)),
              y_position = 4.8) +
  labs(title = "小鼠肺组织中RGN的相对表达量", 
       x = "RGN", y = "Relative RNA Level", fill = "RGN") +
  scale_y_continuous(limits=c(0,5))
ggsave("RGN.png", p2)

p3 <- ggplot(sdata[[3]], aes(x = Group, y = value)) +
  geom_bar(aes(fill = Group), stat = "identity", width = 0.3) +
  geom_errorbar(ymax = c(sdata[[3]]$value[1] + se1[[3]], sdata[[3]]$value[2]+se2[[3]]), 
                ymin = c(sdata[[3]]$value[1] - se1[[3]], sdata[[3]]$value[2]-se2[[3]]), 
                width = 0.15) +
  geom_signif(comparisons = list(c("2M","14M")), 
              annotations = paste0("p=", round(p_value[[3]],3)),
              y_position = 4.8) +
  labs(title = "小鼠肺组织中Calr的相对表达量", 
       x = "Calr", y = "Relative RNA Level", fill = "Calr") +
  scale_y_continuous(limits=c(0,5))
ggsave("Calr.png", p3)

p4 <- ggplot(sdata[[4]], aes(x = Group, y = value)) +
  geom_bar(aes(fill = Group), stat = "identity", width = 0.3) +
  geom_errorbar(ymax = c(sdata[[4]]$value[1] + se1[[4]], sdata[[4]]$value[2]+se2[[4]]), 
                ymin = c(sdata[[4]]$value[1] - se1[[4]], sdata[[4]]$value[2]-se2[[4]]), 
                width = 0.15) +
  geom_signif(comparisons = list(c("2M","14M")), 
              annotations = paste0("p=", round(p_value[[4]],3)),
              y_position = 4.8) +
  labs(title = "小鼠肺组织中PLAU的相对表达量", 
       x = "PLAU", y = "Relative RNA Level", fill = "PLAU") +
  scale_y_continuous(limits=c(0,5))
ggsave("PLAU.png", p4)

p5 <- ggplot(sdata[[5]], aes(x = Group, y = value)) +
  geom_bar(aes(fill = Group), stat = "identity", width = 0.3) +
  geom_errorbar(ymax = c(sdata[[5]]$value[1] + se1[[5]], sdata[[5]]$value[2]+se2[[5]]), 
                ymin = c(sdata[[5]]$value[1] - se1[[5]], sdata[[5]]$value[2]-se2[[5]]), 
                width = 0.15) +
  geom_signif(comparisons = list(c("2M","14M")), 
              annotations = paste0("p=", round(p_value[[5]],3)),
              y_position = 4.8) +
  labs(title = "小鼠肺组织中sRAGE的相对表达量", 
       x = "sRAGE", y = "Relative RNA Level", fill = "sRAGE") +
  scale_y_continuous(limits=c(0,5))
ggsave("sRAGE.png", p5)

p6 <- ggplot(sdata[[6]], aes(x = Group, y = value)) +
  geom_bar(aes(fill = Group), stat = "identity", width = 0.3) +
  geom_errorbar(ymax = c(sdata[[6]]$value[1] + se1[[6]], sdata[[6]]$value[2] + se2[[6]]), 
                ymin = c(sdata[[6]]$value[1] - se1[[6]], sdata[[6]]$value[2] - se2[[6]]), 
                width = 0.15) +
  geom_signif(comparisons = list(c("2M","14M")), 
              annotations = paste0("p=", round(p_value[[6]],3)),
              y_position = 4.8) +
  labs(title = "小鼠肺组织中Growth.Hormone的相对表达量", 
       x = "Growth.Hormone", y = "Relative RNA Level", fill = "Growth.Hormone") +
  scale_y_continuous(limits=c(0,5))
ggsave("Growth.Hormone.png", p6)

p7 <- ggplot(sdata[[7]], aes(x = Group, y = value)) +
  geom_bar(aes(fill = Group), stat = "identity", width = 0.3) +
  geom_errorbar(ymax = c(sdata[[7]]$value[1] + se1[[7]], sdata[[7]]$value[2] + se2[[7]]), 
                ymin = c(sdata[[7]]$value[1] - se1[[7]], sdata[[7]]$value[2] - se2[[7]]), 
                width = 0.15) +
  geom_signif(comparisons = list(c("2M","14M")), 
              annotations = paste0("p=", round(p_value[[7]],3)),
              y_position = 4.8) +
  labs(title = "小鼠肺组织中Agrin的相对表达量", 
       x = "Agrin", y = "Relative RNA Level", fill = "Agrin") +
  scale_y_continuous(limits=c(0,5))
ggsave("Agrin.png", p7)

