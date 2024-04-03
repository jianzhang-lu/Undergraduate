"""
Created on 2023/12/1
Modified on 2023/12/2 (Add the evaluation of combined model)

This class is used to evaluate our two Xception models on the test dataset
Note that the Xception model used for cropped image is also tested using another whole dataset (ACRIMA)
"""

import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from sklearn.metrics import roc_curve, auc, confusion_matrix
from skimage import io
from skimage.transform import resize
from skimage.exposure import equalize_adapthist
import os
import keras


def process_ACRIMA(image_dir):
    """
    @brief:
        Pre-process the images from ACRIMA dataset and generate the label of these images.
        All images are used to evaluate the Xception model for cropped OD images.
    @args:
        image_dir: The directory of all images
    @returns:
        The x and y for testing the model (restore in .npy files for further usage)
    """

    print("--------------------------------------")
    print("Start Data Pre-processing (ACRIMA)")
    print("--------------------------------------")

    # Generate the images (the x)
    preprocessed_images = []
    labels = []
    for file in os.listdir(image_dir):
        image = io.imread(os.path.join(image_dir, file))
        # Resize images to (256, 256)
        resized_image = resize(image, (256, 256, 3), mode='reflect', preserve_range=True)
        # Normalize images to [0, 1]
        normalized_image = resized_image.astype('float32')/255.0
        # Enhance contrast using CLAHE. Applied to each channel individually
        contrast_enhanced_image = np.zeros_like(normalized_image)
        for channel in range(normalized_image.shape[2]):
            contrast_enhanced_image[:, :, channel] = equalize_adapthist(normalized_image[:, :, channel])
        preprocessed_images.append(contrast_enhanced_image)

        # Generate the labels (the y)
        # Check if the file name contains '_g_' which indicates a glaucoma image
        if '_g_' in file:
            labels.append(1)  # 1 for glaucoma
        else:
            labels.append(0)  # 0 for normal
    y_test = keras.utils.to_categorical(labels, 2)

    # Restore these information into .npy files
    np.save('Results/ACRIMA/x_test.npy', preprocessed_images)
    np.save('Results/ACRIMA/y_test.npy', y_test)

    print("Finish Data Pre-processing (ACRIMA)")
    print("--------------------------------------")
    return None


class ModelEvaluator:
    """
    A class for model evaluation

    :attribute model: The trained model (*.h5)
    """
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def Xception_evaluate(self, x_test, y_test):
        """
        @brief:
            Evaluate the model performance using the test images from ORIGA dataset.
        @args:
            x_test: The test images
            y_test: The categorical form of test images
        @returns:
            The confusion matrix of the model
            The output of the model (The probabilities of each class)
            The true label
        """

        # Convert the categorical form into the labels
        labels = np.argmax(y_test, axis=1)
        # Predict the probabilities of each class
        probabilities = self.model.predict(x_test)
        predictions = np.argmax(probabilities, axis=1)
        return confusion_matrix(labels, predictions), probabilities, labels

    def ROC_curve(self, x_test, y_test, name: str):
        """
        @brief:
            Plot the ROC curve to show the performance of the model
        @args:
            x_test: The test images
            y_test: The categorical form of test images
            name: Should be 'Whole Fundus', 'Cropped OD',
                  or 'ACRIMA Dataset' to show which model is being evaluated.
        @returns:
            A ROC curve to show the performance
        """

        _, probabilities, labels = self.Xception_evaluate(x_test, y_test)
        fpr, tpr, thresholds = roc_curve(labels, probabilities[:, 1])
        # Compute AUC (Area under the ROC Curve)
        roc_auc = auc(fpr, tpr)

        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC curve for ' + name)
        plt.legend(loc="lower right")
        plt.show()


# 1. Pre-process the ACRIMA dataset
# NOTE that you need to run the following codes and restore the data loading files (.npy)
# if you want to evaluate the model using ACRIMA dataset.

process_ACRIMA('../../data/ACRIMA')


# 2. Evaluate the model for Whole Fundus (ORIGA)
evaluator1 = ModelEvaluator('../../model-Xception-best-1.h5')
x_test1 = np.load('Results/Original/x_test.npy')
y_test1 = np.load('Results/Original/y_test.npy')
matrix1, probabilities1, labels1 = evaluator1.Xception_evaluate(x_test1, y_test1)
evaluator1.ROC_curve(x_test1, y_test1, 'Whole Fundus')
print(matrix1)


# 3. Evaluate the model for Cropped OD (ORIGA)
evaluator2 = ModelEvaluator('../../model-Xception-best-2.h5')
x_test2 = np.load('Results/Cropped/x_test.npy')
y_test2 = np.load('Results/Cropped/y_test.npy')
matrix2, probabilities2, labels2 = evaluator2.Xception_evaluate(x_test2, y_test2)
evaluator2.ROC_curve(x_test2, y_test2, 'Cropped OD')
print(matrix2)


# 4. Evaluate the model for Cropped OD (ACRIMA)
evaluator3 = ModelEvaluator('../../model-Xception-best-2.h5')
x_test3 = np.load('Results/ACRIMA/x_test.npy')
y_test3 = np.load('Results/ACRIMA/y_test.npy')
matrix3, probabilities3, labels3 = evaluator3.Xception_evaluate(x_test3, y_test3)
evaluator3.ROC_curve(x_test3, y_test3, 'ACRIMA Dataset')
print(matrix3)


# # 5. Combine the model for the Whole Fundus and Cropped OD
evaluator_com1 = ModelEvaluator('../../model-Xception-best-1.h5')
evaluator_com2 = ModelEvaluator('../../model-Xception-best-2.h5')
x_test_whole = np.load('Results/Original/x_test.npy')
x_test_crop = np.load('Results/Cropped/x_test.npy')
y_test = np.load('Results/Original/y_test.npy')

_, probabilities_whole, labels = evaluator_com1.Xception_evaluate(x_test_whole, y_test)
_, probabilities_crop, _ = evaluator_com2.Xception_evaluate(x_test_crop, y_test)
probabilities_com = (np.array(probabilities_whole) + np.array(probabilities_crop))/2
predictions = np.argmax(probabilities_com, axis=1)
print(confusion_matrix(labels, predictions))

fpr, tpr, thresholds = roc_curve(labels, probabilities_com[:, 1])
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve for Combined model')
plt.legend(loc="lower right")
plt.show()

# Conclusion: For the accuracy and AUC: Whole Fundus < Combined Model < Cropped OD
# Thus, we will only use the model for cropped OD to classify (model-Xception-best-2.h5)

