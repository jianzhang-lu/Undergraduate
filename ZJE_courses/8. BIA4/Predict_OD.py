"""
Created on 2023/11/20

This class is used to generate mask predictions for the input images,
and then use these masks to crop the images, focusing on the optical disk part.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from skimage.io import imread
from skimage.transform import resize
from skimage.exposure import equalize_adapthist
from skimage.measure import regionprops, label
import tensorflow as tf


def IoU_cal(y_true, y_pred):
    """
    @brief:
        Calculate the Intersection over Union (IoU) for batches of data in a Keras/TensorFlow model.
    @args:
        y_true (Tensor): True labels.
        y_pred (Tensor): Predicted labels.
    @returns:
        Tensor: The IoU.
    """
    # Threshold predictions to form a binary mask
    y_pred = tf.cast(y_pred > 0.5, tf.float32)

    # Calculate the intersection and union
    intersection = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(y_true, 1), tf.equal(y_pred, 1)), tf.float32),
                                 axis=[1, 2, 3])
    union = tf.reduce_sum(tf.cast(tf.logical_or(tf.equal(y_true, 1), tf.equal(y_pred, 1)), tf.float32),
                          axis=[1, 2, 3])

    # Calculate IoU
    iou = tf.reduce_mean((intersection + tf.keras.backend.epsilon()) / (union + tf.keras.backend.epsilon()), axis=0)

    return iou


def f1_score(y_true, y_pred):
    """
    @brief:
        Calculate the F1 Score for batches of data in a Keras/TensorFlow model.
    @args:
        y_true (Tensor): True labels.
        y_pred (Tensor): Predicted labels.
    @returns:
        Tensor: The F1 Score.
    """
    # Convert probabilities to binary predictions (After sigmoid activation)
    y_pred = tf.cast(y_pred > 0.5, tf.float32)
    true_positives = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(y_true, 1), tf.equal(y_pred, 1)), tf.float32),
                                   axis=[1, 2, 3])
    predicted_positives = tf.reduce_sum(tf.cast(tf.equal(y_pred, 1), tf.float32), axis=[1, 2, 3])
    possible_positives = tf.reduce_sum(tf.cast(tf.equal(y_true, 1), tf.float32), axis=[1, 2, 3])

    precision = true_positives / (predicted_positives + tf.keras.backend.epsilon())
    recall = true_positives / (possible_positives + tf.keras.backend.epsilon())

    f1 = 2 * (precision * recall) / (precision + recall + tf.keras.backend.epsilon())

    return tf.reduce_mean(f1)


class SegmentationOD:
    """
    A class for Prediction based on the input images

    :attribute model: The trained U-Net model for segmentation (*.h5)
    """
    def __init__(self, model_path):
        self.model = load_model(model_path, custom_objects={'IoU_cal': IoU_cal, 'f1_score': f1_score})

    def preprocess_image(self, original_image):
        """
        @brief:
            Pre-process images for the model input
        @args:
            original_image: The input original image (should be png, jpg or jpeg, and have 3 channels)
        @returns:
            The pre-processed image (shape=256, 256, 3)
        """
        resized_image = resize(original_image, (256, 256, 3), mode='reflect', preserve_range=True)
        normalized_image = resized_image.astype('float32') / 255.0
        contrast_enhanced_image = np.zeros_like(normalized_image)
        for channel in range(normalized_image.shape[2]):
            contrast_enhanced_image[:, :, channel] = equalize_adapthist(normalized_image[:, :, channel])

        return contrast_enhanced_image  # (256, 256, 3)

    def process_single_image(self, image_path, output_path=None, save=True):
        """
        @brief:
            Processes a single image: predicts the mask and saves the cropped image focusing on the optical disk.
        @args:
            image_path: The position of the input original image (should be png, jpg or jpeg, and have 3 channels)
            output_path: The position of the output cropped image (only needed if save=True)
            save: Whether to save the cropped images (default is true)
        @returns:
            The cropped image
        """
        original_image = imread(image_path)
        ori_shape = original_image.shape[:-1]
        contrast_enhanced_image = self.preprocess_image(original_image)

        # Predict the mask
        mask_pred = self.model.predict(np.expand_dims(contrast_enhanced_image, axis=0), verbose=0)[0][:, :, 0]
        ## print(mask_pred.shape)  (256, 256)

        # Convert the mask to the original size
        ori_mask_pred = resize(mask_pred, ori_shape)
        ## print(ori_mask_pred.shape)  (2048, 3072)

        # Crop the image based on the mask
        cropped_image = self.crop_image(original_image, ori_mask_pred)

        # Save the cropped image
        if save:
            plt.imsave(output_path, cropped_image)
            print(f"Cropped image saved to {output_path}")
        return cropped_image

    def process_images_in_folder(self, folder_path, output_folder=None, save=True):
        """
        @brief:
            Processes several images in a folder:
            predicts the masks and saves the cropped images focusing on the optical disk.
            All images will be save as '***_cropped.***'
            (e.g. the input is 'abc.png', the output is automatically saved as 'abc_cropped.png')

        @args:
            folder_path: The position of the folder (all files inside should be png, jpg or jpeg, and have 3 channels)
            output_folder: The position of the output cropped images.
            save: Whether to save the cropped images (default is true)

        @returns:
            All cropped images and All original filenames

        @NOTE:
            crop_images has an inhomogeneous shape after 1 dimensions, thus cannot be restored in array.
            Instead, it is restored as a list for further process
        """

        print("--------------------------------------")
        print("Start cropping images in the folder")
        print("--------------------------------------")

        cropped_images = []
        filenames = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filenames.append(filename)
                name, f_type = filename.rsplit('.', 1)
                new_name = f"{name}_cropped.{f_type}"
                image_path = os.path.join(folder_path, filename)
                output_path = os.path.join(output_folder, new_name)
                cropped_image = self.process_single_image(image_path, output_path, save)
                cropped_images.append(cropped_image)

        print("--------------------------------------")
        print("Finish cropping images in the folder")
        print("--------------------------------------")
        return cropped_images, filenames

    def crop_image(self, image, mask):
        """
        @brief:
            Crops the image based on the predicted mask.
        @args:
            image (numpy array): The original image.
            mask (numpy array): The predicted mask.
        @returns:
            numpy array: Cropped image.
        """
        # Threshold and label the mask
        thresh_mask = (mask > 0.5).astype(np.uint8)
        labeled_mask = label(thresh_mask)

        # Calculate region properties
        regions = regionprops(labeled_mask)

        # If no region is found, return the original image
        if not regions:
            return image

        # Find the largest region (assuming it is the optical disk)
        largest_region = max(regions, key=lambda r: r.area)
        ## print(largest_region.centroid)

        # Get the center and diameter of the largest region
        y0, x0 = largest_region.centroid

        # Randomly choose a scale factor to extend the region (from 1.5 to 2)
        scale_factor = np.random.uniform(1.5, 2, 1)[0]
        ## print(largest_region.major_axis_length)
        diameter = largest_region.major_axis_length * scale_factor

        # Calculate cropping coordinates
        x1 = int(max(x0 - diameter/2, 0))
        y1 = int(max(y0 - diameter/2, 0))
        x2 = int(min(x0 + diameter/2, image.shape[1]))
        y2 = int(min(y0 + diameter/2, image.shape[0]))

        # Crop the image
        cropped_image = image[y1:y2, x1:x2]
        ## print(cropped_image.shape)

        return cropped_image


# # Generate all cropped images for training the second classification model
# predict = SegmentationOD('model-unet-best.h5')
# predict.process_images_in_folder('data/ORIGA', 'data/ORIGA_cropped', True)

