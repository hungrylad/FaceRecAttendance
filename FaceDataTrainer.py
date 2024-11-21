import cv2
import numpy as np
import os
from PIL import Image

# Path to the dataset directory
dataset_path = "dataset"
# Path where to save the trained model
model_path = "trained_model.yml"

# Initialize the face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Prepare training data
faces = []
ids = []

# Read images from the dataset folder
for user_folder in os.listdir(dataset_path):
    user_path = os.path.join(dataset_path, user_folder)

    if not os.path.isdir(user_path):
        continue

    # Loop through each image in the user's folder
    for image_name in os.listdir(user_path):
        image_path = os.path.join(user_path, image_name)
        image = Image.open(image_path).convert('L')  # Convert to grayscale
        image_np = np.array(image, 'uint8')

        # Extract the user ID from the image filename
        user_id = int(user_folder)
        faces.append(image_np)
        ids.append(user_id)

        # Optionally show each face being trained
        cv2.imshow("Training on image...", image_np)
        cv2.waitKey(10)

# Train the recognizer
recognizer.train(faces, np.array(ids))
# Save the trained model
recognizer.save(model_path)
print(f"[INFO] Model trained and saved at {model_path}")

cv2.destroyAllWindows()
