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
        data = [line.strip().split(",") for line in attendance_data[1:]]  # Skip header
        for row in data:
            row[2] = datetime.strptime(row[2], "%Y-%m-%d")  # Convert date string to datetime
        sorted_data = sorted(data, key=lambda x: (x[2], int(x[0])))  # Sort by date, then ID
        return sorted_data

    # Function to display attendance data in a Treeview
    def show_attendance(subject_name, selected_date=None):
        attendance_data = read_attendance_file(subject_name)
        if not attendance_data:
            messagebox.showerror("Error", f"No attendance data found for {subject_name}.")
            return

        sorted_data = sort_data_by_date_and_id(attendance_data)
        if selected_date:
            sorted_data = [line for line in sorted_data if line[2].strftime("%Y-%m-%d") == selected_date]

        attendance_window = tk.Toplevel()
        attendance_window.title(f"Attendance for {subject_name}")
        attendance_window.configure(background="black")
        attendance_window.geometry("600x400")

        tree = ttk.Treeview(attendance_window, columns=("ID", "Name", "Date", "Subject"), show="headings")
        tree.pack(padx=10, pady=10, fill="both", expand=True)
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Date", text="Date")
        tree.heading("Subject", text="Subject")
        tree.column("ID", width=50)
        tree.column("Name", width=150)
        tree.column("Date", width=100)
        tree.column("Subject", width=100)
        tree.tag_configure("even", background="black", foreground="white")
        tree.tag_configure("odd", background="gray", foreground="white")

        for i, line_data in enumerate(sorted_data):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=(line_data[0], line_data[1], line_data[2].strftime("%Y-%m-%d"), line_data[3]), tags=(tag,))

        btn_close = tk.Button(attendance_window, text="Close", command=attendance_window.destroy, bg="darkblue", fg="white", font=("Helvetica", 12, "bold"))
        btn_close.pack(pady=10)

    def create_ui_with_dropdown(subjects):
        root = tk.Tk()
        root.title("Attendance Viewer")
        root.configure(background="black")
        root.geometry("400x200")

        label = tk.Label(root, text="Select a subject:", bg="black", fg="white", font=("Helvetica", 16))
        label.pack(pady=10)

        subject_combobox = ttk.Combobox(root, values=subjects, state="readonly", font=("Helvetica", 14))
        subject_combobox.pack(pady=10)
        subject_combobox.set("Choose a Subject")

        def on_subject_select():
            selected_subject = subject_combobox.get()
            if selected_subject:
                show_subject_details(selected_subject)

        btn_show_attendance = tk.Button(root, text="Show Attendance", command=on_subject_select, bg="darkblue", fg="white", font=("Helvetica", 14, "bold"))
        btn_show_attendance.pack(pady=20)

        btn_exit = tk.Button(root, text="Exit", command=root.quit, bg="darkblue", fg="white", font=("Helvetica", 14, "bold"))
        btn_exit.pack(pady=10)

        root.mainloop()

    def show_subject_details(subject_name):
        subject_window = tk.Toplevel()
        subject_window.title(f"Attendance for {subject_name}")
        subject_window.configure(background="black")
        subject_window.geometry("600x400")

        unique_dates = get_unique_dates(subject_name)
        date_combobox = ttk.Combobox(subject_window, values=unique_dates, state="readonly", font=("Helvetica", 14))
        date_combobox.set("Choose a Date")
        date_combobox.pack(pady=20)

        def on_date_select(event):
            selected_date = date_combobox.get()
            show_attendance(subject_name, selected_date)

        date_combobox.bind("<<ComboboxSelected>>", on_date_select)

    def get_unique_dates(subject_name):
        dates = set()
        attendance_data = read_attendance_file(subject_name)
        for line in attendance_data[1:]:
            date = line.strip().split(",")[2]
            dates.add(date)
        return sorted(list(dates))

    attendance_files = scan_for_attendance_files(".")
    if attendance_files:
        create_ui_with_dropdown(attendance_files)
    else:
        messagebox.showerror("No Attendance Files", "No attendance files found in the project directory.")

# if __name__ == "__main__":
#     attendance_viewer()
