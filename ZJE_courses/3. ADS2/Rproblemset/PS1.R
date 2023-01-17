student <- rnorm(100, 86, 5)
hist(student, xlab = "grade", col  = "green", breaks = 10)
length(which(student > 91 | student < 81))
length(subset(student, student > 96|student< 76))

past_time = 0
for (i in 1:10000){
  answers = sample(c("A", "B", "C", "D"), 20, replace = T)
  answers2 = sample(rep(c("A", "B", "C", "D"), c(5,5,5,5)), 20, replace = F)
  my_answer_1 = sample(c("A", "B", "C", "D"), 20, replace = T)
  my_answer_2 = rep("A", 20)
  count = 0
  for (i in 1:20){
    if (answers[i] == my_answer_1[i]){
      count = count + 1
    }
  }
  if (count >= 10){
    past_time = past_time + 1
  }

  # if(sum (answers == my_answer_1) >= 10){
  #   count = count + 1
  # }
}
prob = past_time/10000


# random answer and random my answer ===== 0.013 - 0.014.
# random answer and all A answer ===== 0.013 -  0.014.
# average answer and random my answer ===== 0.013 - 0.014
# average answer and all A answer ===== 0 exactly.
