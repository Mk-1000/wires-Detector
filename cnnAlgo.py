import sys
import cv2
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import os


def CNNTest(image_path):
    # Define the size of the images
    IMG_SIZE = 32

    # Get a list of all the .npz files in the connector_dataset directory
    dataset_dir = "dataset"
    dataset_files = []
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith('.npz'):
                dataset_files.append(os.path.join(root, file))

    # Define a threshold for similarity between images
    SIMILARITY_THRESHOLD = 0.8

    # Load and train on each dataset
    for dataset_path in dataset_files:

        # Load the dataset
        dataset = np.load(dataset_path, allow_pickle=True)

        X_train = dataset['images']
        y_train = dataset['labels']
        class_names = dataset['class_names']

        # Encode the string labels to integer labels
        encoder = LabelEncoder()
        y_train = encoder.fit_transform(y_train)

        # Add a new dimension to X_train
        X_train = np.expand_dims(X_train, axis=-1)

        # Normalize the pixel values
        X_train = X_train / 255.0

        # Define the CNN model architecture
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=X_train.shape[1:]),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(len(class_names))
        ])

        # Compile the model
        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

        # Train the model
        model.fit(X_train, y_train, epochs=10)

        # Load the new image
        if getattr(sys, 'frozen', False):
            # If the script is run as a bundled executable, get the absolute path of the file
            image_path = os.path.join(sys._MEIPASS, image_path)

        new_image = cv2.imread(image_path)

        # Preprocess the new image
        gray_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
        _, thresholded_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
        resized_image = cv2.resize(thresholded_image, (IMG_SIZE, IMG_SIZE))
        X_new = np.array([resized_image])

        # Add a new dimension to X_new
        X_new = np.expand_dims(X_new, axis=-1)

        # Normalize the pixel values
        X_new = X_new / 255.0

        # Predict the class of the new image
        y_new = model.predict(X_new)
        class_index = np.argmax(y_new)
        predicted_class_name = encoder.inverse_transform([class_index])[0]
        try:
            # Compare the new image with each image in the dataset
            for i, x_train in enumerate(X_train):
                similarity = np.corrcoef(x_train.ravel(), X_new.ravel())[0, 1]
                if similarity >= SIMILARITY_THRESHOLD:
                    # print(f"The new image is similar to an image in {dataset_path}. The similar image has class name {class_names[y_train[i]]}.")

                    datasetname = dataset_path.split("\\")[-1].split("_")[0]
                    datasetname = " ".join(datasetname.split())
                    print(f"The name of the connactor is {datasetname}")

                    return (datasetname)
        except:
            return ("none")

# print(CNNTest("connector_images/connector1_images/IMG-20230307-WA0009.jpg"))
