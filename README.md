Run UI.py to access functionalities.

1. Register a new student (face data collected during registration via Webcam, make sure Webcam is active and accessible)
2. Train the model for the collected data after registrations are done, using 'Train' button at the bottom right
3. To mark attendance, click on 'Take Attendance', enter the subject name. Attendance will be marked if the face of the student is recognized based on face data previously collected on which the model has been trained.
4. To view marked attendances, click on 'View Attendance', select a subject name. This opens a pop-up with a drop down to choose the date for which attendance will be shown.
5. Select the date from the drop down to view attendance.
6. 'Exit' to close the program.

===================================================================================

If facing errors related to dependencies from python packages, create a virtual environment and install dependencies in it.

1. To create a virtual environment, open powershell as administrator on windows and execute the following command in order to allow permissions to start a python virtual environment:

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

2. Then, in the terminal of your code editor, run the following command,

    .\venv\Scripts\Activate


Install all python dependencies in your virtual environment required for the following imports-
numpy, pillow, pandas, tkinter, opencv-contrib-python, os, csv, time, datetime

for eg. pip install opencv-contrib-python,
pip install numpy..... and so on
