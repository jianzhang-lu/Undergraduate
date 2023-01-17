library(tidyverse)
# Sort the data
data <- depulicate_all
data <- data %>% arrange(chr, start, end, log2FoldChange)
table(data$chr)

# Remove the duplicated scores. 
dup_index <- which(duplicated(data[,c(1:3)], fromLast = T))
if (length(dup_index) != 0){
  data <- data[-dup_index, ]
  }

chr_index <- unique(data$chr)
group <- list()

for (i in 1:length(chr_index)){
  group[[i]] <- data %>% filter(chr == chr_index[i])
}

over <- c()
overlap <- function(data){
  if (nrow(data) > 1){
    for(i in 1:(nrow(data)-1)){
      if(data[i, 3] >= data[i+1, 2]){
        over <- c(over, i)
      }
    }
    return(over)
    }
}

mean(complete.cases(data))

depulicate_all_2 <- data.frame()

for (i in 1:length(group)){
  if (nrow(group[[i]] > 1)){
    depulicate_all_2 <- bind_rows(depulicate_all_2, group[[i]][overlap(group[[i]]),])
    }
}

other <- anti_join(depulicate_all, depulicate_all_2)


write.table(other[,c(1:4)], 
            file = "D:/系统默认/桌面/g0_down_2.bedgraph", 
            quote = F, sep = "\t", row.names = F, col.names = F)

write.table(depulicate_all_2[,c(1:4)], 
            file = "D:/系统默认/桌面/g0_down_3.bedgraph", 
            quote = F, sep = "\t", row.names = F, col.names = F)

