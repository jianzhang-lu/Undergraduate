# BIA4 Project: Retina Scan (by Group 10) 
## Note that this README file is not the documentation for users. It is used to record the structure of our project, and the function of each file.
## Introduction
Welcome! Our software can be used to segment optical disk regions, detect whether images represent glaucoma or not, segment blood vessels and calculate the overall length of vessels. This `README file` will include a brief introduction to every file in our project.  

- **For users**: If you want to use our software and generate some results, you can ignore this `README file`, directly download the `RetinaScan_Software.zip`, and read the documentation (`Documentation.pdf`). This zipped file contains the necessary model files and Python files to get outputs.  

- **For developers**: If you want to retrain the model using your own dataset/see how we establish and train the model/reproduce or add some functions of our software, you can read the `README file` to know the function of each file in our project, read the documentation  `Documentation.pdf` to know how to use it, and clone this repository to modify the codes/files. 

## Structure
### The center of our software
- `requirements.txt`: Contains the necessary packages needed for our software. You can read the documentation to use it and download the needed packages.
- `RetinaScan.py`: The main file of the software, integrating all functions (optical disk region segmentation, glaucoma classification, vessel segmentation, vessel length calculation). Also contains command-line interface to allow customized inputs and error-tracking mechanisms to handle incorrect user inputs and return related information to let them know the incorrect parts.
- `Predict_OD.py`: Generate optical disk predictions for the input images, and then use these masks to crop the images, focusing on the optical disk region.
- `Classification_Glaucoma.py`: Predict whether the images represent glaucoma or not.
- `Vessel_Segment.py`: Segment blood vessels of input images and calculate the length of vessels.
- `model-unet-best.h5`: The trained U-Net model for optical disk segmentation.
- `model-Xception-best-1.h5`: The trained Xception model for glaucoma segmentation. The input for training is whole fundus images.
- `model-Xception-best-2.h5`: The trained Xception model for glaucoma segmentation. The input for training is cropped images focusing on the optical disk region.

### Test
- `Test_in_image`: Contain different examples to show the functions of our software if the input is a single image (both correct and incorrect).
- `Test_in_folder`: Contains different examples to show the functions of our software if the input is a folder containing many images (both correct and incorrect).

**Please see the documentation for detailed usages**. 

### Data
- `ORIGA`: This dataset contains 650 whole fundus images (482 normal; 168 glaucoma). It is used to train the optical disk segmentation model `model-unet-best.h5` and one of the glaucoma classification models `model-Xception-best-1.h5`.
- `glaucoma.csv`: Contains the metadata of the ORIGA dataset.
- `ORIGA_cropped`: This contains the corresponding cropped images of the ORIGA dataset focusing on the optical disk region. They are generated by our U-Net model `model-unet-best-1.h5` and used to train the other glaucoma classification model `model-Xception-best-2.h5`. 
- `Semi-automatic-annotations`: This contains the ground truth of the optical disk segmentation of the ORIGA dataset. It is used to train the U-Net model `model-unet-best.h5`.
- `ACRIMA`: Another dataset contains 705 cropped images focusing on the optical disk region (309 normal; 396 glaucoma). It is used to test the effectiveness of the classification model trained by cropped ORIGA images `model-Xception-best-2.h5`.
- `Vessel_Segmentation`: This contains our vessel segmentation images for the ORIGA dataset and a summary file to record the vessel length of each image `Vessel_length.csv`.

### Appendix
- `Visualization.py`: This file is used to draw some plots for visualization in the summary report (The heatmaps for HyperTuning results; The Loss and Metrics during the epochs...)
- `Segmentation & Classification`: Contains the whole process of training the U-Net/Xception model for segmentation/classification. (`Loader.py`: Load and split the data; `Model.py`: U-Net/Xception architecture to do the segmentation/classification; `Model_consuming.py`: A better but time-consuming architecture to do the segmentation, not used in this project; `Train.py`: Train the model, including hyperparameter tuning; `Evaluate.py`: Evaluate our model on the test dataset).
- `Segmentation/Results`: Include some results for further analyses (`HyperTune.xlsx`: The results of hyperparameter tuning; `trainHistoryDict.txt`: The changes of loss and metrics during the training; `.npy`: Contains the information of train, validation, and test dataset and can be used directly in the training process to save time). 
- `Classification/Results`: Similar structure as the `Segmentation/Results` folder. Contains dataset information and results for two models (`Original`: model-Xception-best-1.h5; `Cropped`: model-Xception-best-2.h5). 

### !!!Note!!!
Due to the restore limitation of GitHub, we cannot upload all `.npy` files. If you want to retrain the model using our codes and datasets, please first run the `Appendix/Segmentation/Loader.py` and `Appendix/Classification/Loader.py` to get all `.npy` files for the U-Net/Xception training. The following codes are already included in the `Loader.py` and should be uncommented and run.
```python
##### In the Appendix/Segmentation/Loader.py #####
data_loader = Loader(image_dir='../../data/ORIGA/',
                     mask_dir='../../data/Semi-automatic-annotations/',
                     csv_path='../../data/glaucoma.csv')
images, masks = data_loader.preprocess_data(data_loader.image_paths,
                                            data_loader.mask_paths)
data_loader.get_data_split(images, masks, test_size=0.1, random_state=10)


##### In the Appendix/Classification/Loader.py #####
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
```
After that, you can retrain the U-Net model or Xception models. The following codes should be uncommented and run in the `Appendix/Segmentation/Train.py` or `Appendix/Classification/Train.py`.
```python
##### In the Appendix/Segmentation/Train.py #####
train = Train('Results/')
history = train.train_model()
with open('Results/trainHistoryDict.txt', 'wb') as file_pi:
  pickle.dump(history.history, file_pi)


##### In the Appendix/Classification/Train.py #####
# 1. Train the model_1 (From the original image)
train = Train('Results/Original/', 'Xception_tuner_1')
history = train.train_model('model-Xception-best-1.h5', 12)
with open('Results/Original/trainHistoryDict_1.txt', 'wb') as file_pi:
    pickle.dump(history.history, file_pi)
print('Finish training the model 1')

# 2. Train the model_2 (From the cropped image)
train = Train('Results/Cropped/', 'Xception_tuner_2')
history = train.train_model('model-Xception-best-2.h5', 13)
with open('Results/Cropped/trainHistoryDict_2.txt', 'wb') as file_pi:
    pickle.dump(history.history, file_pi)
print('Finish training the model 2')
```

Finally, if you want to evaluate your Xception model using the ACRIMA dataset, please run the following code in the `Appendix/Classification/Evaluate.py` to restore the `.npy` (x_test.npy & y_test.npy) files for the ACRIMA dataset.
```python
process_ACRIMA('../../data/ACRIMA')
```





