# Python code to interface with the RADbox lite model. Plots data in real time and saves it to a CSV file

import sys
import subprocess
import serial
import serial.tools.list_ports
import csv
import time
from datetime import datetime
import os

# IN MAC: Configure the graphics backend before importing pyplot to avoid black screens
import matplotlib
matplotlib.use('TkAgg')

# Native libraries used to display the folder selection dialog window
import tkinter as tk
from tkinter import filedialog

# The plotting stuff is a wee bit jank, so there is some code there that ignores an error message doesn't matter 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import backend_bases
if not sys.warnoptions:
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning,
                            message="Treat the new Tool classes introduced in v1.5 as experimental for now")
plt.rcParams['toolbar'] = 'toolmanager'

import seaborn as sns


# Arduino raw inputs; try/except clause because I kept forgetting to plug it in
try:
    # Automatically detects the arduino port
    ports = list(serial.tools.list_ports.comports())
    for devi in ports:
        if "Arduino" in devi.description or "USB Serial Device" in devi.description or "usbserial" in devi.device or "Arduino" in devi.device:
            arduino_port = devi.device
            print(f"RADBox detected on the port: {arduino_port}")


    baud = 115200 
    serial_connection = serial.Serial(arduino_port, baud)
    serial_connection.reset_input_buffer()  # MAC: Flushes the serial buffer input noise
except:
    print("Please plug in the arduinoo.")
    sys.exit()

# folder selection

print("Please select the target folder to save the CSV data report...")
root = tk.Tk()
root.withdraw() # Hides the small blank Tkinter master window
root.keepfile = True
root.lift()
root.attributes("-topmost", True) 

# Opens the native directory explorer dialog box
save_directory = filedialog.askdirectory(title="Select Destination Folder for CSV Reports")

#  If the user cancels or closes the dialog window, default to the Desktop
if not save_directory:
    save_directory = os.path.expanduser("~/Desktop")
    print(f"No folder was selected. Defaulting path to Desktop: {save_directory}")
else:
    print(f"Target folder selected: {save_directory}")

# Set up CSV; name is given with time so that multiple runs can be done consecutively. File name involves a different unicode character that looks like a colon (but isn't), to avoid issues
not_colon = "-"  # zero-width space character

nombre_archivo = datetime.now().strftime(f"raw-data-%Y-%m-%d-%H{not_colon}%M{not_colon}%S.csv")
csv_file = os.path.join(save_directory, nombre_archivo)


file = open(csv_file, "a")

# Getting user input and reading that many samples
user_input = input("How many samples would you like to take? 12 scans takes roughly 1 minute.\n")

# This try/except clause checks to see if the user input an integer
try:
    number_of_samples = int(user_input)
except:
    print("Please input an integer (e.g. 1, 2, 3...)")
    exit()
else:
    # Estimates how long it will take
    sampling_time = (number_of_samples * 5)/60  # takes one sample every 5 secs
    print(
        f"It will take roughly {round(sampling_time, 2)} minute(s) to collect the data."
        )

time_data = []
raw_data = []
x_axis_max = (number_of_samples * 5.5)

print("Collecting data...")
time.sleep(0.5)                          
serial_connection.reset_input_buffer()   
serial_connection.readline()
start_time = time.time() # start the timer

# Plotting stuff
sns.set_style("ticks")
fig = plt.figure()
plt.xlim(0, x_axis_max)

plt.title(r"CO$_2$ Levels Over Time", fontsize=16)
plt.xlabel("Time (s)", fontsize=14)
plt.ylabel(r"CO$_2$ (ppm)", fontsize=14)
plt.xticks(fontsize=12, rotation=45)
plt.yticks(fontsize=12, rotation=0)

# The plot
ln, = plt.plot(time_data, raw_data, '-o')

# The following is to remove some navigation buttons 
# Full list of navigation buttons: forward, back, pan, zoom, home, help, subplots, save
buttons_names = ['forward', 'back', 'help', 'subplots']

for button in buttons_names:
    fig.canvas.manager.toolmanager.remove_tool(button)

count = 0

def update(i):

    global count

    if count >= number_of_samples:
        return ln,

    if serial_connection.in_waiting > 0:
        try:
            get_data = serial_connection.readline()
            data_string = get_data.decode('utf-8')
            data_string_parsed = data_string[0:][:-2]

            total_time = round((time.time() - start_time), 2)

            float_val = float(data_string_parsed)
            raw_data.append(float_val)
            time_data.append(total_time)

            count += 1
            print(f"Time: {total_time}, CO2: {float_val} \n")

            ln.set_data(time_data, raw_data)

            raw_data_min = min(raw_data)
            raw_data_max = max(raw_data)

            plt.ylim(raw_data_min - 100, raw_data_max + 100)

            real_time_sample_counting = f"Samples left: {number_of_samples - count}"

            plt.legend([str(float_val)], title=real_time_sample_counting)

            sns.despine()
        except ValueError:
            return ln,
        
    if count == number_of_samples:
        all_data = zip(time_data, raw_data) 
        with open(csv_file, 'w', encoding='UTF8', newline='') as f:
            data_headers = ["Time (s)", "CO2 (ppm)"]
            writer = csv.writer(f)
            writer.writerow(data_headers)
            writer.writerows(all_data)
        file.close()
        print("Data collection is complete!")
        
    return ln,

animation = FuncAnimation(fig, update, interval=1000, blit=False, cache_frame_data=False)
plt.show()

# If the user breaks out of the collection process early, this will save their currently collected results
if count < number_of_samples and count > 0:
    all_data = zip(time_data, raw_data)
    
    with open(csv_file, 'w', encoding='UTF8', newline='') as f:
        data_headers = ["Time (s)", "CO2 (ppm)"]

        writer = csv.writer(f)
        writer.writerow(data_headers)
        writer.writerows(all_data)

    file.close()

    print("Data collection stopped early!")