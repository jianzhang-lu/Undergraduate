"""
Created on 2023/11/12
Modified on 2023/11/13 (Finish the model)

Note (update on 2023/11/14)
This is a model reproducing this literature:
'Robust optic disc and cup segmentation with deep learning for glaucoma detection'
Since it is time-consuming and I cannot find any pre-trained ResNet-34 model compatible to us.
We decide to use classical U-Net instead of this better one.
"""

from keras.layers import Input, Conv2D, BatchNormalization, Activation, MaxPooling2D, Add, Conv2DTranspose, Concatenate
from keras.models import Model


def resnet_block(input_tensor, num_filters, kernel_size=3, stride=1, conv_shortcut=False):
    """
    @brief:
        A residual block in Resnet-34 with two 3x3 convolutions and a skip connection.
    @args:
        input_tensor: The input tensor from the previous layer
        num_filters: The number of filters
        kernel_size: The size of kernel used in CNN (default is 3: 3*3 kernel)
        stride: The stride (default is 1)
        conv_shortcut: Whether we need to apply a convolution to the skip connection (default: False)
    @returns:
        The block architecture.
    """

    block = Conv2D(num_filters, kernel_size, padding='same', strides=stride)(input_tensor)
    block = BatchNormalization()(block)
    block = Activation('relu')(block)

    block = Conv2D(num_filters, kernel_size, padding='same')(block)
    block = BatchNormalization()(block)

    # Add a conv to the skip connection: in the first block where the number of filters increases.
    # To match the output of the residual block.
    # If the stride is not equal to 1, main path of the residual block will down-sample the input.
    # To ensure the dimensions match, the shortcut must also down-sample the input.
    if conv_shortcut or stride != 1:
        shortcut = Conv2D(num_filters, kernel_size=1, strides=stride, padding='same')(input_tensor)
        shortcut = BatchNormalization()(shortcut)
    else:
        shortcut = input_tensor

    block = Add()([block, shortcut])
    block = Activation('relu')(block)
    return block


def resnet34(input_shape):
    """
    @brief:
        Build the ResNet-34 architecture for down-sampling
    @args:
        input_shape: The shape of the input image (512, 512, 3)
    @returns:
        Each step of the resnet34 model (added to the decoding part).
    """
    inputs = Input(input_shape)  # (512, 512, 3)

    # Initial Convolution
    resnet = Conv2D(filters=64, kernel_size=7, strides=2, padding="same")(inputs)  # (256, 256, 64)
    resnet = BatchNormalization()(resnet)  # (256, 256, 64)
    resnet_1 = Activation('relu')(resnet)  # (256, 256, 64)
    resnet_2 = MaxPooling2D(pool_size=(2, 2), strides=2, padding="same")(resnet_1)  # (128, 128, 64)

    # Residual blocks (4 stages)
    # STAGE 1: 3 layers (3*3 conv, 64)
    resnet_2 = resnet_block(resnet_2, 64, conv_shortcut=True)
    for _ in range(2):
        resnet_2 = resnet_block(resnet_2, 64)  # (128, 128, 64)

    # STAGE 2: 4 layers (3*3 conv, 128) The first block has the stride of 2
    resnet_3 = resnet_block(resnet_2, 128, stride=2, conv_shortcut=True)
    for _ in range(3):
        resnet_3 = resnet_block(resnet_3, 128)  # (64, 64, 128)

    # STAGE 3: 6 layers (3*3 conv, 256) The first block has the stride of 2
    resnet_4 = resnet_block(resnet_3, 256, stride=2, conv_shortcut=True)
    for _ in range(5):
        resnet_4 = resnet_block(resnet_4, 256)  # (32, 32, 256)

    # STAGE 4: 3 layers (3*3 conv, 512) The first block has the stride of 2
    resnet_5 = resnet_block(resnet_4, 512, stride=2, conv_shortcut=True)
    for _ in range(2):
        resnet_5 = resnet_block(resnet_5, 512)  # (16, 16, 512)

    return inputs, resnet_1, resnet_2, resnet_3, resnet_4, resnet_5


def unet(input_shape, n_classes):
    """
    @brief:
        Build the U-Net architecture for up-sampling
    @args:
        input_shape: The shape of the Resnet-34 output result
        n_classes: The number of classes (in this project, we use binary segmentation)
    @returns:
        The final segmentation model
    """
    # resnet_1: (256, 256, 64); resnet_2: (128, 128, 64);
    # resnet_3: (64, 64, 128); resnet_4: (32, 32, 256); encoder_output: (16, 16, 512)
    inputs, resnet_1, resnet_2, resnet_3, resnet_4, encoder_output = resnet34(input_shape)

    # Decoder part (Modified U-Net)
    ## decoder_filters == 128
    encoder_output = Conv2DTranspose(128, 2, strides=2, padding="same")(encoder_output)  # (32, 32, 128)
    encoder_output = BatchNormalization()(encoder_output)
    encoder_output = Activation('relu')(encoder_output)
    resnet_4 = Conv2D(128, 1, strides=1, padding="same")(resnet_4)  # (32, 32, 128)
    resnet_4 = BatchNormalization()(resnet_4)
    resnet_4 = Activation('relu')(resnet_4)
    encoder_output = Concatenate(axis=2)([resnet_4, encoder_output])  # (32, 32, 256)

    ## decoder_filters == 128
    encoder_output = Conv2DTranspose(128, 2, strides=2, padding="same")(encoder_output)  # (64, 64, 128)
    encoder_output = BatchNormalization()(encoder_output)
    encoder_output = Activation('relu')(encoder_output)
    resnet_3 = Conv2D(128, 1, strides=1, padding="same")(resnet_3)  # (64, 64, 128)
    resnet_3 = BatchNormalization()(resnet_3)
    resnet_3 = Activation('relu')(resnet_3)
    encoder_output = Concatenate(axis=2)([resnet_3, encoder_output])  # (64, 64, 256)

    ## decoder_filters == 128
    encoder_output = Conv2DTranspose(128, 2, strides=2, padding="same")(encoder_output)  # (128, 128, 128)
    encoder_output = BatchNormalization()(encoder_output)
    encoder_output = Activation('relu')(encoder_output)
    resnet_2 = Conv2D(128, 1, strides=1, padding="same")(resnet_2)  # (128, 128, 128)
    resnet_2 = BatchNormalization()(resnet_2)
    resnet_2 = Activation('relu')(resnet_2)
    encoder_output = Concatenate(axis=2)([resnet_2, encoder_output])  # (128, 128, 256)

    ## decoder_filters == 128
    encoder_output = Conv2DTranspose(128, 2, strides=2, padding="same")(encoder_output)  # (256, 256, 128)
    encoder_output = BatchNormalization()(encoder_output)
    encoder_output = Activation('relu')(encoder_output)
    resnet_1 = Conv2D(128, 1, strides=1, padding="same")(resnet_1)  # (256, 256, 128)
    resnet_1 = BatchNormalization()(resnet_1)
    resnet_1 = Activation('relu')(resnet_1)
    encoder_output = Concatenate(axis=2)([resnet_1, encoder_output])  # (256, 256, 256)

    # Transfer to the original shape of images
    outputs = Conv2DTranspose(n_classes, 2, strides=2, activation="sigmoid", padding="same")(encoder_output)  # (512, 512, 1)

    model = Model(inputs=inputs, outputs=outputs)

    return model


# Test the function
input_shape = (512, 512, 3)
n_classes = 1

model = unet(input_shape, n_classes)
print(len(model.layers))
model.summary()
