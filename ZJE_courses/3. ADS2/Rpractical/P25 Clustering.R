library(tidyverse)
guests <- read.csv("ADS_practical/guests.csv")

kmeans(guests[,2:3], centers = 4, iter.max = 5)

# 1. K-means clustering
distance <- function(x1,y1,x2,y2){
  return(sqrt((x1-x2)^2 + (y1-y2)^2))
}

cluster <- function(K){
  guests$cluster <- 0
  for(i in 1:K){
    guests[,4+i] <- 0
  }
  centroids_initial <- sample(guests$names, K, F)
  centroids <- filter(guests, names %in% centroids_initial)
  Continue = TRUE
  step = 0
  
  while(Continue){
    step <- step+1
    distances <- list()
    for(i in 1:length(centroids$names)){
      initial_x <- centroids[i,]$age_norm
      initial_y <- centroids[i,]$hours_norm
      dis_ns <- c()
      
      for(j in 1:length(guests$names)){
        data_x <- guests[j,]$age_norm
        data_y <- guests[j,]$hours_norm
        dis_n <- distance(initial_x, initial_y, data_x, data_y)
        dis_ns <- c(dis_ns, dis_n)
      }
      distances[[i]] <- dis_ns
    }
    
    for(num in 1:K){
      guests[,4+num] <- distances[[num]]
    }
    
    ## Assigning each data point to the cluster of its nearest centroid. 
    for(i in 1:length(guests$names)){
      ds <- guests[i,5:(4+K)]
      guests[i,'cluster'] <- which(ds == min(ds))
    }
    
    ## Re-compute a new centroid
    new_cent <- guests %>% group_by(cluster) %>% summarise(cent_x = mean(age_norm),
                                                           cent_y = mean(hours_norm),
                                                           within_var = var(age_norm) + var(hours_norm))
    within_var <- new_cent[,c(1,4)]
    old_cent_x <- centroids$age_norm
    old_cent_y <- centroids$hours_norm
    centroids$age_norm <- new_cent$cent_x
    centroids$hours_norm <- new_cent$cent_y
    if(sum(old_cent_x == new_cent$cent_x) == K & 
       sum(old_cent_y == new_cent$cent_y) == K){
      Continue <- FALSE
    }
  }
  results <- list(guests, step, centroids, within_var)
  return(results)
}

results <- cluster(4)

ggplot() + 
  geom_point(data = results[[1]], 
             aes(x = age_norm, y = hours_norm, color = factor(cluster))) +
  geom_point(data = results[[3]],
             aes(x = age_norm, y = hours_norm), shape = 3, size = 2, colour = "red") +
  labs(x = 'age', y = 'hours', color = 'class')

# 1 more: Finding the best 4-means cluster
vars <- c()
results_total <- c()
for(i in 1:10){
  results <- cluster(4)
  results_total[[i]] <- results
  vars <- c(vars, mean(results[[4]]$within_var, na.rm = T))
}
index <- which(vars == min(vars))
result_final <- results_total[[sample(index, 1)]]
ggplot() + 
  geom_point(data = result_final[[1]], 
             aes(x = age_norm, y = hours_norm, color = factor(cluster))) +
  geom_point(data = result_final[[3]],
             aes(x = age_norm, y = hours_norm), shape = 3, size = 2, colour = "red") +
  labs(x = 'age', y = 'hours', color = 'class')

# 1 more: Is 4-means the answer?
min_vars <- c()
for(K in 1:20){
  vars <- c()
  for(i in 1:10){
    results <- cluster(K)
    vars <- c(vars, mean(results[[4]]$within_var, na.rm = T))
  }
  min_var <- min(vars, na.rm = T)
  min_vars <- c(min_vars, min_var)
}

elbow <- data.frame('K' = 1:19, 'var' = min_vars[1:19])
ggplot(elbow, aes(x = K, y = var)) +
  geom_line() +
  scale_x_continuous(breaks=1:19) +
  labs(title = 'Elbow plot') +
  theme(plot.title = element_text(hjust = 0.5))

# 2. Hierarchical clustering
clust = hclust(dist(guests[,2:3]))
name = guests$names[clust[["order"]]]
plot(clust, xlab='Guest Names', labels=name, horiz=T)


################################################################################
guests$cluster <- 0
all_clusters <- list()
clusters <- list()
all_clusters[[1]] <- guests %>% mutate(cluster = 1:20)

find_guest <- function(index){
  col = index %/% 20 + 1
  row = index %% 20
  if(row == 0){
    row <- 20
    col <- col - 1 
  }
  return(c(row, col))
}
  
distance_ns <- c()
for(i in 1:length(guests$names)){
  x1 = guests[i,]$age_norm
  y1 = guests[i,]$hours_norm
  for(j in 1:length(guests$names)){
    x2 = guests[j,]$age_norm
    y2 = guests[j,]$hours_norm
    distance_n <- distance(x1,y1,x2,y2)
    distance_ns <- c(distance_ns, distance_n)
  }
}

distance_matrix <- matrix(distance_ns, nrow = 20, byrow = T,
                          dimnames = list(1:20, 1:20))
distance_matrix <- na_if(distance_matrix, 0)


for(i in 2:100){
  data <- all_clusters[[i-1]]
  distance_min <- min(unique(sort(distance_matrix)))
  index <- which(distance_matrix == distance_min)[1]
  name1 <- data$names[find_guest(index)[1]]
  name2 <- data$names[find_guest(index)[2]]
  
  min_cluster <- min(data[data$names == name1, "cluster"],
                   data[data$names == name2, "cluster"])
  
  data[data$names == name1, "cluster"] <- min_cluster
  data[data$names == name2, "cluster"] <- min_cluster
  clusters[[i-1]] <- c(name1, name2)
  distance_matrix[find_guest(index)[1], find_guest(index)[2]] <- NA
  distance_matrix[find_guest(index)[2], find_guest(index)[1]] <- NA
  all_clusters[[i]] <- data
}
