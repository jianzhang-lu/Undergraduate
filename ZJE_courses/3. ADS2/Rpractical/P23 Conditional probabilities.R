library(tidyverse)
# 1. Lie detector problem
## By setting up and running a simulation.

detected <- function(total){
  thieves <- 0.1*total
  not_thieves <- 0.9*total
  
  detected_thieves <- sample(c("+", "-"), thieves, T, c(0.8, 0.2))
  detected_not <- sample(c("+", "-"), not_thieves, T, c(0.2, 0.8))
  detect_num <- sum(detected_thieves=="+") + sum(detected_not=="+")
  return(detect_num)
}

total_list <- 10:500
simulation <- replicate(1000, apply(total_list, 1, detected), simplify = T)
rownames(simulation) <- total_list
simulation <- as.data.frame(simulation)

result <- as.data.frame(apply(simulation, 1, mean))
result$total <- as.numeric(rownames(result))

colnames(result)[1] <- "detected"
total <- result[round(result$detected) == 50, "total"]
thief_num <- total*0.1

# 1. Method 2
results <- c()

for(i in 1:1000){
  detected_thieves = 0
  persons <- c()
  
  while (detected_thieves < 50){
    person = ifelse(sample(100,1) <= 10, 'thief', 'not')
    if (person == 'thief'){
      liers_result = ifelse(sample(100,1) <= 80, 'fail', 'pass')
      detect = ifelse(liers_result == 'fail', 1, 0)
    }
    
    else {
      liers_result = ifelse(sample(100,1) > 80, 'fail', 'pass')
      detect = ifelse(liers_result == 'fail', 1, 0)
    }
    
    detected_thieves <- detected_thieves + detect
    persons <- c(persons, person)
  }
  thief_num <- sum(persons == 'thief')
  results <- c(results, thief_num)
}
mean(results)

# 2. Coin toss
steps <- c()

for (i in 1:10000){
  toss = ''
  step = 0
  while (toss != 'HTTH'){
    if(toss == ''){
      s1 = sample(c('H', 'T'), 1)
      toss = ifelse(s1 == 'H', 'H', '')
      step = step + 1
    }
  
    if (toss == 'H'){
      s2 = sample(c('H', 'T'), 1)
      toss = ifelse(s2 == 'T', 'HT', 'H')
      step = step + 1
    }
    
    if (toss == 'HT'){
      s3 = sample(c('H', 'T'), 1)
      toss = ifelse(s3 == 'T', 'HTT', 'H')
      step = step + 1
    }
    
    if (toss == 'HTT'){
      s4 = sample(c('H', 'T'), 1)
      toss = ifelse(s4 == 'H', 'HTTH', '')
      step = step + 1
    }
  }
  steps <- c(steps, step)
}
mean(steps)



N <- c()
coin <- c('H','T')
answer <- 'HTTH'

for(j in 1:10000){
  s <- c()
  i <- 0
  while(TRUE){
    i = i+1
    s = paste0(s, sample(coin, 1))
    if (str_sub(s, -4, -1)==answer){
      break
    }
  }
  N <- c(N, i)
}
mean(N)
