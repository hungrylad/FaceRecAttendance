If facing errors related to dependencies from python packages, create a virtual environment and install dependencies in it.

1. To create a virtual environment, open powershell as administrator on windows and execute the following command in order to allow permissions to start a python virtual environment:

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

2. Then, in the terminal of your code editor, run the following command,

    .\venv\Scripts\Activate

This activates your virtual environment.
=============================

install all python dependencies in your virtual environment required for the following imports-
numpy, pillow, pandas, tkinter, opencv-contrib-python, os, csv, time, datetime
