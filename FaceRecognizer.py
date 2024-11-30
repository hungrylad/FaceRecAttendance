import cv2
import numpy as np
import time  # For tracking time
import csv  # To read the studentdetails.csv file
import datetime  # For getting the current date
import os  # To check if attendance file exists
import tkinter as tk
from tkinter import messagebox, ttk  # Import ttk for combobox
import yaml  # To load the subject names from YAML

def face_recognizer():
    model_path = "trained_model.yml"  # Replace with your path to the trained model
    haarcasecade_path = "haarcascade_frontalface_default.xml"  # Path to Haar Cascade file
    student_details_file = "studentdetails.csv"  # Path to the CSV file
    subjects_file = "subjectNames.yml"  # Path to the subjects YAML file

    # Initialize Tkinter window (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Function to handle loading subjects from YAML
    def load_subjects():
        try:
            with open(subjects_file, 'r') as file:
                subjects = yaml.safe_load(file)
            if not subjects:
                raise ValueError("No subjects found in the file.")
            return subjects
        except FileNotFoundError:
            messagebox.showerror("Error", "Subject file not found.")
            exit()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading subjects: {e}")
            exit()

    # Function to display subject selection dropdown
    def ask_subject_name():
        subjects = load_subjects()

        # Create a new Toplevel window for input
        input_window = tk.Toplevel(root)
        input_window.title("Select Subject Name")
        input_window.geometry("400x200")
        input_window.configure(background="black")

        # Label for instructions
        label = tk.Label(input_window, text="Select the subject name:", fg="white", bg="black",
                         font=("Helvetica", 14), pady=20)
        label.pack()

        # Combobox (dropdown) for selecting subject name
        subject_name_var = tk.StringVar()
        subject_name_combo = ttk.Combobox(input_window, textvariable=subject_name_var, values=subjects,
                                          font=("Helvetica", 14), state="readonly", width=20)
        subject_name_combo.pack(pady=10)
        subject_name_combo.set("Choose a Subject")

        # Function to handle the submission of the selected subject
        def submit_subject_name(subject_name):
            # subject_name = subject_name_var.get()
            if subject_name:
                input_window.destroy()  # Close the input window
                process_subject_name(subject_name)  # Call function to process the selected subject
            else:
                messagebox.showerror("Input Error", "Please select a subject name!")

        # Submit button to process the input
        submit_button = tk.Button(input_window, text="Submit", font=("Helvetica", 14),
                                  command=lambda: submit_subject_name(subject_name_combo.get()),
                                  bg="darkblue", fg="white")

        submit_button.pack(pady=10)

        input_window.mainloop()

    # Function to process the subject name
    def process_subject_name(subject_name):
        if not subject_name:
            print("No subject name selected. Exiting...")
            exit()

        attendance_file = f"{subject_name}_attendance.csv"

        # Load the face recognition model
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read(model_path)
        except cv2.error:
            messagebox.showerror("Error", "No students registered. Register and train the model first.")
            return
        except FileNotFoundError:
            messagebox.showerror("Error", "Face model data not found.")
            return
        except Exception:
            messagebox.showerror("Error", "Error while reading face data model.")
            return

        face_cascade = cv2.CascadeClassifier(haarcasecade_path)

        students = {}
        with open(student_details_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                user_id, name = row
                students[int(user_id)] = name

        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        start_time = time.time()

        if not os.path.exists(attendance_file):
            with open(attendance_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Date", "Subject"])

        def show_attendance_ui(student_id, student_name):
            root.deiconify()
            root.title("Attendance System")
            root.configure(background="black")
            root.geometry("700x250")

            label_font = ("Helvetica", 16, "bold")
            attendance_message = f"Attendance marked for: {student_id}, {student_name} for {subject_name} on {datetime.datetime.now().strftime('%Y-%m-%d')}"
            label = tk.Label(root, text=attendance_message, fg="white", bg="black", font=label_font, pady=20)
            label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
            root.mainloop()

        while True:
            ret, frame = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            for (x, y, w, h) in faces:
                Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                if conf < 50:
                    name = students.get(Id, "Unknown")
                    if name != "Unknown":
                        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                        with open(attendance_file, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([Id, name, current_date, subject_name])

                        show_attendance_ui(Id, name)
                        cam.release()
                        cv2.destroyAllWindows()
                        return

            if time.time() - start_time > 10:
                messagebox.showinfo("Info", "Timeout reached. No match found.")
                cam.release()
                cv2.destroyAllWindows()
                break

            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(10) & 0xFF == 27:
                break

        cam.release()
        cv2.destroyAllWindows()

    ask_subject_name()

# face_recognizer()
