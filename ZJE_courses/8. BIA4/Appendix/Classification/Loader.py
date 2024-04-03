"""
Created on 2023/11/22

A class to Load the data (both original and cropped) for classification
"""

import os
import numpy as np
import pandas as pd
from skimage import io
from skimage.transform import resize
from skimage.exposure import equalize_adapthist
from sklearn.model_selection import train_test_split
import keras


class Loader:
    """
    A class of Data Loader to load images, preprocess the data, and split the dataset.

    :attribute image_dir (str): The folder of original images (e.g. 001.jpg)
    :attribute csv_path (str): The path of the summary .csv file.
    :attribute data_info (DataFrame): A pandas DataFrame containing the information from the csv file.
    :attribute image_paths: All paths of images
    """

    def __init__(self, image_dir, csv_path):
        self.image_dir = image_dir
        self.csv_path = csv_path
        self.data_info = pd.read_csv(csv_path)
        image_filenames = os.listdir(self.image_dir)
        self.image_paths = [os.path.join(self.image_dir, f) for f in image_filenames]

    def preprocess_data(self, image_paths):
        """
        @brief:
            Preprocess the data by resizing the images and masks to (256, 256, 3),
            normalizing the images, enhancing the contrast.
        @args:
            image_paths: The array of images to preprocess.
        @returns:
            An array containing the preprocessed images.
        """

        print("--------------------------------------")
        print("Start Data Pre-processing")
        print("--------------------------------------")

        preprocessed_images = []

        for i in range(len(image_paths)):
            image = io.imread(image_paths[i])

            # Resize images to (256, 256)
            resized_image = resize(image, (256, 256, 3), mode='reflect', preserve_range=True)

            # Normalize images to [0, 1]
            normalized_image = resized_image.astype('float32')/255.0

            # Enhance contrast using CLAHE. Applied to each channel individually
            contrast_enhanced_image = np.zeros_like(normalized_image)
            for channel in range(normalized_image.shape[2]):
                contrast_enhanced_image[:, :, channel] = equalize_adapthist(normalized_image[:, :, channel])

            preprocessed_images.append(contrast_enhanced_image)

        print("Finish Data Pre-processing")
        print("--------------------------------------")

        return np.array(preprocessed_images)

    def split_data(self, output_dir, colname, test_size=0.1, random_state_1=1, random_state_2=2):
        """
        @brief:
            Splits the data into training, validation, and test sets with the same proportion for both classes.
            Since this dataset has an imbalanced number of glaucoma and non-glaucoma,
            split the two classes with the same proportion is a good idea.

        @args:
            output_dir: The folder of .npy files (restoring the splitting information).
            colname: colname == 'Filename' when dealing with original images
                     colname == 'Cropname' when dealing with cropped images
            test_size (float): Proportion of the dataset to include in the test split.
            random_state_1 (int): Random state for reproducibility (non-glaucoma).
            random_state_2 (int): Random state for reproducibility (glaucoma).

        @returns:
            tuple: A tuple containing all information
            (Also save these to reduce running time for further process)
        """

        print("Start Data Splitting")
        print("--------------------------------------")

        # Split the non-glaucoma images
        # 0: no glaucoma
        # 1: glaucoma
        df_non_glaucoma = np.array(self.data_info[self.data_info['Glaucoma'] == 0][colname])  # len=482
        train_non_glaucoma, test_non_glaucoma = train_test_split(df_non_glaucoma,
                                                                 test_size=test_size,
                                                                 random_state=random_state_1)
        train_non_glaucoma, val_non_glaucoma = train_test_split(train_non_glaucoma,
                                                                test_size=test_size / (1 - test_size),
                                                                random_state=random_state_1)

        # Split the glaucoma images
        df_glaucoma = np.array(self.data_info[self.data_info['Glaucoma'] == 1][colname])  # len=167
        train_glaucoma, test_glaucoma = train_test_split(df_glaucoma,
                                                         test_size=test_size,
                                                         random_state=random_state_2)
        train_glaucoma, val_glaucoma = train_test_split(train_glaucoma,
                                                        test_size=test_size / (1 - test_size),
                                                        random_state=random_state_2)

        # Combining both classes for each set (e.g. 001.jpg/001_cropped.jpg...)
        train_file = np.append(train_glaucoma, train_non_glaucoma)
        val_file = np.append(val_glaucoma, val_non_glaucoma)
        test_file = np.append(test_glaucoma, test_non_glaucoma)

        # Generating the label of each dataset (y)
        y_train, y_val, y_test = [], [], []
        for i in train_file:
            y = np.array(self.data_info[self.data_info[colname] == i]['Glaucoma'])[0]
            y_train.append(y)
        for i in val_file:
            y = np.array(self.data_info[self.data_info[colname] == i]['Glaucoma'])[0]
            y_val.append(y)
        for i in test_file:
            y = np.array(self.data_info[self.data_info[colname] == i]['Glaucoma'])[0]
            y_test.append(y)
        y_train_final = keras.utils.to_categorical(y_train, 2)
        y_val_final = keras.utils.to_categorical(y_val, 2)
        y_test_final = keras.utils.to_categorical(y_test, 2)

        # Generating the whole path for each image
        train_path = [os.path.join(self.image_dir, f) for f in train_file]
        val_path = [os.path.join(self.image_dir, f) for f in val_file]
        test_path = [os.path.join(self.image_dir, f) for f in test_file]

        # Generating the image for each dataset (x)
        x_train = self.preprocess_data(train_path)
        x_val = self.preprocess_data(val_path)
        x_test = self.preprocess_data(test_path)

        # Restore all information for further reuse (this can save much time)
        index = ['x_train', 'x_val', 'x_test', 'y_train', 'y_val', 'y_test']
        info = [x_train, x_val, x_test, y_train_final, y_val_final, y_test_final]
        for i, p in enumerate(index):
            restore_path = os.path.join(output_dir, p)
            np.save(restore_path, info[i])

        print("Finish Data Splitting")
        print("--------------------------------------")

        return np.array(x_train), np.array(x_val), np.array(x_test), \
            np.array(y_train_final), np.array(y_val_final), np.array(y_test_final)


# NOTE that you need to run the following codes and restore the data loading files (.npy)
# if you want to retrain the model

# 1. Generate files restoring train, val, and test datasets (Original images)
data_loader1 = Loader(image_dir='../../data/ORIGA',
                      csv_path='../../data/glaucoma.csv')

data_loader1.split_data(output_dir='Results/Original',
                        colname='Filename')

# 2. Generate files restoring train, val, and test datasets (Cropped images)
data_loader2 = Loader(image_dir='../../data/ORIGA_cropped',
                      csv_path='../../data/glaucoma.csv')

data_loader2.split_data(output_dir='Results/Cropped',
                        colname='Cropname')

