"""
Created on 2023/12/09
This function is used to segment blood vessels of input images and calculate the length of vessels.
Partially adapted from https://github.com/getsanjeev/retina-features
"""

import matplotlib.pyplot as plt
from skimage import morphology
from skimage.morphology import black_tophat, disk
import cv2
import numpy as np
import os


def vessel_segmentation(image_path, output_path=None, length=False):
    """
    @brief:
        Segment the blood vessels out of a single image and measure the length
    @args:
        image_path: The path of input images (should be png, jpg or jpeg, and have 3 channels)
        output_path: The position of the output image to show the segmentation of vessels
        length: Whether to measure the length of blood vessels or not
    @returns:
        Saved: The vessel segmentation image
        vessel_distances_sum: The vessel length of this single image (unit: pixel)
    """

    ## 1. Vessel Segmentation
    # split the image into three channels
    image = cv2.imread(image_path)
    b, green_fundus, r = cv2.split(image)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10, 10))
    # Apply Contrast Limited Adaptive Histogram Equalization (CLAHE) to improve contrast.
    contrast_enhanced_green_fundus = clahe.apply(green_fundus)

    # applying alternate sequential filtering (3 times closing opening); cv2.morphologyEx perform
    # advanced morphological transformations using an erosion and dilation as basic operations.
    r1 = cv2.morphologyEx(contrast_enhanced_green_fundus,
                          cv2.MORPH_OPEN,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=1)
    R1 = cv2.morphologyEx(r1, cv2.MORPH_CLOSE,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=1)

    r2 = cv2.morphologyEx(R1, cv2.MORPH_OPEN,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)), iterations=1)
    R2 = cv2.morphologyEx(r2, cv2.MORPH_CLOSE,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)), iterations=1)

    r3 = cv2.morphologyEx(R2, cv2.MORPH_OPEN,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23)), iterations=1)
    R3 = cv2.morphologyEx(r3, cv2.MORPH_CLOSE,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23)), iterations=1)

    contrast_enhanced_green_fundus_blurred = cv2.GaussianBlur(contrast_enhanced_green_fundus, (5, 5),
                                                              sigmaX=250, sigmaY=250)
    f4 = cv2.subtract(R3, contrast_enhanced_green_fundus_blurred)
    clahe_1 = cv2.createCLAHE(clipLimit=3, tileGridSize=(15, 15))
    f5 = clahe_1.apply(f4)

    # removing very small contours through area parameter noise removal
    ret, f6 = cv2.threshold(f5, 15, 255, cv2.THRESH_BINARY)
    mask = np.ones(f5.shape[:2], dtype="uint8") * 255
    # find and extract contours from binary or grayscale images
    contours, hierarchy = cv2.findContours(f6.copy(), cv2.RETR_LIST,
                                           cv2.CHAIN_APPROX_SIMPLE)

    # draw contour outlines in the image
    for cnt in contours:
        if cv2.contourArea(cnt) <= 200:
            cv2.drawContours(mask, [cnt], -1, 0, -1)
    im = cv2.bitwise_and(f5, f5, mask=mask)
    ret, fin = cv2.threshold(im, 15, 255, cv2.THRESH_BINARY_INV)
    newfin = cv2.erode(fin, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1)

    # removing blobs of unwanted bigger chunks taking in consideration they are not straight lines like blood
    # vessels and also in an interval of area
    fundus_eroded = cv2.bitwise_not(newfin)
    xmask = np.ones(image.shape[:2], dtype="uint8") * 255
    xcontours, xhierarchy = cv2.findContours(fundus_eroded.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in xcontours:
        shape = "unidentified"
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * peri, False)
        if len(approx) > 4 and 3000 >= cv2.contourArea(cnt) >= 100:
            shape = "circle"
        else:
            shape = "veins"
        if shape == "circle":
            cv2.drawContours(xmask, [cnt], -1, 0, -1)
    finimage = cv2.bitwise_and(fundus_eroded, fundus_eroded, mask=xmask)
    blood_vessels = cv2.bitwise_not(finimage)

    # Bottom-hat filtering
    # Define the structuring element
    selem = disk(15)  # You can adjust the size of the structuring element as per your requirements
    # Perform the bottom-hat transform
    bottom_hat_gray = black_tophat(blood_vessels, selem)

    plt.imsave(output_path, bottom_hat_gray, cmap='gray')
    print(f"Segmented vessel image saved to {output_path}")

    ## 2. Length Calculation
    if length:
        # Skeletonization
        skel, distance = morphology.medial_axis(bottom_hat_gray, return_distance=True)
        dis_on_skel = distance * skel

        # Calculate the length for each vessel
        threshold_value = 4.3
        max_value = 255
        # Use threshold processing function to process image threshold
        ret, thresholded_image = cv2.threshold(dis_on_skel, threshold_value, max_value, cv2.THRESH_BINARY)
        count = np.count_nonzero(thresholded_image == 255)
        print("Sum of distances for vessel pixels:", count)

    else:
        count = None
    return count


def vessel_batch_segmentation(folder_path, output_folder=None, length=False):
    """
    @brief:
        Segment the blood vessels out of all the images in a folder and measure lengths.
        All processed images will be save as '***_vessel.***'
        (e.g. the input is 'abc.png', the output is automatically saved as 'abc_vessel.png')

    @args:
        folder_path: The path of input images (all files inside should be png, jpg or jpeg, and have 3 channels)
        output_path: The path to save the images of segmented blood vessels
        length: Whether to measure the length of blood vessels or not

    @returns:
        Saved: A folder containing images of segmented blood vessels
    """

    print("--------------------------------------")
    print("Start segmenting vessels in the folder")
    print("--------------------------------------")

    vessels = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            name, f_type = filename.rsplit('.', 1)
            new_name = f"{name}_vessel.{f_type}"
            image_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, new_name)
            vessel_len = vessel_segmentation(image_path, output_path, length)
            if length:
                vessels.append(vessel_len)
            else:
                vessels = None

    print("--------------------------------------")
    print("Finish segmenting vessels in the folder")
    print("--------------------------------------")

    return vessels

