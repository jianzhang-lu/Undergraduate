"""
Created on 2023/12/4

This class is used to predict whether the images represent glaucoma or not.
From the evaluation of classification performance:
Whole Fundus Model < Combined Model < Cropped OD Model
Thus, we will only use the model for cropped OD to classify (model-Xception-best-2.h5)
"""

import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras.metrics import AUC, Precision, Recall, Metric

from Predict_OD import SegmentationOD


# Define the F1 Score to evaluate the model (The same as Train.py).
# This class inherits from the Metric Class, can be used to perform custom metrics.
class F1Score(Metric):
    def __init__(self, name='f1_score', **kwargs):
        super(F1Score, self).__init__(name=name, **kwargs)
        self.precision = Precision()
        self.recall = Recall()

    def update_state(self, y_true, y_pred, sample_weight=None):
        self.precision.update_state(y_true, y_pred, sample_weight)
        self.recall.update_state(y_true, y_pred, sample_weight)

    def result(self):
        precision_val = self.precision.result()
        recall_val = self.recall.result()
        return 2 * ((precision_val * recall_val) / (precision_val + recall_val + tf.keras.backend.epsilon()))

    def reset_state(self):
        self.precision.reset_state()
        self.recall.reset_state()


class Classification:
    """
    A class to classify whether the input image represents glaucoma or not.

    :attribute model: The trained Xception model for classification (*.h5)
    """
    def __init__(self, model_path):
        self.model = load_model(model_path, custom_objects={'auc_1': AUC(), 'f1_score': F1Score()})

    def classify_single_image(self, cropped_image):
        """
        @brief:
            Classify the single image using the Xception model
        @args:
            cropped_image: The input cropped image
        @returns:
            The prediction of the class (Glaucoma or not)
        """

        # Resize the cropped image and enhance contrast (the same as the pre-process step in the Predict_OD.py
        processed_image = SegmentationOD.preprocess_image(self.model, cropped_image)
        probabilities = self.model.predict(np.expand_dims(processed_image, axis=0), verbose=0)[0]
        prediction = np.argmax(probabilities, axis=0)
        # 1: Glaucoma; 0: no Glaucoma
        return prediction

    def classify_images_in_folder(self, cropped_images) -> list:
        """
        @brief:
            Classify all images in a folder using the Xception model
        @args:
            cropped_images: The input cropped images in a folder (preprocessed in Predict_OD.py)
        @returns:
            All predicted classes in a list (Glaucoma or not)
        """

        print("--------------------------------------")
        print("Start classifying images in the folder")
        print("--------------------------------------")

        predictions = []
        for cropped_image in cropped_images:
            prediction = self.classify_single_image(cropped_image)
            predictions.append(prediction)

        print("--------------------------------------")
        print("Finish classifying images in the folder")
        print("--------------------------------------")
        return predictions

