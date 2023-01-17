library(tidyverse)
library(nnet)

ggplot(gather_feature) +
  geom_line(aes(x = feature, y = average, color = factor(number))) +
  facet_wrap(vars(factor(number)))

# 1. Normalize the features
features[,3:58] <- features[,3:58]/255

# 2. Split data into training and validation sets
rows <- sample(1:1000, 700, F)

train_labels <- features[rows, 1] 
valid_labels <- features[-rows, 1] 
train_data <- features[rows, -c(1,2)] 
valid_data <- features[-rows, -c(1,2)]

# 3. Generate an appropriate output representation for a neural network
train_labels_matrix = class.ind(train_labels)

# 4. Train the neural network.
nn = nnet(train_data, train_labels_matrix, size = 4, softmax = TRUE) 

# 5. Predict.
pred_train = predict(nn, train_data, type="class") 
pred_valid = predict(nn, valid_data, type="class") 

# 6. Calculate the accuracy.
mean(pred_train == train_labels)
mean(pred_valid == valid_labels)

# 7. Find the most appropriate size
accuracy_trains <- c()
accuracy_valids <- c()

for(i in 1:12){
  nn = nnet(train_data, train_labels_matrix, size = i, softmax = TRUE) 
  pred_train = predict(nn, train_data, type="class") 
  pred_valid = predict(nn, valid_data, type="class")
  accuracy_trains <- c(accuracy_trains, mean(pred_train == train_labels))
  accuracy_valids <- c(accuracy_valids, mean(pred_valid == valid_labels))
}
plot(accuracy_trains)
plot(accuracy_valids)  


