"""
Created on 2023/11/24

Perform the data augmentation, train two Xception models separately;
Improve CNN performance to avoid over-fitting (early stop);
Tune hyperparameters.
"""

from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
import keras_tuner as kt
import tensorflow as tf
from keras.metrics import AUC, Precision, Recall, Metric
import pickle
import numpy as np
import os

from Model import xception


# Define the F1 Score to evaluate the model.
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


class XceptionHyperModel(kt.HyperModel):
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

        # The hyperparameter regularization & learning rate could be optimized
        learning_rate = hp.Choice('learning_rate', values=[0.01, 0.005, 0.001])
        regularization = hp.Choice('regularization', values=[0.01, 0.005, 0.015])

        # Build the Xception model
        model = xception(self.input_shape, regularization, 2)
        model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss=binary_crossentropy,
            metrics=['accuracy', AUC(), F1Score()])
        return model


class Train:
    """
    A class to train the Xception model.

    :attribute x_train, x_val, x_test: The train, validation, and test dataset for images
    :attribute y_train, y_val, y_test: The train, validation, and test dataset for the true labels
    :attribute hypermodel: The instantiation the hypermodel to tune the hyperparameters
    :attribute batch_size: The hyperparameter batch size (need to be optimized)
    :attribute tuner: The final Keras model
    """

    def __init__(self, npy_dir, project_name):
        # Load the data from .npy files
        self.x_train = np.load(os.path.join(npy_dir, "x_train.npy"))
        self.x_val = np.load(os.path.join(npy_dir, "x_val.npy"))
        self.x_test = np.load(os.path.join(npy_dir, "x_test.npy"))
        self.y_train = np.load(os.path.join(npy_dir, "y_train.npy"))
        self.y_val = np.load(os.path.join(npy_dir, "y_val.npy"))
        self.y_test = np.load(os.path.join(npy_dir, "y_test.npy"))

        self.hypermodel = XceptionHyperModel(input_shape=self.x_train.shape[1:])

        # Find all possible combinations (9 sets)
        self.tuner = kt.GridSearch(self.hypermodel,
                                   objective=['val_loss'],
                                   executions_per_trial=1,
                                   directory=project_name,
                                   project_name=project_name)

    def data_aug(self, seed: int):
        """
        @brief:
            Perform the data augmentation process
        @args:
            Seed: The seed helping to reproduce the result
        @returns:
            The augmented generator of images
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
        image_generator = image_datagen.flow(self.x_train, self.y_train, seed=seed, batch_size=8)

        print("Finish Data Augmentation")
        print("--------------------------------------")

        return image_generator

    def tuner_search(self, seed: int):
        """
        @brief:
            Start to search the best hyperparameters
        @args:
            Seed: The seed helping to reproduce the result
        @returns:
            The model with the best hyperparameters
            The best hyperparameters
        """
        image_generator = self.data_aug(seed)

        print("--------------------------------------")
        print("Start Hyperparameter Tune")
        print("--------------------------------------")

        self.tuner.search(image_generator,
                          batch_size=8,
                          steps_per_epoch=len(self.x_train) // 8,
                          validation_data=(self.x_val, self.y_val),
                          epochs=20,
                          callbacks=[EarlyStopping(patience=10), ReduceLROnPlateau(patience=5)])

        print("Finish Hyperparameter Tune")
        print("--------------------------------------")

        # Retrieve the best hyperparameters
        best_hp = self.tuner.get_best_hyperparameters(num_trials=1)[0]
        print(f"The best regularization is: {best_hp.get('regularization')}")
        print(f"The best learning rate is: {best_hp.get('learning_rate')}")

        # Rebuild the model with the best hyperparameters
        model = self.hypermodel.build(best_hp)
        return model, best_hp

    def train_model(self, name, seed: int):
        """
        @brief:
            Train the Xception model
        @args:
            name: The name of .h5 file to restore the model
            seed: The seed helping to reproduce the result
        @returns:
            The history for each epoch
        """

        print("--------------------------------------")
        print("Start Model training")
        print("--------------------------------------")

        # Define callbacks
        callbacks = [EarlyStopping(patience=10, verbose=1), ReduceLROnPlateau(patience=5),
                     ModelCheckpoint(name, verbose=1, save_best_only=True)]

        # Train the model with the best hyperparameters
        best_model, best_hp = self.tuner_search(seed)
        image_generator = self.data_aug(seed)
        history = best_model.fit(image_generator,
                                 steps_per_epoch=len(self.x_train) // 8,
                                 validation_data=(self.x_val, self.y_val),
                                 epochs=100,
                                 callbacks=callbacks)

        print("Finish Model training")
        print("--------------------------------------")

        return history


# # NOTE that the results of model training are restored in the Cropped/trainHistoryDict_2.txt
# # and Original/trainHistoryDict_1 files.
# # This training step takes much longer time, we do not suggest running it again.
# # If you want to run the following code, please select a different position to restore the training result.

# # Train the model_1 (From the original image)
# train = Train('Results/Original/', 'Xception_tuner_1')
# history = train.train_model('model-Xception-best-1.h5', 12)
# with open('Results/Original/trainHistoryDict_1.txt', 'wb') as file_pi:
#     pickle.dump(history.history, file_pi)
#
# print('Finish training the model 1')


# # Train the model_2 (From the cropped image)
# train = Train('Results/Cropped/', 'Xception_tuner_2')
# history = train.train_model('model-Xception-best-2.h5', 13)
# with open('Results/Cropped/trainHistoryDict_2.txt', 'wb') as file_pi:
#     pickle.dump(history.history, file_pi)
#
# print('Finish training the model 2')
