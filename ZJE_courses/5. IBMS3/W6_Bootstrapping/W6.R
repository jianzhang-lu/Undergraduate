# Example 1
## Method 1
number_correct <- vector(mode = "numeric")

nexp <- 10000
for (i in 1:nexp){
  block <- sample(c(0, 1), 50, replace = TRUE)
  correct <- sum(block)
  number_correct <- c(number_correct, correct)
}

hist(number_correct, col = "seagreen2", main = "Null distribution",
     xlab = "Number of correct guesses", ylab = "Number of experiments")
abline(v = 31, col = "midnightblue", lwd = 2)

p = sum(number_correct >= 31) / nexp

## Method 2
all_experiments <- sample(c(0, 1), 50 * nexp, replace = TRUE)
all_experiments <- matrix(all_experiments, ncol = 50)
number_correct <- rowSums(all_experiments)
p = sum(number_correct >= 31) / nexp
p

# Example 2
forearm_data <- read.csv("IBMS3_workshop/W6_Bootstrapping/forearm_length.csv", header=TRUE)

lowx <- min(forearm_data$ForearmLength) - 10
highx <- max(forearm_data$ForearmLength) + 10
hist(forearm_data[forearm_data$Gender == "M", "ForearmLength"],
     col = adjustcolor("orange2", alpha.f = 0.2), xlim = c(lowx, highx),
     xlab = "", ylab = "", main = "M")

hist(forearm_data[forearm_data$Gender == "F", "ForearmLength"],
     col = adjustcolor("turquoise", alpha.f = 0.2), xlim = c(lowx, highx),
     xlab = "Forearm Length (mm)",
     main = "F", ylab = "")

mean_M <- mean(forearm_data[forearm_data$Gender == "M", "ForearmLength"])
mean_F <- mean(forearm_data[forearm_data$Gender == "F", "ForearmLength"])
diff <- abs(mean_M - mean_F)

## Bootstrapping once
n_male <- sum(forearm_data$Gender == "M")
n_female <- sum(forearm_data$Gender == "F")

male <- sample(forearm_data$ForearmLength, n_male, replace = TRUE)
female <- sample(forearm_data$ForearmLength, n_female, replace = TRUE)
lowx <- min(forearm_data$ForearmLength) - 10
highx <- max(forearm_data$ForearmLength) + 10
hist(male,
     col = adjustcolor("orange2", alpha.f = 0.2), xlim = c(lowx, highx),
     xlab = "", ylab = "", main = "M")

hist(female,
     col = adjustcolor("turquoise", alpha.f = 0.2), xlim = c(lowx, highx),
     xlab = "Forearm Length (mm)",
     main = "F", ylab = "")

## Bootstrapping many times
experiments <- 10000
diffs <- vector(mode = "numeric")
for (i in 1:experiments){
  male <- sample(forearm_data$ForearmLength, n_male, replace = TRUE)
  female <- sample(forearm_data$ForearmLength, n_female, replace = TRUE)
  sample_mean_M <- mean(male)
  sample_mean_F <- mean(female)
  sample_diff <- abs(sample_mean_M - sample_mean_F)
  diffs <- c(diffs, sample_diff)
}

xmax <- max(diffs, diff)
hist(diffs, main = "Null distribution", xlab = "absolute difference",
     col = "indianred1", xlim = c(0, xmax + 2))
abline(v = diff, col = "indianred4", lwd = 2)
pval <- sum(diffs >= diff) / experiments

## T-test instead
t.test(ForearmLength ~ Gender, data = forearm_data)



