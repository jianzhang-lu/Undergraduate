library(tidyverse)
library(pROC)
library(caret)
library(rpart)
library(rpart.plot)

wdbc <- read.csv("IBMS3_workshop/W7_Classification/WDBC.csv")
complete.cases(wdbc)
ggplot(wdbc, aes(x = radius, y = smoothness)) +
  geom_point(aes(color = diagnosis))

# Creating training and test sets
wdbc$diagnosis <- as.factor(wdbc$diagnosis)
set.seed(123)
num.samples <- nrow(wdbc)
test.id <- sample(1:num.samples, size = 1/3 * num.samples, replace = FALSE)
wdbc.test <- wdbc[test.id, ]
wdbc.train <- wdbc[-test.id, ]

# Set the model
model.logistic <- glm(diagnosis ~ ., data = wdbc.train, family = binomial)
summary(model.logistic)

# Evaluating the model
pr <- predict(model.logistic, wdbc.train, type = "response")
tb <- table(Prediction = ifelse(pr < 0.5, "B", "M"),
            Real = wdbc.train$diagnosis)

accuracy <- (tb[1,1] + tb[2,2]) / sum(tb)
FP <- tb[1,2]/sum(tb)
FN <- tb[2,1]/sum(tb)

pr <- predict(model.logistic, wdbc.test, type = "response")
tb <- table(ifelse(pr < 0.5, "B", "M"), wdbc.test$diagnosis)
accuracy <- (tb[1,1] + tb[2,2]) / sum(tb)
FP <- tb[1,2]/sum(tb)
FN <- tb[2,1]/sum(tb)

# ROC curve
ROC.curve <- roc(wdbc.test$diagnosis,
                 predict(model.logistic, wdbc.test, "response"))

plot(ROC.curve, las = 1)
best.thr <- coords(ROC.curve, "best", transpose = TRUE)

# Try with the new threshold
pr <- predict(model.logistic, wdbc.test, type = "response")
tb.1 <- table(Prediction = ifelse(pr < 0.5, "B", "M"),
              Real = wdbc.test$diagnosis)
tb.2 <- table(Prediction = ifelse(pr < best.thr["threshold"], "B", "M"),
              Real = wdbc.test$diagnosis)

# Cross-validation
train.control <- trainControl(method = "cv", number = 10)
model.logistic.cv <- train(diagnosis ~ ., 
                           data = wdbc,
                           trControl = train.control,
                           method = "glm", 
                           family = binomial)
print(model.logistic.cv)
model.logistic.cv$resample$Accuracy

# Trees and Random Forest
model.tree <- rpart(diagnosis ~ ., wdbc.train)
rpart.plot(model.tree)


