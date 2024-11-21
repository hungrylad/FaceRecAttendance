import cv2
import numpy as np
import time  # For tracking time
import csv  # To read the studentdetails.csv file
import datetime  # For getting the current date
import os  # To check if attendance file exists
import tkinter as tk
from tkinter import messagebox  # Import messagebox
import subprocess

# Paths to the pre-trained model and Haar Cascade classifier
model_path = "trained_model.yml"  # Replace with your path to the trained model
haarcasecade_path = "haarcascade_frontalface_default.xml"  # Path to Haar Cascade file
student_details_file = "studentdetails.csv"  # Path to the CSV file

# Initialize Tkinter window (hidden)
root = tk.Tk()
root.withdraw()  # Hide the root window

# Function to handle user input for subject name
def ask_subject_name():
    # Create a new Toplevel window for input
    input_window = tk.Toplevel(root)
    input_window.title("Enter Subject Name")
    input_window.geometry("400x200")
    input_window.configure(background="black")

    # Label for instructions
    label = tk.Label(input_window, text="Enter the subject name:", fg="white", bg="black", font=("Helvetica", 14), pady=20)
    label.pack()

    # Text entry widget for the user to enter the subject name
    subject_name_entry = tk.Entry(input_window, font=("Helvetica", 14), width=20)
    subject_name_entry.pack(pady=10)

    # Function to handle the submission of the subject name
    def submit_subject_name():
        subject_name = subject_name_entry.get()
        if subject_name:
            input_window.destroy()  # Close the input window
            process_subject_name(subject_name)  # Call function to process the subject name
        else:
            messagebox.showerror("Input Error", "Please enter a subject name!")

    # Submit button to process the input
    submit_button = tk.Button(input_window, text="Submit", font=("Helvetica", 14), command=submit_subject_name, bg="darkblue", fg="white")
    submit_button.pack(pady=10)

    # Start the input window loop
    input_window.mainloop()

# Function to process the subject name (after it's submitted)


def process_subject_name(subject_name):
    if not subject_name:
        print("No subject name entered. Exiting...")
        exit()

    # Prepare the file to store attendance (subject-wise)
    attendance_file = f"{subject_name}_attendance.csv"

    # Load the face recognition model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)  # Load the pre-trained model

    # Load Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(haarcasecade_path)

    # Load students (ID-to-name mapping) from studentdetails.csv
    students = {}
    with open(student_details_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            user_id, name = row
            students[int(user_id)] = name  # Map the ID to the name

    # Open a connection to the webcam
    cam = cv2.VideoCapture(0)

    # Set font for displaying names on the image
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Track the start time
    start_time = time.time()

    # Create or append to the attendance CSV file (if it doesn't exist, create it)
    if not os.path.exists(attendance_file):
        with open(attendance_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Date", "Subject"])  # Header for attendance CSV

    # Function to display the attendance confirmation UI without action buttons
    def show_attendance_ui(student_id, student_name):
        # Show the Tkinter window for attendance
        root.deiconify()  # Show the root window

        # Set up the window layout
        root.title("Attendance System")
        root.configure(background="black")
        root.geometry("700x250")

        # Define a larger, bold font for the display
        label_font = ("Helvetica", 16, "bold")

        # Display attendance message
        attendance_message = f"Attendance marked for: {student_id}, {student_name} for {subject_name} on {datetime.datetime.now().strftime('%Y-%m-%d')}"
        label = tk.Label(root, text=attendance_message, fg="white", bg="black", font=label_font, pady=20)
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Keep the window open to display the message
        root.mainloop()

    # Loop until a match is found or 10 seconds have passed
    while True:
        # Capture a frame from the webcam
        ret, frame = cam.read()
        if not ret:
            break

        # Convert the frame to grayscale (LBPH works with grayscale images)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        # Loop over each detected face
        for (x, y, w, h) in faces:
            # Predict the ID of the detected face
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            # Check confidence threshold (e.g., conf < 70 for a confident match)
            if conf < 70:
                # Get the name associated with the recognized ID
                name = students.get(Id, "Unknown")
                recognition_status = f"Recognized: ID = {Id}, Name = {name}"

                # If confidence is low, do not mark attendance and show the "No match found" message
                if name == "Unknown":
                    recognition_status = "No match found, attendance not marked."
                    print(recognition_status)

                    # Display the message in Tkinter window
                    root.deiconify()  # Show the root window
                    label_font = ("Helvetica", 16, "bold")
                    label = tk.Label(root, text=recognition_status, fg="white", bg="black", font=label_font, pady=20)
                    label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

                    # Keep the window open to display the message
                    root.mainloop()

                    # Do not log attendance if no match is found
                    cam.release()
                    cv2.destroyAllWindows()
                    return

                color = (0, 255, 0)  # Green if recognized
                print(recognition_status)

                # Get the current date for attendance log
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")

                # Log the attendance (ID, Name, Date, Subject)
                with open(attendance_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([Id, name, current_date, subject_name])

                # Draw a rectangle around the face and display the name
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, f"{name} ({round(conf, 2)})", (x, y-10), font, 0.9, color, 2)

                # Show the custom Tkinter UI with the student details
                show_attendance_ui(Id, name)

                # Break the loop as soon as a match is found
                cv2.imshow("Face Recognition", frame)
                cam.release()
                cv2.destroyAllWindows()
                break

        # Check for timeout (10 seconds)
        elapsed_time = time.time() - start_time
        if elapsed_time > 10:
            print("Timeout reached. No match found.")
            cam.release()
            cv2.destroyAllWindows()
            break

        # Show the frame with detected faces
        cv2.imshow("Face Recognition", frame)

        # Break the loop if 'Esc' is pressed (optional, but will still allow Esc to break if desired)
        if cv2.waitKey(10) & 0xFF == 27:
            break

    # Release resources
    cam.release()
    cv2.destroyAllWindows()

# Start the process to ask for the subject name
ask_subject_name()
