"""
Created on 2023/11/9
Modified on 2023/11/16
"""

import os
import numpy as np
import pandas as pd
from skimage import io
from skimage.transform import resize
from skimage.exposure import equalize_adapthist
from scipy.io import matlab
from sklearn.model_selection import train_test_split


class Loader:
    """
    A class of Data Loader to load images and masks, preprocess the data, and split the dataset.

    :attribute image_dir (str): The folder of original images (e.g. 001.jpg)
    :attribute mask_dir (str): The folder of mask images, that is, the ground truth of OC and OD positions (e.g. 001.mat)
    :attribute csv_path (str): The path of the summary .csv file.
    :attribute data_info (DataFrame): A pandas DataFrame containing the information from the csv file.
    :attribute image_paths: All paths of images
    :attribute mask_paths: All paths of masks
    """

    def __init__(self, image_dir, mask_dir, csv_path):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.csv_path = csv_path
        self.data_info = pd.read_csv(csv_path)
        image_filenames = os.listdir(self.image_dir)
        mask_filenames = os.listdir(self.mask_dir)
        self.image_paths = [os.path.join(self.image_dir, f) for f in image_filenames]
        self.mask_paths = [os.path.join(self.mask_dir, f) for f in mask_filenames]

    def preprocess_data(self, image_paths, mask_paths):
        """
        @brief:
            Preprocess the data by resizing the images and masks to (256, 256, 3),
            normalizing the images, enhancing the contrast, and converting masks to binary format
            1: OD region (including OC); 0: background (other parts).

        @args:
            image_paths: The array of images to preprocess.
            mask_paths: The array of masks to preprocess.

        @returns:
            tuple: A tuple containing the preprocessed images and masks.
        """

        print("--------------------------------------")
        print("Start Data Pre-processing")
        print("--------------------------------------")

        preprocessed_images = []
        preprocessed_masks = []

        # for i in range(32):
        for i in range(len(image_paths)):
            image = io.imread(image_paths[i])
            mask = matlab.loadmat(mask_paths[i])['mask']

            # Resize images to (256, 256)
            resized_image = resize(image, (256, 256, 3), mode='reflect', preserve_range=True)

            # Normalize images to [0, 1]
            normalized_image = resized_image.astype('float32')/255.0

            # Enhance contrast using CLAHE. Applied to each channel individually
            contrast_enhanced_image = np.zeros_like(normalized_image)
            for channel in range(normalized_image.shape[2]):
                contrast_enhanced_image[:, :, channel] = equalize_adapthist(normalized_image[:, :, channel])

            # Resize masks to (256, 256) and convert to binary format
            resized_mask = resize(mask, (256, 256), order=0, mode='reflect', preserve_range=True)
            binary_mask = (resized_mask > 0).astype('float32')

            # Reshape to (num_samples, width, height, channels)
            binary_mask = binary_mask.reshape(binary_mask.shape[0],
                                              binary_mask.shape[1], 1)

            preprocessed_images.append(contrast_enhanced_image)
            preprocessed_masks.append(binary_mask)

        print("Finish Data Pre-processing")
        print("--------------------------------------")

        return np.array(preprocessed_images), np.array(preprocessed_masks)

    def get_data_split(self, images, masks, test_size=0.1, random_state=10):
        """
        @brief:
            Split the data into training, validation, and test datasets (8:1:1).
            Also restore the results for further use
        @args:
            images: All preprocessed images.
            masks: All preprocessed masks.
            test_size (float): The proportion of the dataset to include in the test split.
            random_state (int): To reproduce the results
        @returns:
            tuple: A tuple containing all information
            (train images, validation images, test images, train masks, validation masks, and test masks).
        """

        print("Start Data Splitting")
        print("--------------------------------------")

        # len(x) = 585; len(y) = 65
        x_train, x_test, y_train, y_test = train_test_split(images, masks,
                                                            test_size=test_size,
                                                            random_state=random_state)
        # 65/585 = 1/9
        x_train, x_val, y_train, y_val = train_test_split(x_train, y_train,
                                                          test_size=test_size/(1 - test_size),
                                                          random_state=random_state)

        np.save('Results/x_train', x_train)
        np.save('Results/x_val', x_val)
        np.save('Results/x_test', x_test)
        np.save('Results/y_train', y_train)
        np.save('Results/y_val', y_val)
        np.save('Results/y_test', y_test)

        print("Finish Data Splitting")
        print("--------------------------------------")

        return np.array(x_train), np.array(x_val), np.array(x_test), \
            np.array(y_train), np.array(y_val), np.array(y_test)


# NOTE that you need to run the following codes and restore the data loading files (.npy)
# if you want to retrain the model

# Generate files restoring train, val, and test datasets
data_loader = Loader(image_dir='../../data/ORIGA/',
                     mask_dir='../../data/Semi-automatic-annotations/',
                     csv_path='../../data/glaucoma.csv')
images, masks = data_loader.preprocess_data(data_loader.image_paths,
                                            data_loader.mask_paths)
data_loader.get_data_split(images, masks, test_size=0.1, random_state=10)

