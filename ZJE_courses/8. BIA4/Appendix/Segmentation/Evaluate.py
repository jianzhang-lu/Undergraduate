"""
Created on 2023/11/19

This class is used to evaluate our U-Net model on the test dataset
"""
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model

from Train import IoU_cal, f1_score


class ModelEvaluator:
    """
    A class for model evaluation

    :attribute model: The trained model (*.h5)
    """
    def __init__(self, model_path):
        self.model = load_model(model_path, custom_objects={'IoU_cal': IoU_cal, 'f1_score': f1_score})

    def unet_evaluate(self, x_test, y_test):
        """
        @brief:
            Evaluate the model performance
        @args:
            x_test: The test images
            y_test: The ground truth of test images
        @returns:
            The final evaluation results
        """
        eval_results = self.model.evaluate(x_test, y_test, batch_size=8)
        return eval_results

    def display_sample_prediction(self, x_test, y_test):
        """
        @brief:
            Display a random test image, its prediction image, and the ground truth
        @args:
            x_test: The test images
            y_test: The ground truth of test images
        @returns:
            A plot to show the ground truth and our predicted mask
        """
        test_img_number = np.random.randint(0, len(x_test))
        test_img = x_test[test_img_number]
        ground_truth = y_test[test_img_number]

        # Elevating dimension to meet the needs of 'predict' (batch_size, w, h, c)
        prediction = self.model.predict(np.expand_dims(test_img, axis=0))[0]

        plt.figure(figsize=(12, 4))

        plt.subplot(1, 3, 1)
        plt.imshow(test_img)
        plt.title('Test Image')

        plt.subplot(1, 3, 2)
        plt.imshow(ground_truth.squeeze(), cmap='gray')
        plt.title('Ground Truth')

        plt.subplot(1, 3, 3)
        plt.imshow(prediction.squeeze(), cmap='gray')
        plt.title('Prediction')

        plt.show()


# Test the function
x_test = np.load('Results/x_test.npy')
y_test = np.load('Results/y_test.npy')

evaluator = ModelEvaluator('../../model-unet-best.h5')
res = evaluator.unet_evaluate(x_test, y_test)
evaluator.display_sample_prediction(x_test, y_test)
