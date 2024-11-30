import tkinter as tk
from tkinter import messagebox
import cv2
import os
import csv


def face_data_collector():
    # Function to handle face data collection
    def collect_face_data():
        # Get user input from the UI
        user_id = entry_user_id.get()
        name = entry_name.get()

        if not user_id or not name:
            messagebox.showerror("Input Error", "Please enter both ID and Name.")
            return

        # Directory to save face images
        dataset_path = "dataset"
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)

        # Load Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Initialize webcam
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            messagebox.showerror("Webcam Error", "Could not open webcam.")
            return

        cam.set(3, 640)  # Set video width
        cam.set(4, 480)  # Set video height

        # Directory for this user's images
        user_path = os.path.join(dataset_path, user_id)
        if not os.path.exists(user_path):
            os.makedirs(user_path)

        # Create or append to the studentdetails.csv file
        student_details_file = "studentdetails.csv"

        # Check if the CSV file already exists. If not, create it with headers.
        if not os.path.exists(student_details_file):
            with open(student_details_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name"])

        # Append the new user's details (ID, Name) to the CSV file
        with open(student_details_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, name])

        # Capture face images
        count = 0
        print("[INFO] Starting to capture images. Press 'q' to quit.")
        while True:
            ret, frame = cam.read()

            if not ret:
                print("Error: Failed to capture image.")
                break  # Or retry the loop if you want

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                count += 1
                image_path = f"{user_path}/User.{user_id}.{count}.jpg"
                cv2.imwrite(image_path, gray[y:y+h, x:x+w])

                # Draw a rectangle around the face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imshow("Face", frame)

            # Exit on pressing 'q' or after capturing 100 images
            if cv2.waitKey(1) & 0xFF == ord('q') or count >= 100:
                break

        # Release resources
        print(f"[INFO] Captured {count} images for user ID {user_id}")
        cam.release()
        cv2.destroyAllWindows()

        # Close the input window after data collection is complete
        root.quit()
        root.destroy()

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Face Data Collector")

    # Set the background color
    root.configure(background="black")

    # Adjust the size of the window
    root.geometry("400x300")

    # Define a larger, bold font
    label_font = ("Helvetica", 14, "bold")
    entry_font = ("Helvetica", 12)

    # Create and place labels and input fields for User ID and Name
    label_user_id = tk.Label(root, text="Enter Your ID:", font=label_font, fg="white", bg="black")
    label_user_id.pack(pady=10)

    entry_user_id = tk.Entry(root, font=entry_font)
    entry_user_id.pack(pady=5)

    label_name = tk.Label(root, text="Enter Your Name:", font=label_font, fg="white", bg="black")
    label_name.pack(pady=10)

    entry_name = tk.Entry(root, font=entry_font)
    entry_name.pack(pady=5)

    # Create a button to start collecting face data
    btn_collect_data = tk.Button(root, text="Start Collecting Data", font=label_font, bg="darkblue", fg="white", command=collect_face_data)
    btn_collect_data.pack(pady=20)

    # Run the Tkinter event loop
    root.mainloop()