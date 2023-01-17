from sklearn.decomposition import PCA
from numpy.linalg import svd, eigh
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import pickle

# row: 500 cells  col: 1000 genes.
X = pd.read_csv("data.tsv", sep="\t", header=None).to_numpy()[:, :1000]
cells = np.shape(X)[0]
features = np.shape(X)[1]

# 1. Calculate the mean of each dimension.
## Xbar = X.T.mean(1)
## Xbar = np.mean(X, axis=0)

Xbar = np.zeros(features)
for i in range(features):
    a = np.mean(X[:, i])
    Xbar[i] = a

# 2. Obtain the centralized matrix
B = X - Xbar

# 3. Perform PCA with first 10 dimensions via eigen decomposition
C = np.dot(B.T, B)/(cells-1)
## eigh返回特征值(list)和特征向量
eigen_value, eigen_vector = eigh(C)
print(eigen_value)
pc = 10
PCA_decomposition = np.dot(B, eigen_vector[:, 0:pc])
print(np.shape(PCA_decomposition))
print(PCA_decomposition)

# 4. Perform PCA with first 10 dimensions via SVD
## B = U(PC$rotation) * Singular values * V.T(PC$x)
U, Singular_values, VT = svd(B)
V = VT.T
PCA_SVD = np.dot(B, V[:, 0:pc])
print(np.shape(PCA_SVD))
print(PCA_SVD)
## PCA(pc).fit_transform(B)

# 5. Calculate the explained variance ratio of top 10 PCs using eigen decomposition or SVD
eigen_value2 = eigen_value[::-1]
eig_sum = np.sum(eigen_value2)
explained_ratio_eig = [eigen_value2[i]/eig_sum for i in range(20)]
plt.scatter(range(20), explained_ratio_eig)
plt.show()

Singular_values_square = np.power(Singular_values, 2)
SVD_sum = np.sum(Singular_values_square)
explained_ratio_SVD = [Singular_values_square[i]/SVD_sum for i in range(20)]
plt.scatter(range(20), explained_ratio_SVD)
plt.show()


# Image compression using PCA
with open("lion.npy", "rb") as f:
    img = pickle.load(f)
print(img.shape)
plt.imshow(img, cmap="gray")

## Decentralize the image matrix
Xbar = np.mean(img, axis=0)
B = img - Xbar
plt.imshow(B, cmap="gray")

fig, ax = plt.subplots(1, 6)
fig.set_size_inches(60, 10)
U, S, VT = svd(B)
V = VT.T

for idx, pc in enumerate([100, 50, 20, 10, 5, 2]):
    Z = np.dot(B, V[:, 0:pc])
    R = np.dot(Z, VT[0:pc, :])
    ax[idx].imshow(R, cmap='gray')
plt.show()
