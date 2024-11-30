import sys
import tkinter as tk
from tkinter import messagebox
import subprocess
from AttendanceViewer import attendance_viewer
from FaceDataTrainer import train_face_data_model
from FaceRecognizer import face_recognizer
from FaceDataCollector import face_data_collector
from PIL import Image, ImageTk  # Importing the required modules for image handling

# Function to handle Register New Student (to invoke FaceDataCollector.py)
def register_new_student():
    try:
        # Call the face_data_collector function
        face_data_collector()
        messagebox.showinfo("Register New Student", "Student registration process completed successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "An error occurred while registering the new student.")

# Function to handle Take Attendance (to invoke FaceRecognizer.py)
def take_attendance():
    try:
        # Call the face_recognizer function
        face_recognizer()
        messagebox.showinfo("Mark Attendance", "Attendance process completed successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "An error occurred while taking attendance.")

# Function to handle View Attendance (to invoke AttendanceViewer.py)
def view_attendance():
    try:
        # Call the attendance_viewer method directly
        attendance_viewer()
        messagebox.showinfo("View Attendance", "Displaying attendance records...")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while displaying attendance records: {e}")

# Function to handle Exit
def exit_program():
    sys.exit()

# Function to handle Train (invoking FaceDataTrainer.py)
def train_model():
    try:
        # Call the train_model function directly
        train_face_data_model()
        messagebox.showinfo("Train", "Training completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the training process: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Attendance System")

# Set the size of the window to be square
window_size = 850  # Set both width and height to the same value to make the window square
root.geometry(f"{window_size}x{window_size-150}")

# Load the background image using PIL
background_image = Image.open("myImage.jpg")  # Open the image
background_image = background_image.resize((window_size, window_size))  # Resize the image to fit the square window
background_photo = ImageTk.PhotoImage(background_image)  # Convert image to a Tkinter-compatible format

# Create a label with the image as background
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)  # Cover the entire window

# Add scrolling, bouncing text
label = tk.Label(root, text="Attendance using Face Recognition", font=("Helvetica", 20, "bold"), fg="black", bg="yellow")  # Black text with no background
label.place(x=0, y=40)  # Position the text at the top of the window

# Initialize direction to move text right (1) or left (-1)
direction = 1

# Function to move the text left to right and right to left
def scroll_text():
    global direction

    # Get the current position of the label
    current_position = label.winfo_x()

    # Get the width of the window and label
    window_width = root.winfo_width()
    label_width = label.winfo_width()

    # If the label reaches the right edge, change direction to move left
    if current_position + label_width >= window_width:
        direction = -1

    # If the label reaches the left edge, change direction to move right
    elif current_position <= 0:
        direction = 1

    # Move the label by 5 pixels in the current direction
    label.place(x=current_position + (5 * direction), y=40)

    # Call the scroll_text function every 50 milliseconds to update the label position
    root.after(50, scroll_text)

# Initialize the text scroll
scroll_text()

# Define a larger, bold font for the buttons
button_font = ("Helvetica", 16, "bold")

# Create buttons with custom colors and larger/bold fonts
btn_register = tk.Button(root, text="Register New Student", width=25, height=2, command=register_new_student, bg="darkblue", fg="white", font=button_font, padx=10, pady=10)
btn_take_attendance = tk.Button(root, text="Mark Attendance", width=25, height=2, command=take_attendance, bg="darkblue", fg="white", font=button_font, padx=10, pady=10)
btn_view_attendance = tk.Button(root, text="View Attendance", width=25, height=2, command=view_attendance, bg="darkblue", fg="white", font=button_font, padx=10, pady=10)

# Arrange the buttons in a grid layout below the scrolling text
btn_register.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
btn_take_attendance.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
btn_view_attendance.grid(row=2, column=2, padx=10, pady=10, sticky="ew")


# Define the Exit button and the Train button with the adjusted size
btn_exit = tk.Button(root, text="Exit", width=10, height=2, command=exit_program, bg="darkblue", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=10)
btn_train = tk.Button(root, text="Train", command=train_model, bg="darkblue", fg="white", font=("Helvetica", 12, "bold"), width=10, height=2, padx=10, pady=10)

# Place the Exit button and the Train button in the bottom-right corner of the window
btn_train.grid(row=3, column=0, padx=10, pady=10, sticky="sw")
btn_exit.grid(row=3, column=2, padx=10, pady=10, sticky="se")

# Configure the grid to expand and fill the window
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)


# Run the application
root.mainloop()
