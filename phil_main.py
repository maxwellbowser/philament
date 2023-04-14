# This program is meant to take input of prerecorded .tif videos of bright objects on a dark background
# and output thresholded .tif videos, along with a csv file with the frame to frame displacements of each
# object for all of the imported videos!

# All code and comments written by Ryan Bowser (@maxwellbowser on github, ryanbowser@arizona.edu)
# Feel free to send me an email if you have any questions!


import trackpy as tp
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
import os
import os.path
from datetime import date

# import multiprocessing
from tkinter import filedialog as fd
import cv2
import sys
from time import time


import tkinter as tk

from phil_threshold import *
from phil_track import *

# Want to change from pickled lists to dicts stored as Json files
import json

if __name__ == "__main__":
    # This line is neccesary for proper running after being compiled with pyinstaller
    # multiprocessing.freeze_support()

    todays_date = date.today()

    # Handling user closing window, so that the program will end

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit()

    # Function for opening browse window selecting files
    def select_files():

        if was_avi == True:
            filetypes = (
                ("AVI Files", "*.avi"),
                ("TIFF Files", "*.tif"),
                ("All Files", "*.*"),
            )

        else:
            filetypes = (
                ("TIFF Files", "*.tif"),
                ("AVI Files", "*.avi"),
                ("All Files", "*.*"),
            )

        global filepath
        filepath = []

        filepath = fd.askopenfilenames(
            title="Open files", initialdir=r"C:\Users\Desktop", filetypes=filetypes
        )

        root.destroy()

    """
    Naming_Indices:
    Input: naming_input is a string, containing exactly 2 "*" characters
    Output: slash_positions is a tuple, containing the 2 reverse indices of the "*" contained text
    
    This function takes in a string (naming_input), and returns the reverse indices of whatever is contained between
    the two lines. I chose to do reverse indices, because our file naming system will increase the length of the file-
    name in the front of the string, but the file number is in the back of the string.
    e.g
    1Lmod-01, 10Lmod-01, 100Lmod-01 | Reverse index is unaffected

    Later in the script, the selected file names will have Thresh- prefixes and .tif suffixes added, which is accounted for
    by adding them before finding the indices.

    e.g.
    naming_input is "100-Tropomodulin*01*"
    This means the normal filename would be "100-Tropomodulin01"
    The future actual filename would be "Thresh-100-Tropomodulin01.tif"
    slash_positions = (-6, -4)
    
    So eventually, when filename = Thresh-100-Tropomodulin01.tif, 
    filename[slash_positions[0]:slash_positions[1]] returns "01"       
    """

    def Naming_Indices(naming_input):
        slash_positions = []
        naming_input = (
            "Thresh-" + naming_input + ".tif"
        )  # The suffix could also be .avi

        test_list = list(naming_input)

        counter = 0
        for char in test_list:
            if char == "*":
                slash_positions.append(counter)

            counter += 1

        if len(slash_positions) > 2:
            showinfo(
                title="Naming Convention",
                message="Please check naming convention, and only suround the file number with one asterisk (*) on each side.\ne.g. Filename-*01*",
            )
            sys.exit()
        try:
            slash_positions = (
                slash_positions[0] - len(naming_input) + 2,
                slash_positions[1] - len(naming_input) + 1,
            )
        except IndexError:
            showinfo(
                "Uh Oh!",
                "You forgot to surround the Naming Convention file number with asterisks (*)! \nPlease restart Phil and try again...",
            )
        return slash_positions

    # This will check if the default values have already been made
    # If not, it sets them to our preset values and then creates a default_value file
    if os.path.exists("Phil-Settings.json") == True:
        f = open("Phil-Settings.json")
        settings = json.load(f)

    else:
        settings = {
            "pixel_size": 0.139,
            "object_area": 25,
            "sheet_size": 10,
            "trk_memory": 5,
            "search_range": 35,
            "fps": 5,
            "was_avi": False,
            "full_obj_data": False,
            "naming_convention": "ActinMyosin-*01*",
        }

    global was_avi
    was_avi = settings["was_avi"]

    # Setting up root & frames for the starting GUI
    root = tk.Tk()
    root.title("Welcome to Philament!")
    root.geometry("550x425")
    root.minsize(450, 370)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    button_frame = ttk.Frame(root, padding="5 5 10 10")
    button_frame.grid(column=1, row=1)

    values_frame = ttk.Frame(root, padding="5 5 10 10", takefocus=True)
    values_frame.grid(column=0, row=0)

    options_frame = ttk.Frame(root, padding="2 2 10 10")
    options_frame.grid(column=1, row=0)

    # Tkinter variables being made
    tk_full_obj_data = tk.BooleanVar(value=settings["full_obj_data"])
    tk_pixel_size = tk.DoubleVar(value=settings["pixel_size"])
    tk_object_area = tk.IntVar(value=settings["object_area"])
    tk_sheet_size = tk.IntVar(value=settings["sheet_size"])
    tk_trk_memory = tk.IntVar(value=settings["trk_memory"])
    tk_search_range = tk.IntVar(value=settings["search_range"])
    tk_fps = tk.IntVar(value=settings["fps"])
    tk_date = tk.StringVar(value=todays_date)
    tk_file_name = tk.StringVar(value=settings["naming_convention"])

    # Labels being made
    ttk.Label(values_frame, text="Pixel size (Microns):", anchor="w").grid(
        column=0, row=0, padx=5, pady=5, sticky="W"
    )
    ttk.Label(
        values_frame,
        text="Object area (In pixels):\nMUST be an odd integer",
        anchor="w",
    ).grid(column=0, row=1, padx=5, pady=5, sticky="W")
    ttk.Label(values_frame, text="# of files per condition:", anchor="w").grid(
        column=0, row=2, padx=5, pady=5, sticky="W"
    )
    ttk.Label(
        values_frame, text="Object tracking memory:\n(# of frames)", anchor="w"
    ).grid(column=0, row=3, padx=5, pady=5, sticky="W")
    ttk.Label(values_frame, text="Search radius:\n(pixels)", anchor="w").grid(
        column=0, row=4, padx=5, pady=5, sticky="W"
    )
    ttk.Label(values_frame, text="Frames per second:", anchor="w").grid(
        column=0, row=5, padx=5, pady=5, sticky="W"
    )
    ttk.Label(
        values_frame,
        text="Naming Convention:\nSurround file number with '*'",
        anchor="w",
    ).grid(column=0, row=6, padx=5, pady=5, sticky="W")
    ttk.Label(options_frame, text="Desired Folder Name:", anchor="n").grid(
        column=0, row=1, padx=5, pady=5, sticky="N"
    )

    # Checkbox / Entries being made
    ttk.Checkbutton(
        options_frame,
        text="Include full object data? \n(Warning: Large files)",
        variable=tk_full_obj_data,
        onvalue=True,
        offvalue=False,
    ).grid(column=0, row=0, padx=10, pady=5, sticky="N")
    ttk.Entry(options_frame, width=10, textvariable=tk_date).grid(
        column=0, row=2, padx=5, pady=5
    )
    ttk.Entry(values_frame, textvariable=tk_pixel_size).grid(
        column=1, row=0, padx=5, pady=5
    )
    ttk.Entry(values_frame, textvariable=tk_object_area).grid(
        column=1, row=1, padx=5, pady=5
    )
    ttk.Entry(values_frame, textvariable=tk_sheet_size).grid(
        column=1, row=2, padx=5, pady=5
    )
    ttk.Entry(values_frame, textvariable=tk_trk_memory).grid(
        column=1, row=3, padx=5, pady=5
    )
    ttk.Entry(values_frame, textvariable=tk_search_range).grid(
        column=1, row=4, padx=5, pady=5
    )
    ttk.Entry(values_frame, textvariable=tk_fps).grid(column=1, row=5, padx=5, pady=5)

    ttk.Entry(values_frame, textvariable=tk_file_name).grid(
        column=1, row=6, padx=5, pady=5
    )

    def close_window():
        root.destroy()
        sys.exit()

    browse_button = ttk.Button(button_frame, text="Browse", command=select_files).grid(
        column=1, row=0, padx=1, pady=5
    )

    close_button = ttk.Button(button_frame, text="Cancel", command=close_window).grid(
        column=0, row=0, padx=1, pady=5
    )

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    # Setting regular variables equal to the tkinter variables
    # This also updates the default values, so they will be saved the next time you run the program
    try:
        settings["pixel_size"] = tk_pixel_size.get()
        settings["object_area"] = tk_object_area.get()
        settings["full_obj_data"] = tk_full_obj_data.get()
        settings["sheet_size"] = tk_sheet_size.get()
        settings["trk_memory"] = tk_trk_memory.get()
        settings["search_range"] = tk_search_range.get()
        settings["fps"] = tk_fps.get()
        chosen_dir_name = tk_date.get()
        settings["naming_convention"] = tk_file_name.get()
    except:
        showinfo(
            title="Whoops!",
            message="Error: Invalid Input\nPlease restart program and ensure parameters are in correct format",
        )
        sys.exit()

    name_index = Naming_Indices(settings["naming_convention"])

    threshold_value, is_avi = threshold_value_testing(filepath)

    settings["was_avi"] = is_avi

    with open("Phil-Settings.json", "w") as f:
        json.dump(settings, f, indent=4)

    f = open("Phil-Settings.json")
    settings = json.load(f)

    # Folder creation and changing cwd
    try:
        dir_name = str(chosen_dir_name) + " - Analyzed Files"
        current_dir = os.getcwd()
        new_dir = current_dir + "\\" + dir_name
        os.mkdir(new_dir)
        os.chdir(new_dir)

    except FileExistsError:
        showinfo(
            "Error",
            "Chosen folder name already exists!\nPlease delete or move the folder and try again.",
        )
        folder = os.getcwd()
        os.startfile(folder)
        sys.exit()

    start_time = int((time()) * 1000)

    # Progress bar design (nothing super cool/ interesting)
    list_len = len(filepath)

    root = tk.Tk()
    root.title("Progress Bar")
    root.geometry("300x150")

    frame = ttk.Frame(root)
    frame.grid(column=0, row=1, padx=0, pady=2)

    frame_2 = ttk.Frame(root)
    frame_2.grid(column=0, row=0, padx=0, pady=2)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    progress = tk.StringVar()
    items = tk.StringVar(value=str(list_len))

    prgbr_title = ttk.Label(
        frame_2, text="Total Progress: \nThresholding & Saving Files! :)"
    ).grid(column=0, row=0, padx=1, pady=1)

    prgbr_progress = ttk.Label(frame, textvariable=progress).grid(
        column=0, row=0, padx=1, pady=3
    )

    of_label = ttk.Label(frame, text="out of ").grid(column=1, row=0, padx=1, pady=3)

    prgbr_total = ttk.Label(frame, textvariable=items).grid(
        column=2, row=0, padx=1, pady=3
    )

    thresholding_files(
        filepath, threshold_value, progress, root, is_avi, settings["fps"]
    )

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
        thresholded_tifs.append(x)

    # Breaking the list into nested lists, to separate sample condition data into different sheets
    split_list = [
        thresholded_tifs[i : i + settings["sheet_size"]]
        for i in range(0, len(thresholded_tifs), settings["sheet_size"])
    ]

    # Same progress bar code from above
    list_len = len(thresholded_tifs)

    root = tk.Tk()
    root.title("Progress Bar")
    root.geometry("300x150")

    frame = ttk.Frame(root)
    frame.grid(column=0, row=1, padx=0, pady=2)

    frame_2 = ttk.Frame(root)
    frame_2.grid(column=0, row=0, padx=0, pady=2)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    progress = tk.IntVar(frame_2)
    items = tk.StringVar(value=str(list_len))

    prgbr_title = ttk.Label(
        frame_2, text="Total Progress: \nTracking & Saving Files! :)"
    ).grid(column=0, row=0, padx=1, pady=1)

    prgbr_progress = ttk.Label(frame, textvariable=progress).grid(
        column=0, row=0, padx=1, pady=3
    )

    of_label = ttk.Label(frame, text="out of ").grid(column=1, row=0, padx=1, pady=3)

    prgbr_total = ttk.Label(frame, textvariable=items).grid(
        column=2, row=0, padx=1, pady=3
    )

    # This function takes care of all the tracking, linking, data analysis, and data formatting
    tracking_data_analysis(split_list, progress, root, settings, name_index, is_avi)

    # Incase user clicks the red x and wants to shutdown the program.
    root.protocol("WM_DELETE_WINDOW", on_closing)

    end_time = int((time()) * 1000)
    elapsed_time = end_time - start_time
    elapsed_time_sec = round(elapsed_time / 1000, 2)
    elapsed_time_min = round(elapsed_time_sec / 60, 2)
    print(f"Total time to run was {elapsed_time_sec} sec or {elapsed_time_min} min")

    showinfo(title="Finished", message=f"All Files Tracked and Saved")

    # Opens folder where files were saved, so user can access them right away
    folder = os.getcwd()
    os.startfile(folder)
