"""
Created on 2023/12/4
Modified on 2023/12/15  (Adding the functions related to vessel properties)

The main file of the software, mainly having these functions:
(1) Integrating all functions: Segmentation the optical disk region + Classify glaucoma + vessel length
(2) Adding Command-line-interface to allow customized inputs
(3) Error tracking: Handle incorrect user input and return related information to let them know the incorrect parts.
"""

import argparse
from skimage.io import imread
import os

import pandas as pd
from Predict_OD import SegmentationOD
from Classification_Glaucoma import Classification
from Vessel_Segment import vessel_segmentation, vessel_batch_segmentation


# Only display the error and warning information
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'


def Parse_args():
    """
    @brief:
        Use argparse to make the code command-line executable
    @returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(prog='RetinaScan.py',
                                     description='Retina Scan: This software can be used to automatically segment '
                                                 'the optical disk region from the whole fundus images, and detect '
                                                 'whether images represent glaucoma or not. Additionally, our software '
                                                 'provides vessel properties like length.',
                                     epilog='You can read the documentation or summary report for '
                                            'detailed explanation.')

    # 1. About the input file:
    parser.add_argument('-i', '--input_path',
                        metavar='',
                        help="The path of the input image or a folder containing many images. "
                             "The type of input images should be 'png', 'jpg' or 'jpeg', "
                             "and encoded with three channels.",
                        required=True,
                        type=str)

    parser.add_argument('-t', '--type',
                        choices=['whole', 'cropped'],
                        default='whole',
                        help="Type of the input images: 'whole' for whole fundus images, "
                             "'cropped' for cropped images focusing on the optical disk region. \n"
                             "If you input a folder containing many images, please make sure they are in the same type "
                             "(all represent the whole fundus or all represent the cropped images).")

    # 2. About the vessel length
    parser.add_argument('-l', '--length',
                        help='Whether to calculate the vessel lengths of your input images. \n'
                             'If added, our software will include the vessel lengths into the final result file. \n'
                             'NOTA THAT you can only set this parameter if your input images represent whole fundus '
                             '(-t whole). It is impossible to segment the vessels and calculate lengths '
                             'if your inputs are cropped images focusing on the optical disk region (-t cropped).',
                        action="store_true")

    # 3. About the output
    parser.add_argument('-o', '--output_folder',
                        metavar='',
                        type=str,
                        required=True,
                        help="The output folder to save the cropped images/classification results/vessel properties.")

    args = parser.parse_args()
    return args


def RetinaScan():
    """
    @brief:
        Main functions combining all functions.
        Include handling incorrect user input and returning related information to let them know the incorrect parts.
    @returns:
        Error messages/or return TRUE if everything is correct.
        The final output is a .csv file containing information about classification.
        If the input is whole fundus images (-t whole), the output will also include the cropped images focusing on
        the optical disk region. The .csv file will contain the vessel properties.
    """

    args = Parse_args()
    # Error 0: the inputs are cropped images and set the -l
    if args.length and args.type == 'cropped':
        print("Error: We can not calculate the vessel length if your inputs are cropped images. Please use whole "
              "fundus images instead or do not set -l/--length to ignore the length calculation.")
        return

    # Error 1: We cannot find the input image/folder.
    if not os.path.exists(args.input_path):
        print(f"Error: The path '{args.input_path}' does not exist.")
        return

    # Situation 1: The input is one single image
    if os.path.isfile(args.input_path):
        # Error 2: The file type is not correct.
        filename = os.path.basename(args.input_path)  # abc.jpg
        name, f_type = filename.rsplit('.', 1)  # abc; jpg
        new_cropped_name = f"{name}_cropped.{f_type}"  # abc_cropped.jpg
        new_vessel_name = f"{name}_vessel.{f_type}"  # abc_vessel.jpg

        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print("Error: Your input file should be .png/.jpg/.jpeg.")
            return

        # Error 3: The image is not encoded in 3 channels.
        image = imread(args.input_path)
        if len(image.shape) != 3:
            print("Error: Your input image should be encoded in 3 channels (RGB).")
            return

        # Check the output path and create the new output path.
        if not os.path.exists(args.output_folder):
            os.makedirs(args.output_folder)
        output_crop_path = os.path.join(args.output_folder, new_cropped_name)
        output_vessel_path = os.path.join(args.output_folder, new_vessel_name)

        # Perform the segmentation and classification
        seg = SegmentationOD('model-unet-best.h5')
        cla = Classification('model-Xception-best-2.h5')

        # If the input is the whole fundus image, we will first crop the optical disk region and then classify
        # If the input is already the cropped image, we will directly classify
        if args.type == 'whole':
            cropped_image = seg.process_single_image(args.input_path, output_crop_path, True)
        else:
            cropped_image = seg.preprocess_image(image)

        prediction = cla.classify_single_image(cropped_image)
        if prediction == 0:
            classification = 'non-Glaucoma'
            print('This image may represent non-Glaucoma.')
        else:
            classification = 'Glaucoma'
            print('This image may represent Glaucoma.')

        # Vessel Segmentation & Vessel length calculation
        if args.type == 'whole':
            if args.length:
                vessel_len = vessel_segmentation(args.input_path, output_vessel_path, True)
                result_file = pd.DataFrame({'Filename': filename,
                                            'Classification': classification,
                                            'Vessel_length': round(vessel_len, 0)}, index=[0])
            else:
                _ = vessel_segmentation(args.input_path, output_vessel_path, False)
                result_file = pd.DataFrame({'Filename': filename,
                                            'Classification': classification}, index=[0])
        else:
            result_file = pd.DataFrame({'Filename': filename,
                                        'Classification': classification}, index=[0])

        result_path = os.path.join(args.output_folder, 'results.csv')
        if os.path.exists(result_path):
            os.remove(result_path)
        result_file.to_csv(result_path)

    # Situation 2: The input is a folder contain many images: We will only process the files end with png/jpg/jpeg.
    else:
        # Error 4: One specific file is not encoded in 3 channels
        for filename in os.listdir(args.input_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(args.input_path, filename)
                image = imread(image_path)
                if len(image.shape) != 3:
                    print(f"Error: Your input image '{filename}' should be encoded in 3 channels (RGB)")
                    return

        # Perform the segmentation and classification
        seg = SegmentationOD('model-unet-best.h5')
        cla = Classification('model-Xception-best-2.h5')

        # Check the output path and create the new output path.
        if not os.path.exists(args.output_folder):
            os.makedirs(args.output_folder)
        output_cropped_folder, output_vessel_folder = None, None

        if args.type == 'whole':
            output_cropped_folder = os.path.join(args.output_folder, 'optical_disk')
            if not os.path.exists(output_cropped_folder):
                os.makedirs(output_cropped_folder)

            output_vessel_folder = os.path.join(args.output_folder, 'vessel')
            if not os.path.exists(output_vessel_folder):
                os.makedirs(output_vessel_folder)

        # If the input is the whole fundus image, we will first crop the optical disk region and then classify
        # If the input is already the cropped image, we will directly classify
        if args.type == 'whole':
            cropped_images, final_filenames = seg.process_images_in_folder(args.input_path, output_cropped_folder, True)
        else:
            final_filenames = []
            cropped_images = []

            for filename in os.listdir(args.input_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    final_filenames.append(filename)
                    process_path = os.path.join(args.input_path, filename)
                    process_image = imread(process_path)
                    cropped_image = seg.preprocess_image(process_image)
                    cropped_images.append(cropped_image)

        predictions = cla.classify_images_in_folder(cropped_images)
        classifications = []
        for prediction in predictions:
            if prediction == 0:
                classifications.append('non-Glaucoma')
            else:
                classifications.append('Glaucoma')

        # Vessel Segmentation & Vessel length calculation
        if args.type == 'whole':
            if args.length:
                vessel_lens = vessel_batch_segmentation(args.input_path, output_vessel_folder, True)
                vessel_lens = [round(i, 0) for i in vessel_lens]
                result_file = pd.DataFrame({'Filename': final_filenames,
                                            'Classification': classifications,
                                            'Vessel_length': vessel_lens})
            else:
                _ = vessel_batch_segmentation(args.input_path, output_vessel_folder, False)
                result_file = pd.DataFrame({'Filename': final_filenames,
                                            'Classification': classifications})
        else:
            result_file = pd.DataFrame({'Filename': final_filenames,
                                        'Classification': classifications})

        result_path = os.path.join(args.output_folder, 'results.csv')
        if os.path.exists(result_path):
            os.remove(result_path)
        result_file.to_csv(result_path)


if __name__ == '__main__':
    RetinaScan()

