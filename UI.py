import tkinter as tk
from tkinter import messagebox
import subprocess

# Function to handle Register New Student (to invoke FaceDataCollector.py)
def register_new_student():
    try:
        # Call the FaceDataCollector.py script using subprocess
        subprocess.run(["python", "FaceDataCollector.py"], check=True)
        messagebox.showinfo("Register New Student", "Student registration process completed successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "An error occurred while registering the new student.")

# Function to handle Take Attendance (to invoke FaceRecognizer.py)
def take_attendance():
    try:
        # Call the FaceRecognizer.py script using subprocess
        subprocess.run(["python", "FaceRecognizer.py"], check=True)
        messagebox.showinfo("Take Attendance", "Attendance process completed successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "An error occurred while taking attendance.")

# Function to handle View Attendance (to invoke AttendanceViewer.py)
def view_attendance():
    try:
        # Call the AttendanceViewer.py script using subprocess
        subprocess.run(["python", "AttendanceViewer.py"], check=True)
        messagebox.showinfo("View Attendance", "Displaying attendance records...")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "An error occurred while displaying attendance records.")

# Function to handle Exit
def exit_program():
    root.quit()

# Function to handle Train (invoking FaceDataTrainer.py)
def train_model():
    try:
        # Call the FaceDataTrainer.py script using subprocess
        subprocess.run(["python", "FaceDataTrainer.py"], check=True)
        messagebox.showinfo("Train", "Training completed successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "An error occurred during the training process.")

# Create the main window
root = tk.Tk()
root.title("Attendance System")

# Set the background color of the window
root.configure(background="black")

# Calculate the new width as 1.5x the original width
original_width = 600
new_width = int(original_width * 1.5)

# Set the size of the window with the new width and adjusted height
root.geometry(f"{new_width}x250")  # Adjusted window width, height remains the same

# Define a larger, bold font
button_font = ("Helvetica", 16, "bold")  # 1.5x larger than default and bold

# Create buttons with custom colors and larger/bold fonts
btn_register = tk.Button(root, text="Register New Student", width=25, height=2, command=register_new_student, bg="darkblue", fg="white", font=button_font, padx=10, pady=10)
btn_take_attendance = tk.Button(root, text="Take Attendance", width=25, height=2, command=take_attendance, bg="darkblue", fg="white", font=button_font, padx=10, pady=10)
btn_view_attendance = tk.Button(root, text="View Attendance", width=25, height=2, command=view_attendance, bg="darkblue", fg="white", font=button_font, padx=10, pady=10)
btn_exit = tk.Button(root, text="Exit", width=25, height=2, command=exit_program, bg="darkblue", fg="white", font=button_font, padx=10, pady=10)

# Arrange the buttons in a grid layout
btn_register.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
btn_take_attendance.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
btn_view_attendance.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

# Place the Exit button in the center of the second row
btn_exit.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Configure the grid to expand and fill the window
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Add a small Train button at the bottom-right corner
# Create the Train button (no image)
btn_train = tk.Button(root, text="Train", command=train_model, bg="darkblue", fg="white", font=("Helvetica", 12, "bold"), width=10, height=2)

# Place the Train button at the bottom-right corner
btn_train.grid(row=2, column=2, padx=10, pady=10, sticky="se")

# Run the application
root.mainloop()
