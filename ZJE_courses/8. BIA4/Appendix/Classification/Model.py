"""
Created on 2023/11/22

Partial adapted from https://blog.csdn.net/dgvv4/article/details/123460427
Xception architecture to do the classification
"""

from keras.layers import Input, Conv2D, MaxPooling2D, BatchNormalization, \
    ReLU, SeparableConv2D, Add, GlobalAveragePooling2D, Dense
from keras.models import Model
import keras


def conv_block(input_shape, filters: int, kernel_size, stride: int):
    """
    @brief:
        A classical convolution block
    @args:
        input_shape: The shape of the image
        filters: The number of filters
        kernel_size: The size of kernel
        stride: The stride of the kernel
    @returns:
        The block model
    """

    block_model = Conv2D(filters=filters,
                         kernel_size=kernel_size,
                         strides=stride,
                         padding='same',
                         use_bias=False)(input_shape)

    block_model = BatchNormalization()(block_model)
    block_model = ReLU()(block_model)
    return block_model


def sep_conv_block(input_shape, filters: int, kernel_size):
    """
    @brief:
        A depth-wise separable convolution (can reduce the parameter number)
    @args:
        input_shape: The shape of the image
        filters: The number of filters
        kernel_size: The size of kernel
    @returns:
        The separable convolution model
    """
    sep_model = ReLU()(input_shape)
    sep_model = SeparableConv2D(filters=filters,
                                kernel_size=kernel_size,
                                strides=1,
                                padding='same',
                                use_bias=False)(sep_model)

    return sep_model


def res_block(input_shape, filters: int):
    """
    @brief:
        A unit of the Xception network (Residual block)
    @args:
        input_shape: The shape of the image
        filters: The number of filters
    @returns:
        The Residual block unit
    """
    residual = Conv2D(filters,
                      kernel_size=(1, 1),
                      strides=2)(input_shape)
    residual = BatchNormalization()(residual)

    conv = sep_conv_block(input_shape, filters, kernel_size=(3, 3))
    conv = sep_conv_block(conv, filters, kernel_size=(3, 3))
    unit = MaxPooling2D(pool_size=(3, 3), strides=2, padding='same')(conv)

    # Residual added to the output
    output = Add()([residual, unit])

    return output


def middle_flow(x, filters):
    """
    @brief:
        A unit in the middle flow (should be repeated 4 times for simplification)
    @args:
        x: The output of the previous layer
        filters: The number of filters
    @returns:
        The middle flow unit
    """
    for _ in range(4):
        residual = x
        # Three separable convolution unit
        x = sep_conv_block(x, filters, kernel_size=(3, 3))
        x = sep_conv_block(x, filters, kernel_size=(3, 3))
        x = sep_conv_block(x, filters, kernel_size=(3, 3))
        # Stacking residual edges
        x = Add()([residual, x])
    return x


def xception(input_shape, r, classes):
    """
    @brief:
        The main function of Xception model
    @args:
        input_shape: The shape of the image
        r: The hyperparameter set in keras.regularizers.l2 (avoid over-fitting)
        classes: The number of the classes
    @returns:
        The final Xception model
    """

    print("--------------------------------------")
    print("Start Model Construction")
    print("--------------------------------------")

    ################################################# The Entry Flow #################################################
    inputs = Input(shape=input_shape)  # (256, 256, 3)

    x = conv_block(inputs, filters=16, kernel_size=(3, 3), stride=2)  # (128, 128, 16)
    x = conv_block(x, filters=32, kernel_size=(3, 3), stride=1)  # (128, 128, 32)

    residual = Conv2D(filters=64, kernel_size=(1, 1), strides=2,
                      padding='same', use_bias=False)(x)  # (64, 64, 64)
    residual = BatchNormalization()(residual)  # (64, 64, 64)

    x = SeparableConv2D(64, kernel_size=(3, 3), strides=1, padding='same', use_bias=False)(x)  # (128, 128, 64)
    x = BatchNormalization()(x)  # (128, 128, 64)
    x = sep_conv_block(x, filters=64, kernel_size=(3, 3))  # (128, 128, 64)
    x = MaxPooling2D(pool_size=(3, 3), strides=2, padding='same')(x)  # (64, 64, 64)
    x = Add()([x, residual])  # (64, 64, 64)

    x = res_block(x, filters=128)  # (32, 32, 128)
    x = res_block(x, filters=256)  # (16, 16, 256)

    ################################################# The Middle Flow #################################################
    x = middle_flow(x, filters=256)  # (16, 16, 256)

    ################################################# The Exit Flow #################################################
    residual = Conv2D(filters=512, kernel_size=(1, 1),
                      strides=2, use_bias=False, padding='same')(x)  # (8, 8, 512)
    residual = BatchNormalization()(residual)  # (8, 8, 512)

    x = sep_conv_block(x, filters=256, kernel_size=(3, 3))  # (16, 16, 256)
    x = sep_conv_block(x, filters=512, kernel_size=(3, 3))  # (16, 16, 512)
    x = MaxPooling2D(pool_size=(3, 3), strides=2, padding='same')(x)  # (8, 8, 512)
    x = Add()([residual, x])  # (8, 8, 512)

    x = SeparableConv2D(512, (3, 3), padding='same', use_bias=False)(x)  # (8, 8, 512)
    x = BatchNormalization()(x)
    x = ReLU()(x)  # (8, 8, 512)

    x = SeparableConv2D(1024, (3, 3), padding='same', use_bias=False)(x)  # (8, 8, 1024)
    x = BatchNormalization()(x)
    x = ReLU()(x)  # (8, 8, 1024)

    x = GlobalAveragePooling2D()(x)  # (, , 1024)

    outputs = Dense(classes, activation='softmax',
                    kernel_regularizer=keras.regularizers.l2(r))(x)  # (, , classes)
    model = Model(inputs, outputs)

    print("--------------------------------------")
    print("Finish Model Construction")
    print("--------------------------------------")
    return model


# # Test the function
# model = xception(input_shape=(256, 256, 3), r=0.01, classes=2)
# model.summary()
