import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'Arial'
matplotlib.rcParams['font.size'] = '16'

# 生成train数据和test数据
spring = pd.read_csv("SPRING.tsv", sep="\t")
index1 = np.random.choice(spring.index, 5000)
train_data = spring.iloc[index1, :2].to_numpy()
train_label = np.array(list(spring.iloc[index1, 2]))

spring_test = spring.iloc[~index1, :]
spring_test.index = range(len(spring_test))
index2 = np.random.choice(spring_test.index, 100)
test_data = spring_test.iloc[index2, :2].to_numpy()
validation_label = spring_test.iloc[index2, 2]
print(train_data.shape)
print(test_data.shape)

# 初始化图
def colors(categories):
    cm_dict = dict(zip(categories, [plt.cm.tab10(i/float(len(categories)-1)) for i in range(len(categories))]))
    return cm_dict


cm_dict = colors(np.unique(spring.iloc[:, 2]))

fig, axes = plt.subplots(1, 2)
fig.set_size_inches(10, 5)
axes[0].scatter(train_data[:, 0], train_data[:, 1],
                c=list(map(lambda x: cm_dict[x], spring.iloc[index1, 2])), s=2)
axes[0].set_title("Train data")
axes[1].scatter(test_data[:, 0], test_data[:, 1], s=2, c="k")
axes[1].set_title("Test data")
# plt.show()

# KNN class
## np.argsort(a) 返回的是元素值从小到大排序后的索引值的数组
class KNN:
    def __init__(self, train_data, train_label):
        self.train_data = train_data
        self.train_label = train_label

    def distance(self, p1, p2):
        return np.sqrt(np.sum(np.square(p2 - p1)))

    def fit(self, test_data, n_neighbors):
        """
        @arg test_data test data.dimension should be the same as train_data
        @arg n_neighbors n neighbors to use
        @return a list of the labels of the test data
        """
        labels = []
        for test_point in test_data:
            distances = []
            # candidates字典记录了某个test point的neighbors中每个label的个数
            candidates = {}
            for train_point in self.train_data:
                distances.append(self.distance(test_point, train_point))
            dis_sort = np.argsort(distances)[0:n_neighbors]
            neigh_labels = self.train_label[dis_sort]

            for i in neigh_labels:
                if i not in candidates:
                    candidates[i] = 1
                else:
                    candidates[i] += 1

            # 找到candidates中数目最多的label
            for i in candidates:
                if candidates[i] == max(list(candidates.values())):
                    labels.append(i)
                    break
        return labels


knn = KNN(train_data, train_label)
test_labels = knn.fit(test_data, 5)
fig, axes = plt.subplots(1, 2)
fig.set_size_inches(10, 5)
axes[0].scatter(train_data[:, 0], train_data[:, 1],
                c=list(map(lambda x: cm_dict[x], spring.iloc[index1, 2])), s=2)
axes[0].set_title("Train data")

axes[1].scatter(test_data[:, 0], test_data[:, 1],
                s=4, c=list(map(lambda x: cm_dict[x], test_labels)))
axes[1].set_title("Test data")
plt.show()

print("Number of correct label: %d out of %d"
      % (len(list(filter(lambda x: x[0] == x[1],
                         zip(test_labels, validation_label)))),
         len(test_labels)))

