import os
import cv2
import numpy as np


def creatdataset():
    # Set the data directory to the connector_images directory
    DATA_DIR = 'connector_images'

    # Define the list of valid image extensions
    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']

    # Define the size of the images
    IMG_SIZE = 32

    # Define the threshold value for the connector segmentation
    THRESHOLD_VALUE = 200

    # Loop over each directory in the data directory
    for connector_dir in os.listdir(DATA_DIR):
        # Create a path to the connector directory
        connector_path = os.path.join(DATA_DIR, connector_dir)
        dataset_name = connector_path.split("\\")[-1].split("_")[0]

        if os.path.isdir(connector_path):
            # Create a list to store the image data and labels
            images = []
            labels = []

            # Loop over each file in the connector directory
            for filename in os.listdir(connector_path):
                # Check if the file is an image file
                if any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                    # Load the image
                    image_path = os.path.join(connector_path, filename)
                    image = cv2.imread(image_path)

                    # Convert the image to grayscale
                    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    # Apply thresholding to separate the connector from the background
                    _, thresholded_image = cv2.threshold(gray_image, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)

                    # Resize the thresholded image to IMG_SIZE x IMG_SIZE pixels
                    resized_image = cv2.resize(thresholded_image, (IMG_SIZE, IMG_SIZE))

                    # Append the image data and label to the lists
                    images.append(resized_image)
                    labels.append(filename)

            # Save the image data and labels to an npz file
            if images:
                dataset_father_path = os.path.join("dataset", dataset_name)
                dataset_path = os.path.join(dataset_father_path, f"{connector_dir}_{IMG_SIZE}.npz")
                np.savez(dataset_path, images=np.array(images), labels=np.array(labels),
                         class_names=np.array(list(set(labels))))
                print(f'{dataset_path} file saved')