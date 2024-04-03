"""
Created on 2023/11/14

U-Net architecture to do the segmentation
"""

from keras.layers import Input, Conv2D, MaxPooling2D, Conv2DTranspose, Concatenate, Dropout
from keras.models import Model


def unet(input_shape, drop_p: float, n_classes: int):
    """
    @brief:
        Build the U-Net architecture for up-sampling
    @args:
        input_shape: The shape of the image
        drop_p: Float between 0 and 1. Fraction of the input units to drop.
        n_classes: The number of classes (in this project, we use binary segmentation)
    @returns:
        The final U-Net model
    """

    print("--------------------------------------")
    print("Start Model Construction")
    print("--------------------------------------")

    ## Encode part
    inputs = Input(input_shape)  # (256, 256, 3)

    model_1 = Conv2D(16, 3, activation='relu', kernel_initializer='he_normal', padding='same')(inputs)
    model_1 = Conv2D(16, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_1)
    # (256, 256, 16)

    model_2 = MaxPooling2D(pool_size=(2, 2))(model_1)  # (128, 128, 16)
    model_2 = Conv2D(32, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_2)
    model_2 = Dropout(drop_p)(model_2)
    model_2 = Conv2D(32, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_2)
    # (128, 128, 32)

    model_3 = MaxPooling2D(pool_size=(2, 2))(model_2)  # (64, 64, 32)
    model_3 = Conv2D(64, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_3)
    model_3 = Dropout(drop_p)(model_3)
    model_3 = Conv2D(64, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_3)
    # (64, 64, 64)

    model_4 = MaxPooling2D(pool_size=(2, 2))(model_3)  # (32, 32, 64)
    model_4 = Conv2D(128, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_4)
    model_4 = Dropout(drop_p)(model_4)
    model_4 = Conv2D(128, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_4)
    # (32, 32, 128)

    model_5 = MaxPooling2D(pool_size=(2, 2))(model_4)  # (16, 16, 128)
    model_5 = Conv2D(256, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_5)
    model_5 = Dropout(drop_p)(model_5)
    model_5 = Conv2D(256, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_5)
    # (16, 16, 256)

    ## Decode part
    model_6 = Conv2DTranspose(128, 2, strides=2, padding='same')(model_5)  # (32, 32, 128)
    model_6 = Concatenate(axis=3)([model_4, model_6])  # (32, 32, 256)
    model_6 = Conv2D(128, 2, activation='relu', kernel_initializer='he_normal', padding='same')(model_6)
    model_6 = Dropout(drop_p)(model_6)
    model_6 = Conv2D(128, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_6)
    # (32, 32, 128)

    model_7 = Conv2DTranspose(64, 2, strides=2, padding='same')(model_6)  # (64, 64, 64)
    model_7 = Concatenate(axis=3)([model_3, model_7])  # (64, 64, 128)
    model_7 = Conv2D(64, 2, activation='relu', kernel_initializer='he_normal', padding='same')(model_7)
    model_7 = Dropout(drop_p)(model_7)
    model_7 = Conv2D(64, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_7)
    # (64, 64, 64)

    model_8 = Conv2DTranspose(32, 2, strides=2, padding='same')(model_7)  # (128, 128, 32)
    model_8 = Concatenate(axis=3)([model_2, model_8])  # (128, 128, 64)
    model_8 = Conv2D(32, 2, activation='relu', kernel_initializer='he_normal', padding='same')(model_8)
    model_8 = Dropout(drop_p)(model_8)
    model_8 = Conv2D(32, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_8)
    # (128, 128, 32)

    model_9 = Conv2DTranspose(16, 2, strides=2, padding='same')(model_8)  # (256, 256, 16)
    model_9 = Concatenate(axis=3)([model_1, model_9])  # (256, 256, 32)
    model_9 = Conv2D(16, 2, activation='relu', kernel_initializer='he_normal', padding='same')(model_9)
    model_9 = Dropout(drop_p)(model_9)
    model_9 = Conv2D(16, 3, activation='relu', kernel_initializer='he_normal', padding='same')(model_9)
    # (256, 256, 16)

    outputs = Conv2D(n_classes, 3, activation='sigmoid', padding='same')(model_9)  # (256, 256, 1)
    model = Model(inputs=inputs, outputs=outputs)

    print("Finish Model Construction")
    print("--------------------------------------")

    return model


# # Test the function
# from Loader import Loader
# from keras.optimizers import Adam
# from keras.losses import binary_crossentropy
# import tensorflow as tf
# data_loader = Loader('../../data/ORIGA/', '../../data/Semi-automatic-annotations/', '../../data/glaucoma.csv')
# images, masks = data_loader.preprocess_data(data_loader.image_paths, data_loader.mask_paths)
#
# x_train, x_val, x_test, y_train, y_val, y_test = data_loader.get_data_split(images, masks,
#                                                                             test_size=0.1, random_state=10)
#
#
# input_shape = (256, 256, 3)
# n_classes = 1
# drop_p = 0.2
#
# def IoU(y_true, y_pred):
#     """
#     @brief:
#         Calculate the Intersection over Union (IoU) for batches of data in a Keras/TensorFlow model.
#     @args:
#         y_true (Tensor): True labels.
#         y_pred (Tensor): Predicted labels.
#     @returns:
#         Tensor: The IoU.
#     """
#     # Threshold predictions to form a binary mask
#     y_pred = tf.cast(y_pred > 0.5, tf.float32)
#
#     # Calculate the intersection and union
#     intersection = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(y_true, 1), tf.equal(y_pred, 1)), tf.float32),
#                                  axis=[1, 2, 3])
#     union = tf.reduce_sum(tf.cast(tf.logical_or(tf.equal(y_true, 1), tf.equal(y_pred, 1)), tf.float32),
#                           axis=[1, 2, 3])
#
#     # Calculate IoU
#     iou = tf.reduce_mean((intersection + tf.keras.backend.epsilon()) / (union + tf.keras.backend.epsilon()), axis=0)
#
#     return iou
#
#
# def f1_score(y_true, y_pred):
#     """
#     @brief:
#         Calculate the F1 Score for batches of data in a Keras/TensorFlow model.
#     @args:
#         y_true (Tensor): True labels.
#         y_pred (Tensor): Predicted labels.
#     @returns:
#         Tensor: The F1 Score.
#     """
#     # Convert probabilities to binary predictions (After sigmoid activation)
#     y_pred = tf.cast(y_pred > 0.5, tf.float32)
#     true_positives = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(y_true, 1), tf.equal(y_pred, 1)), tf.float32),
#                                    axis=[1, 2, 3])
#     predicted_positives = tf.reduce_sum(tf.cast(tf.equal(y_pred, 1), tf.float32), axis=[1, 2, 3])
#     possible_positives = tf.reduce_sum(tf.cast(tf.equal(y_true, 1), tf.float32), axis=[1, 2, 3])
#
#     precision = true_positives / (predicted_positives + tf.keras.backend.epsilon())
#     recall = true_positives / (possible_positives + tf.keras.backend.epsilon())
#
#     f1 = 2 * (precision * recall) / (precision + recall + tf.keras.backend.epsilon())
#
#     return tf.reduce_mean(f1)
#
#
# model = unet(input_shape, drop_p, n_classes)
# model.summary()
# model.compile(
#     optimizer=Adam(learning_rate=0.005),
#     loss=binary_crossentropy,
#     metrics=['accuracy', IoU, f1_score])
# history = model.fit(x_train, y_train,
#                     batch_size=8,
#                     epochs=10,
#                     validation_data=(x_val, y_val))

