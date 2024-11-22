import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def attendance_viewer():
    # Function to scan the project directory for attendance files
    def scan_for_attendance_files(directory):
        attendance_files = []
        for file_name in os.listdir(directory):
            if file_name.endswith("_attendance.csv"):
                subject_name = file_name.replace("_attendance.csv", "")
                attendance_files.append(subject_name)
        return attendance_files

    # Function to read the attendance data from the CSV file
    def read_attendance_file(subject_name):
        file_name = f"{subject_name}_attendance.csv"
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                content = file.readlines()
            return content
        else:
            return None

    # Function to sort the data by Date and ID
    def sort_data_by_date_and_id(attendance_data):
        # Skip the header row and sort the rest of the data by Date and ID
        data = [line.strip().split(",") for line in attendance_data[1:]]

        # Convert date string to datetime object for correct sorting
        for row in data:
            row[2] = datetime.strptime(row[2], "%Y-%m-%d")  # Convert date string to datetime

        # Sort first by date, and then by ID within each date
        sorted_data = sorted(data, key=lambda x: (x[2], int(x[0])))  # Sorting by date, then by ID
        return sorted_data

    # Function to display the attendance data in a grid format (Treeview)
    def show_attendance(subject_name, selected_date=None):
        # Read and sort the attendance data
        attendance_data = read_attendance_file(subject_name)

        if not attendance_data:
            messagebox.showerror("Error", f"No attendance data found for {subject_name}.")
            return

        # Filter data by selected date if provided
        sorted_data = sort_data_by_date_and_id(attendance_data)
        if selected_date:
            sorted_data = [line for line in sorted_data if line[2].strftime("%Y-%m-%d") == selected_date]

        # Create a new window to display the attendance data
        attendance_window = tk.Toplevel()
        attendance_window.title(f"Attendance for {subject_name}")

        # Set the background and window size
        attendance_window.configure(background="black")
        attendance_window.geometry("600x400")

        # Create a Treeview widget to display the attendance data in a grid format
        tree = ttk.Treeview(attendance_window, columns=("ID", "Name", "Date", "Subject"), show="headings")
        tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Define the column headings
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Date", text="Date")
        tree.heading("Subject", text="Subject")

        # Define the column width
        tree.column("ID", width=50)
        tree.column("Name", width=150)
        tree.column("Date", width=100)
        tree.column("Subject", width=100)

        # Apply styling to the grid (black background and white text)
        tree.tag_configure("even", background="black", foreground="white")
        tree.tag_configure("odd", background="gray", foreground="white")

        # Insert the sorted attendance data into the treeview (sorted by Date and ID)
        for i, line_data in enumerate(sorted_data):
            # Alternate row colors for better readability
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=(line_data[0], line_data[1], line_data[2].strftime("%Y-%m-%d"), line_data[3]), tags=(tag,))

        # Add a Close button similar to the buttons for other UI
        btn_close = tk.Button(attendance_window, text="Close", command=attendance_window.destroy, bg="darkblue", fg="white", font=("Helvetica", 12, "bold"))
        btn_close.pack(pady=10)

    # Function to create the UI with buttons for each subject
    def create_ui_with_buttons(subjects):
        root = tk.Tk()
        root.title("Attendance System")

        # Set the background color of the window
        root.configure(background="black")

        # Define a larger, bold font for the buttons
        button_font = ("Helvetica", 16, "bold")

        # Create a grid layout for buttons, dynamically generating buttons based on subjects
        for i, subject in enumerate(subjects):
            row = i // 2  # Adjust row index (2 buttons per row)
            col = i % 2   # Adjust column index

            # Create a button for each subject
            btn = tk.Button(root, text=subject, command=lambda s=subject: show_subject_details(s), bg="darkblue", fg="white", font=button_font, width=20, height=2)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        # Add a "Exit" button at the bottom of the grid layout
        btn_exit = tk.Button(root, text="Exit", command=root.quit, bg="darkblue", fg="white", font=("Helvetica", 16, "bold"), width=20, height=2)
        btn_exit.grid(row=len(subjects) // 2 + 1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Configure grid to make buttons expand proportionally
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Run the Tkinter main loop
        root.geometry("500x500")
        root.mainloop()

    # Function to show the subject details with a date dropdown
    def show_subject_details(subject_name):
        subject_window = tk.Toplevel()
        subject_window.title(f"Attendance for {subject_name}")

        # Set the background and window size
        subject_window.configure(background="black")
        subject_window.geometry("600x400")

        # Create a dropdown to select the date
        unique_dates = get_unique_dates(subject_name)
        date_combobox = ttk.Combobox(subject_window, values=unique_dates, state="readonly", font=("Helvetica", 14))
        date_combobox.pack(pady=20)

        # Add a button to show the attendance for the selected date
        def on_date_select(event):
            selected_date = date_combobox.get()
            show_attendance(subject_name, selected_date)

        date_combobox.bind("<<ComboboxSelected>>", on_date_select)

    # Function to get unique dates from the attendance file
    def get_unique_dates(subject_name):
        dates = set()
        attendance_data = read_attendance_file(subject_name)
        for line in attendance_data[1:]:
            date = line.strip().split(",")[2]
            dates.add(date)
        return sorted(list(dates))

    # Scan the current directory for attendance files
    attendance_files = scan_for_attendance_files(".")

    # Check if there are any attendance files
    if attendance_files:
        # Create the UI with buttons for each subject
        create_ui_with_buttons(attendance_files)
    else:
        messagebox.showerror("No Attendance Files", "No attendance files found in the project directory.")

# You can call the function if you want it to run when the script is executed
if __name__ == "__main__":
    attendance_viewer()
