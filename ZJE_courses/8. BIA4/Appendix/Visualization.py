"""
Created on 2023/11/17

This file is used to draw some plots for visualization in the summary report.
e.g. The heatmaps for HyperTuning results;
     The Loss and Metrics during the epochs
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pickle
from skimage import io
from scipy.io import matlab
from skimage.transform import resize
from skimage.exposure import equalize_adapthist
# Need dependency 'openpyxl'

############################################## U-Net Part (Segmentation) ##############################################
## 1. Test the effect of data pre-processing
image = io.imread("../data/ORIGA/001.jpg")
mask = matlab.loadmat("../data/Semi-automatic-annotations/001.mat")['mask']

resized_image = resize(image, (256, 256, 3), mode='reflect', preserve_range=True)
normalized_image = resized_image.astype('float32')/255.0

contrast_enhanced_image = np.zeros_like(normalized_image)
for channel in range(normalized_image.shape[2]):
    contrast_enhanced_image[:, :, channel] = equalize_adapthist(normalized_image[:, :, channel])

resized_mask = resize(mask, (256, 256), order=0, mode='reflect', preserve_range=True)

binary_mask = (resized_mask > 0).astype('float32')

fig, ax = plt.subplots(2, 3, figsize=(12, 8))
for i in ax.ravel():
    i.axis('off')

ax[0, 0].imshow(image)
ax[0, 0].set_title("Original Image", fontsize=20)

ax[0, 1].imshow(normalized_image)
ax[0, 1].set_title("Resized Image", fontsize=20)

ax[0, 2].imshow(contrast_enhanced_image)
ax[0, 2].set_title("Enhanced Image", fontsize=20)

ax[1, 0].imshow(mask, cmap='gray')
ax[1, 0].set_title("Original Mask", fontsize=20)

ax[1, 1].imshow(resized_mask, cmap='gray')
ax[1, 1].set_title("Resized Mask", fontsize=20)

ax[1, 2].imshow(binary_mask, cmap='gray')
ax[1, 2].set_title("Binary Mask", fontsize=20)

plt.show()

## 2. HyperTuning Results for the segmentation part (Heatmap)
# Load the data from the Excel file
file_path = 'Segmentation/Results/HyperTune.xlsx'
data = pd.read_excel(file_path)

metrics = ['train_loss', 'train_IoU', 'train_F1_score',
           'val_loss', 'val_IoU', 'val_F1_score']
title = ['Training Loss', 'Training IoU', 'Training F1 Score',
         'Validation Loss', 'Validation IoU', 'Validation F1 Score']
big_title = ["Heatmap of " + t + " by Drop Probability and Learning Rate" for t in title]

# The index can be set to 0~5 to see different heatmaps
# (train_loss, train_IoU, train_F1_score, val_loss, val_IoU, val_F1_score)
index = 0

# Create a pivot table for the heatmap
plt.figure(figsize=(12, 10))
pivot_table = data.pivot_table(index="drop_p", columns="learning_rate", values=metrics[index])
ax = sns.heatmap(pivot_table, annot=True, fmt=".3f", cmap="YlGnBu",
                 linewidths=.5, linecolor=None, annot_kws={"size": 20})
ax.set_title(big_title[index], fontsize=18)
ax.set_xlabel("Learning Rate", fontsize=25, labelpad=30)
ax.set_ylabel("Drop Probability", fontsize=25, labelpad=30)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
cbar = ax.collections[0].colorbar
cbar.set_label(title[index], fontsize=25, labelpad=20)
cbar.ax.tick_params(labelsize=18)
plt.show()


## 3. Train Loss, Validation Loss during epochs
with open('Segmentation/Results/trainHistoryDict.txt', 'rb') as file_pi:
    history = pickle.load(file_pi)

plt.figure(figsize=(20, 5))
plt.subplot(1, 4, 1)
plt.plot(history['loss'], color='blue', label='Training loss')
plt.plot(history['val_loss'], color='orange', label='Validation loss')
plt.legend()
plt.title('Loss')

plt.subplot(1, 4, 2)
plt.plot(history['accuracy'], color='blue', label='Training accuracy')
plt.plot(history['val_accuracy'], color='orange', label='Validation accuracy')
plt.ylim(0.965, 1)
plt.legend()
plt.title('Accuracy')

plt.subplot(1, 4, 3)
plt.plot(history['IoU_cal'], color='blue', label='Training IoU')
plt.plot(history['val_IoU_cal'], color='orange', label='Validation IoU')
plt.ylim(0, 1)
plt.legend()
plt.title('IoU')

plt.subplot(1, 4, 4)
plt.plot(history['f1_score'], color='blue', label='Training F1 Score')
plt.plot(history['val_f1_score'], color='orange', label='Validation F1 Score')
plt.ylim(0, 1)
plt.legend()
plt.title('F1 Score')

plt.show()


############################################ Xception Part (Classification) ############################################
## 1. HyperTuning Results for the classification part (Heatmap)
# Load the data from the Excel file
file1 = 'Classification/Results/Original/HyperTune_Xception_whole.xlsx'
file2 = 'Classification/Results/Cropped/HyperTune_Xception_crop.xlsx'
data1 = pd.read_excel(file1)
data2 = pd.read_excel(file2)

metrics = ['train_loss', 'train_accuracy', 'train_AUC', 'train_F1_score',
           'val_loss', 'val_accuracy', 'val_AUC', 'val_F1_score']
title = ['Training Loss', 'Training Accuracy', 'Training AUC Value', 'Training F1 Score',
         'Validation Loss', 'Validation Accuracy', 'Validation AUC Value', 'Validation F1 Score']
big_title = ["Heatmap of " + t + " by Regularization and Learning Rate" for t in title]

# The index can be set to 0~7 to see different heatmaps
index = 6

pivot_table1 = data1.pivot_table(index="regularization", columns="learning_rate", values=metrics[index])
pivot_table2 = data2.pivot_table(index="regularization", columns="learning_rate", values=metrics[index])

# Create a pivot table for the heatmap
plt.figure(figsize=(28, 12))
plt.subplot(1, 2, 1)
ax = sns.heatmap(pivot_table1, annot=True, fmt=".3f", cmap="YlGnBu",
                 linewidths=.5, linecolor=None, annot_kws={"size": 20})
ax.set_title(big_title[index], fontsize=18)
ax.set_xlabel("Learning Rate", fontsize=25, labelpad=30)
ax.set_ylabel("Regularization", fontsize=25, labelpad=30)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
cbar = ax.collections[0].colorbar
cbar.set_label(title[index], fontsize=25, labelpad=20)
cbar.ax.tick_params(labelsize=18)

plt.subplot(1, 2, 2)
ax = sns.heatmap(pivot_table2, annot=True, fmt=".3f", cmap="YlGnBu",
                 linewidths=.5, linecolor=None, annot_kws={"size": 20})
ax.set_title(big_title[index], fontsize=18)
ax.set_xlabel("Learning Rate", fontsize=25, labelpad=30)
ax.set_ylabel("Regularization", fontsize=25, labelpad=30)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
cbar = ax.collections[0].colorbar
cbar.set_label(title[index], fontsize=25, labelpad=20)
cbar.ax.tick_params(labelsize=18)

plt.show()

## 2. Train Loss, Validation Loss during epochs
with open('Classification/Results/Original/trainHistoryDict_1.txt', 'rb') as file_pi:
    history1 = pickle.load(file_pi)

with open('Classification/Results/Cropped/trainHistoryDict_2.txt', 'rb') as file_pi:
    history2 = pickle.load(file_pi)

plt.figure(figsize=(20, 10))
plt.subplot(2, 4, 1)
plt.plot(history1['loss'], color='blue', label='Training loss')
plt.plot(history1['val_loss'], color='orange', label='Validation loss')
plt.ylim(0.35, 1)
plt.legend()
plt.title('Loss (Whole Fundus)')

plt.subplot(2, 4, 2)
plt.plot(history1['accuracy'], color='blue', label='Training accuracy')
plt.plot(history1['val_accuracy'], color='orange', label='Validation accuracy')
plt.ylim(0.66, 0.86)
plt.legend()
plt.title('Accuracy (Whole Fundus)')

plt.subplot(2, 4, 3)
plt.plot(history1['auc_1'], color='blue', label='Training AUC')
plt.plot(history1['val_auc_1'], color='orange', label='Validation AUC')
plt.ylim(0, 1)
plt.legend()
plt.title('AUC (Whole Fundus)')

plt.subplot(2, 4, 4)
plt.plot(history1['f1_score'], color='blue', label='Training F1 Score')
plt.plot(history1['val_f1_score'], color='orange', label='Validation F1 Score')
plt.ylim(0, 1)
plt.legend()
plt.title('F1 Score (Whole Fundus)')

plt.subplot(2, 4, 5)
plt.plot(history2['loss'], color='blue', label='Training loss')
plt.plot(history2['val_loss'], color='orange', label='Validation loss')
plt.ylim(0.35, 1)
plt.legend()
plt.title('Loss (Cropped OD)')

plt.subplot(2, 4, 6)
plt.plot(history2['accuracy'], color='blue', label='Training accuracy')
plt.plot(history2['val_accuracy'], color='orange', label='Validation accuracy')
plt.ylim(0.66, 0.86)
plt.legend()
plt.title('Accuracy (Cropped OD)')

plt.subplot(2, 4, 7)
plt.plot(history2['auc_1'], color='blue', label='Training AUC')
plt.plot(history2['val_auc_1'], color='orange', label='Validation AUC')
plt.ylim(0, 1)
plt.legend()
plt.title('AUC (Cropped OD)')

plt.subplot(2, 4, 8)
plt.plot(history2['f1_score'], color='blue', label='Training F1 Score')
plt.plot(history2['val_f1_score'], color='orange', label='Validation F1 Score')
plt.ylim(0, 1)
plt.legend()
plt.title('F1 Score (Cropped OD)')
plt.show()
