# This program is meant to take input of prerecorded .tif videos of bright objects on a dark background
# and output thresholded .tif videos, along with an excel sheet of the frame to frame displacement of each
# object for all of the imported videos!

# All code and comments written by Ryan Bowser (@maxwellbowser on github, ryanbowser@arizona.edu)
# Feel free to send me an email if you have any questions!


import pickle
import trackpy as tp
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
import os
import os.path
from datetime import date
import multiprocessing
from tkinter import filedialog as fd
import cv2

import tkinter as tk
from Phil_threshold import *
from Phil_track import *


if __name__ == '__main__':
    # This line is neccesary for proper running after being compiled with pyinstaller
    multiprocessing.freeze_support()

    # All of this is for the starting GUI (I'm guessing I could make it smaller/more efficient)
    # If you're reading this and have any advice plz let me know!
    global pixel_size
    global object_area
    global full_obj_data
    global sheet_size
    global trk_memory
    global search_range
    global trk_algo
    todays_date = date.today()

    # Handling user closing window, so that the program will end
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            exit()

    # Function for opening browse window selecting files
    def select_files():

        filetypes = (
            ('TIFF Files', '*.tif'),
            ('All files', '*.*')
        )

        global filepath
        filepath = []

        filepath = fd.askopenfilenames(
            title='Open files',
            initialdir=r'C:\Users\Desktop',
            filetypes=filetypes)

        root.destroy()

    # This will check if the default values have already been made
    # If not, it sets them to my preset values and then saves a default_value file
    settings_test = os.path.exists('Default_values.pickle')

    if settings_test == True:
        with open('Default_values.pickle', 'rb') as f:
            past_values = pickle.load(f)
        pixel_size = past_values[0]
        object_area = past_values[1]
        full_obj_data = past_values[2]
        sheet_size = past_values[3]
        trk_memory = past_values[4]
        search_range = past_values[5]
        trk_algo = past_values[6]
        fps = past_values[7]

    else:
        pixel_size = 0.139
        object_area = 25
        full_obj_data = False
        sheet_size = 10
        trk_memory = 5
        search_range = 35
        trk_algo = 'numba'
        fps = 5

        # This is the order that the values are saved
        Default_values = [pixel_size, object_area, full_obj_data,
                          sheet_size, trk_memory, search_range, trk_algo, fps]

        with open('Default_values.pickle', 'wb') as f:
            pickle.dump(Default_values, f)

    # Setting up root & frames for the starting GUI
    root = tk.Tk()
    root.title('Welcome to Philament Tracker!')
    root.geometry('540x375')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    button_frame = ttk.Frame(root,  padding="5 5 10 10")
    button_frame.grid(column=1, row=1)

    values_frame = ttk.Frame(root,  padding="5 5 10 10",
                             takefocus=True)
    values_frame.grid(column=0, row=0)

    options_frame = ttk.Frame(root,  padding="2 2 10 10")
    options_frame.grid(column=1, row=0)

    # Tkinter variables being made
    tk_full_obj_data = tk.BooleanVar(value=full_obj_data)
    tk_pixel_size = tk.DoubleVar(value=pixel_size)
    tk_object_area = tk.IntVar(value=object_area)
    tk_sheet_size = tk.IntVar(value=sheet_size)
    tk_trk_memory = tk.IntVar(value=trk_memory)
    tk_search_range = tk.IntVar(value=search_range)
    tk_fps = tk.IntVar(value=fps)
    tk_date = tk.StringVar(value=todays_date)

    # Labels being made
    ttk.Label(values_frame, text="Pixel size:", anchor="w").grid(
        column=0, row=0, padx=5, pady=5, sticky='W')
    ttk.Label(values_frame, text="Object area (In pixels):\nMUST be an ODD integer", anchor="w").grid(
        column=0, row=1, padx=5, pady=5, sticky='W')
    ttk.Label(values_frame, text="# of files per condition:", anchor="w").grid(
        column=0, row=2, padx=5, pady=5, sticky='W')
    ttk.Label(values_frame, text="Object tracking memory:\n(# of frames)", anchor="w").grid(
        column=0, row=3, padx=5, pady=5, sticky='W')
    ttk.Label(values_frame, text="Search radius:\n(pixels)", anchor="w").grid(
        column=0, row=4, padx=5, pady=5, sticky='W')
    ttk.Label(values_frame, text="Frames per second:", anchor="w").grid(
        column=0, row=5, padx=5, pady=5, sticky='W')
    ttk.Label(values_frame, text="Path linking strategy:\n(Numba is recommended)", anchor="w").grid(
        column=0, row=6, padx=5, pady=5, sticky='W')
    ttk.Label(options_frame, text="Desired Folder Name:", anchor='n').grid(
        column=0, row=1, padx=5, pady=5, sticky='N')

    # Checkbox / Entries being made
    ttk.Checkbutton(options_frame, text="Include full object data? \n(Warning: Large files)",
                    variable=tk_full_obj_data, onvalue=True, offvalue=False).grid(
        column=0, row=0, padx=10, pady=5, sticky='N')
    ttk.Entry(options_frame, width=10, textvariable=tk_date).grid(
        column=0, row=2, padx=5, pady=5)
    ttk.Entry(values_frame, textvariable=tk_pixel_size).grid(
        column=1, row=0, padx=5, pady=5)
    ttk.Entry(values_frame, textvariable=tk_object_area).grid(
        column=1, row=1, padx=5, pady=5)
    ttk.Entry(values_frame, textvariable=tk_sheet_size).grid(
        column=1, row=2, padx=5, pady=5)
    ttk.Entry(values_frame, textvariable=tk_trk_memory).grid(
        column=1, row=3, padx=5, pady=5)
    ttk.Entry(values_frame, textvariable=tk_search_range).grid(
        column=1, row=4, padx=5, pady=5)
    ttk.Entry(values_frame, textvariable=tk_fps).grid(
        column=1, row=5, padx=5, pady=5)
    menubut = ttk.Menubutton(values_frame, text='Select One')
    menubut.grid(column=1, row=6, padx=5, pady=5)

    file = tk.Menu(menubut, tearoff=0)
    menubut["menu"] = file

    # Functions for buttons
    def set_value(x):
        global trk_algo
        trk_algo = x

    def close_window():
        root.destroy()
        exit()

    # Making RadioButtons (would've made with a for loop to save space, but it caused problems, and this is more readable anyways)
    file.add_radiobutton(
        label='Numba',
        command=lambda: set_value('numba'))
    file.add_radiobutton(
        label='Recursive',
        command=lambda: set_value('recursive'))
    file.add_radiobutton(
        label='Nonrecursive',
        command=lambda: set_value('nonrecursive'))
    file.add_radiobutton(
        label='Drop',
        command=lambda: set_value('drop'))
    file.add_radiobutton(
        label='Auto',
        command=lambda: set_value('auto'))

    browse_button = ttk.Button(
        button_frame,
        text='Browse',
        command=select_files
    ).grid(column=1, row=0, padx=1, pady=5)

    close_button = ttk.Button(
        button_frame,
        text='Cancel',
        command=close_window
    ).grid(column=0, row=0, padx=1, pady=5)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    # Setting regular variables equal to the tkinter variables
    # This also updates the default values, so they will be saved the next time you run the program
    try:
        pixel_size = tk_pixel_size.get()
        object_area = tk_object_area.get()
        full_obj_data = tk_full_obj_data.get()
        sheet_size = tk_sheet_size.get()
        trk_memory = tk_trk_memory.get()
        search_range = tk_search_range.get()
        fps = tk_fps.get()
        chosen_dir_name = tk_date.get()
    except:
        showinfo(title='Whoops!',
                 message='Error: Invalid Input\nPlease restart program')
        exit()
    Default_values = [pixel_size, object_area, full_obj_data,
                      sheet_size, trk_memory, search_range, trk_algo, fps]
    with open('Default_values.pickle', 'wb') as f:
        pickle.dump(Default_values, f)

    # Folder creation and changing cwd
    try:
        dir_name = str(chosen_dir_name) + ' - Analyzed Files'
        current_dir = os.getcwd()
        new_dir = current_dir + "\\" + dir_name
        os.mkdir(new_dir)
        os.chdir(new_dir)

    except FileExistsError:
        showinfo(
            "Error", "Folder already exists!\nPlease delete or move the folder and try again.")
        exit()

# If the user closes the window, this handles it & closes the program
    try:
        threshold_value = threshold_value_testing(filepath)
    except:
        showinfo(title='Program Closed',
                 message='Goodbye, have a good day! :)')
        exit()

    # Progress bar design (nothing super cool/ interesting)
    list_len = len(filepath)

    root = tk.Tk()
    root.title('Progress Bar')
    root.geometry('300x150')
    frame = ttk.Frame(root)
    frame.grid(column=0, row=1, padx=0, pady=2)

    frame_2 = ttk.Frame(root)
    frame_2.grid(column=0, row=0, padx=0, pady=2)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    progress = tk.StringVar()
    items = tk.StringVar(value=str(list_len))

    prgbr_title = ttk.Label(frame_2,
                            text="Total Progress: \nThresholding & Saving Files! :)").grid(column=0, row=0, padx=1, pady=1)

    prgbr_progress = ttk.Label(
        frame, textvariable=progress).grid(column=0, row=0, padx=1, pady=3)

    of_label = ttk.Label(frame, text="out of ").grid(
        column=1, row=0, padx=1, pady=3)

    prgbr_total = ttk.Label(frame, textvariable=items).grid(
        column=2, row=0, padx=1, pady=3)

    thresholding_files(filepath, threshold_value, progress, root)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.destroy()
    frame.mainloop()
    cv2.waitKey()

    # w/o this, trackpy prints lots of information that's useless for the user, so I silenced it
    tp.quiet()

    thresholded_tifs = []
    split_list = []

    # By finding all filepaths that end in .tif in the working directory (where the thresholded videos are saved)
    # This function is able to automatically find the filepaths for the newly thresholded videos
    for x in os.listdir():
        if x.endswith('.tif'):
            thresholded_tifs.append(x)

    # Breaking the list into nested lists, to separate sample condition data into different sheets
    split_list = [thresholded_tifs[i:i + sheet_size]
                  for i in range(0, len(thresholded_tifs), sheet_size)]

    # Same progress bar code from above
    list_len = len(thresholded_tifs)

    root = tk.Tk()
    root.title('Progress Bar')
    root.geometry('300x150')
    frame = ttk.Frame(root)
    frame.grid(column=0, row=1, padx=0, pady=2)

    frame_2 = ttk.Frame(root)
    frame_2.grid(column=0, row=0, padx=0, pady=2)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    progress = tk.IntVar(frame_2)
    items = tk.StringVar(value=str(list_len))

    prgbr_title = ttk.Label(frame_2,
                            text="Total Progress: \nTracking & Saving Files! :)").grid(column=0, row=0, padx=1, pady=1)

    prgbr_progress = ttk.Label(
        frame, textvariable=progress).grid(column=0, row=0, padx=1, pady=3)

    of_label = ttk.Label(frame, text="out of ").grid(
        column=1, row=0, padx=1, pady=3)

    prgbr_total = ttk.Label(frame, textvariable=items).grid(
        column=2, row=0, padx=1, pady=3)

    # This function takes care of all the tracking, linking, data analysis, and data formatting
    tracking_data_analysis(split_list, progress, root, Default_values)


# Incase user clicks the red x and wants to shutdown the program.
    root.protocol("WM_DELETE_WINDOW", on_closing)

    showinfo(title="Finished",
             message=f"All Files Tracked and Saved")

# Opens folder where files were saved
    folder = os.getcwd()
    os.startfile(folder)
