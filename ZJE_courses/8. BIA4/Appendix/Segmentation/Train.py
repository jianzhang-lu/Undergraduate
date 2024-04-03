"""
Created on 2023/11/14
Modified on 2023/11/16

Perform the data augmentation, train the model;
Improve CNN performance to avoid over-fitting (early stop);
Tune hyperparameters.
"""

from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
import keras_tuner as kt
import tensorflow as tf
import pickle
import numpy as np
import os

from Model import unet


## Use IoU and F1 Score to test the effectiveness of segmentation
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


class UNetHyperModel(kt.HyperModel):
    """
    A HyperModel class for KerasTuner

    :attribute name: Optional string, the name of this HyperModel (superclass).
    :attribute tunable: Boolean, whether the hyperparameters defined in this
                        hypermodel should be added to search space (superclass).
    :attribute input_shape: The input_shape of images (256, 256, 3).
    """

    def __init__(self, input_shape):
        super().__init__()
        self.input_shape = input_shape

    def build(self, hp):
        """
        @brief:
            Build the Keras model, which defines and compiles the model with hyperparameters that need to tune.
        @args:
            hp: A 'HyperParameters' instance
        @returns:
            The final Keras model
        """

        # The hyperparameter drop_p can be optimized
        ## drop_p = 0.05, 0.1, 0.15, 0.2
        drop_p = hp.Float('drop_p', min_value=0.05, max_value=0.2, step=0.05)
        learning_rate = hp.Choice('learning_rate', values=[0.05, 0.01, 0.005, 0.001])

        # Build the U-Net model
        model = unet(self.input_shape, drop_p, 1)
        model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss=binary_crossentropy,
            metrics=['accuracy', IoU_cal, f1_score])
        return model


class Train:
    """
    A class to train the U-Net model.

    :attribute x_train, x_val, x_test: The train, validation, and test dataset for images
    :attribute y_train, y_val, y_test: The train, validation, and test dataset for masks
    :attribute hypermodel: The instantiation the hypermodel to tune the hyperparameters
    :attribute tuner: The final Keras model
    """
    def __init__(self, npy_dir):

        # Load the data from .npy files
        self.x_train = np.load(os.path.join(npy_dir, "x_train.npy"))
        self.x_val = np.load(os.path.join(npy_dir, "x_val.npy"))
        self.x_test = np.load(os.path.join(npy_dir, "x_test.npy"))
        self.y_train = np.load(os.path.join(npy_dir, "y_train.npy"))
        self.y_val = np.load(os.path.join(npy_dir, "y_val.npy"))
        self.y_test = np.load(os.path.join(npy_dir, "y_test.npy"))

        self.hypermodel = UNetHyperModel(input_shape=self.x_train.shape[1:])

        self.tuner = kt.RandomSearch(self.hypermodel,
                                     objective=['val_loss'],
                                     executions_per_trial=1,
                                     directory='unet_tuner',
                                     project_name='unet_tune')

    def data_aug(self):
        """
        @brief:
            Perform the data augmentation process
        @returns:
            The augmented generator of images and masks
        """

        print("--------------------------------------")
        print("Start Data Augmentation")
        print("--------------------------------------")

        # Data augmentation generators
        data_gen_args = dict(rotation_range=10,
                             width_shift_range=0.1,
                             height_shift_range=0.1,
                             shear_range=0.1,
                             zoom_range=0.1,
                             horizontal_flip=True,
                             fill_mode='nearest')
        image_datagen = ImageDataGenerator(**data_gen_args)
        mask_datagen = ImageDataGenerator(**data_gen_args)

        # Provide the same seed and keyword arguments to the fit and flow methods
        seed = 10
        image_datagen.fit(self.x_train, augment=True, seed=seed)
        mask_datagen.fit(self.y_train, augment=True, seed=seed)
        image_generator = image_datagen.flow(self.x_train, batch_size=8, seed=seed)
        mask_generator = mask_datagen.flow(self.y_train, batch_size=8, seed=seed)

        print("Finish Data Augmentation")
        print("--------------------------------------")

        return image_generator, mask_generator

    def tuner_search(self):
        """
        @brief:
            Start to search the best hyperparameters
        @returns:
            The model with the best hyperparameters
            The best hyperparameters
        """
        image_generator, mask_generator = self.data_aug()
        train_generator = zip(image_generator, mask_generator)

        print("--------------------------------------")
        print("Start Hyperparameter Tune")
        print("--------------------------------------")

        self.tuner.search(train_generator,
                          batch_size=8,
                          steps_per_epoch=len(self.x_train) // 8,
                          validation_data=(self.x_val, self.y_val),
                          epochs=20,
                          callbacks=[EarlyStopping(patience=10), ReduceLROnPlateau(patience=5)])

        print("Finish Hyperparameter Tune")
        print("--------------------------------------")

        # Retrieve the best hyperparameters
        best_hp = self.tuner.get_best_hyperparameters(num_trials=1)[0]
        # print(f"The best optimizer is: {best_hp.get('optimizer')}")

        # Rebuild the model with the best hyperparameters
        model = self.hypermodel.build(best_hp)
        return model, best_hp

    def train_model(self):
        """
        @brief:
            Train the model
        @returns:
            The history for each epoch
        """

        print("--------------------------------------")
        print("Start Model training")
        print("--------------------------------------")

        # Define callbacks
        callbacks = [EarlyStopping(patience=10, verbose=1), ReduceLROnPlateau(patience=5),
                     ModelCheckpoint('model-unet-best.h5', verbose=1, save_best_only=True)]

        # Train the model with the best hyperparameters
        best_model, best_hp = self.tuner_search()
        image_generator, mask_generator = self.data_aug()
        train_generator = zip(image_generator, mask_generator)
        history = best_model.fit(train_generator,
                                 steps_per_epoch=len(self.x_train) // 8,
                                 validation_data=(self.x_val, self.y_val),
                                 epochs=100,
                                 callbacks=callbacks)

        print("Finish Model training")
        print("--------------------------------------")

        return history


# # NOTE that the results of model training are restored in the trainHistoryDict.txt file.
# # This training step takes much longer time, we do not suggest running it again.
# # If you want to run the following code, please select a different position to restore the training result.
# # Train the model
# train = Train('Results/')
# history = train.train_model()
# with open('Results/trainHistoryDict.txt', 'wb') as file_pi:
#     pickle.dump(history.history, file_pi)

