'''
Created on Aug 9, 2022

@author: panch
'''

from datetime import date
import multiprocessing
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
import os
import os.path
import xlsxwriter

import cv2

from numpy import array
import openpyxl as op
import pandas as pd
from pandas import ExcelWriter
import tifffile as tif
import tkinter as tk
import trackpy as tp
import random
from multiprocessing import freeze_support
from statistics import mean
import pickle

# This program is meant to take input of prerecorded .tif videos of bright objects on a dark background
# and output thresholded .tif videos, along with an excel sheet of the mean squared displacement of each
# object for all the imported videos!

# All code and comments written by Ryan Bowser (@maxwellbowser on github, ryanbowser@arizona.edu)
# Feel free to send me an email if you have any questions!

if __name__ == '__main__':

    # This line is neccesary for proper running after being compiled with pyinstaller
    multiprocessing.freeze_support()

    todays_date = date.today()

    # All of this is for the starting GUI (I'm guessing I could make it smaller/more efficient)
    # If you're reading this and have any advice plz let me know!

    global pixel_size
    global object_diameter
    global full_obj_data
    global sheet_size
    global trk_memory
    global search_range
    global trk_algo

    # Function for opening browse window selecting files
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            exit()

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
        object_diameter = past_values[1]
        full_obj_data = past_values[2]
        sheet_size = past_values[3]
        trk_memory = past_values[4]
        search_range = past_values[5]
        trk_algo = past_values[6]
        fps = past_values[7]

    else:
        pixel_size = 0.139
        object_diameter = 25
        full_obj_data = False
        sheet_size = 10
        trk_memory = 5
        search_range = 35
        trk_algo = 'numba'
        fps = 5

        # This is the order that the values are saved
        Default_values = [pixel_size, object_diameter, full_obj_data,
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

    # Variables being made
    tk_full_obj_data = tk.BooleanVar(value=full_obj_data)
    tk_pixel_size = tk.DoubleVar(value=pixel_size)
    tk_object_diameter = tk.IntVar(value=object_diameter)
    tk_sheet_size = tk.IntVar(value=sheet_size)
    tk_trk_memory = tk.IntVar(value=trk_memory)
    tk_search_range = tk.IntVar(value=search_range)
    tk_fps = tk.IntVar(value=fps)
    tk_date = tk.StringVar(value=todays_date)

    # Labels being made
    ttk.Label(values_frame, text="Pixel size:", anchor="w").grid(
        column=0, row=0, padx=5, pady=5, sticky='W')
    ttk.Label(values_frame, text="Object diameter:\nMUST be an ODD integer", anchor="w").grid(
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
    ttk.Entry(values_frame, textvariable=tk_object_diameter).grid(
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
        object_diameter = tk_object_diameter.get()
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
    Default_values = [pixel_size, object_diameter, full_obj_data,
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
            "Error", "Folder already exists!\nPlese delete or move the folder and try again.")
        exit()

    # Gui to help user find best thresholding value for videos (Picks a random chosen video to use)
    # For larger sample sizes more videos will be tested
    # Always at least 1 video, and capped at 5 if n > 200 (n is selected files)

    def threshold_value_testing(List_of_Filepaths):
        multiples_of_50 = len(List_of_Filepaths) // 50
        if multiples_of_50 == 1:
            num_files_for_threshold = 2
        elif multiples_of_50 == 2:
            num_files_for_threshold = 3
        elif multiples_of_50 == 3:
            num_files_for_threshold = 4
        elif multiples_of_50 >= 4:
            num_files_for_threshold = 5
        else:
            num_files_for_threshold = 1

        try:
            rand_file_num = random.sample(
                range(0, len(List_of_Filepaths)), num_files_for_threshold)
            thresh_values = []
        except:
            print('Please re-run program, and make sure to select files!')
            exit()

        # running the thresholding picker gui
        for i in range(0, len(rand_file_num)):

            def close():
                window.destroy()
                cv2.destroyAllWindows()

            # the arg values being passed to the function is meant to not be used (I promise im not dumb)
            def double_check(values):

                threshold_value = value.get()

                blur = cv2.medianBlur(checking_images[0], 5)

                ret, thresholded_checked = cv2.threshold(
                    blur, threshold_value, 255, cv2.THRESH_BINARY_INV)

                cv2.imshow('Thresholded Image', thresholded_checked)
                cv2.imshow('Original Image', checking_images[0])
                cv2.waitKey(5)

            window = tk.Tk()
            window.title('Checking Thresholding Value')
            window.resizable(False, False)
            window.geometry('425x250')

            thresh_check_frame = ttk.Frame(window, padding='5 5 10 10')
            thresh_check_frame.grid(column=0, row=0)
            window.columnconfigure(0, weight=1)
            window.rowconfigure(0, weight=1)

            checking_images = []
            current_num = i+1

            loaded, checking_images = cv2.imreadmulti(
                mats=checking_images, filename=List_of_Filepaths[rand_file_num[i]], flags=cv2.IMREAD_GRAYSCALE)

            # Here 100 is just a default starting point for the thresholding value
            value = tk.IntVar(thresh_check_frame, 100)

            # Widgets! I chose not to show threshold value to eliminate human bias % simplicity
            slider = ttk.Scale(thresh_check_frame, from_=255, to=0, orient='horizontal',
                               variable=value, command=double_check, length=200).grid(column=0, row=1)

            cont_but = ttk.Button(thresh_check_frame, text='Continue', command=close).grid(
                column=1, row=1, padx=10, pady=5)

            old_thresh_label = ttk.Label(thresh_check_frame, text='Select best thresholding value:',
                                         font=12).grid(column=0, row=0, padx=20, pady=10)
            ttk.Label(thresh_check_frame, text=f'Image {current_num} out of {num_files_for_threshold}').grid(
                column=1, row=0, padx=20, pady=10)

            double_check(0)
            thresh_check_frame.mainloop()
            thresh_values.append(value.get())

        # setting the thresholding value to be used when thresholding
        threshold_value = int(mean(thresh_values))
        return threshold_value


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

    # Start of the data analysis, the thresholding and saving of files
    try:

        for i in range(0, len(filepath)):

            # incase someone selects non-files
            assert os.path.isfile(filepath[i])
            try:

                threshold_images = []
                original_images = []

                loaded, original_images = cv2.imreadmulti(
                    mats=original_images, filename=f"{filepath[i]}", flags=cv2.IMREAD_GRAYSCALE)

                filename = os.path.basename(filepath[i])

                for x in range(0, len(original_images)):

                    # Image processing (blur & thresholding)
                    blur = cv2.medianBlur(original_images[x], 5)

                    ret, image = cv2.threshold(
                        blur, threshold_value, 255, cv2.THRESH_BINARY_INV)

                    threshold_images.append(image)

                    # Saving thresholded tiff images using tifffile
                    threshold_array = array(threshold_images)
                    tif.imwrite("Thresh-" + filename, threshold_array)

                    progress.set(i + 1)
                    root.update()

            except AssertionError:
                showinfo(
                    title="Assertion Error",
                    message=f"Sorry, there was an error with: {filename[i]}\nPhil couldn't determine if it is a file or not.\nPlease try again.")

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.destroy()
        frame.mainloop()
        cv2.waitKey()

    # There were a few times I got a random NameError, so added this
    except NameError:
        showinfo(
            title="Error",
            message=f"Sorry, Something happened")
        exit()

    # w/o this, trackpy prints lots of information that's useless for the user, so I silenced it
    tp.quiet()

    thresholded_tifs = []
    split_list = []

    # This allows for saving multiple sheets to the same excel file
    book = op.Workbook()
    book.remove(book.active)
    writer = pd.ExcelWriter(
        f'Analyzed_Data-{dir_name}.xlsx', engine='openpyxl')
    writer.book = book

    # For full object data option (multiple excel sheets)
    if full_obj_data == True:
        book1 = op.Workbook()
        book1.remove(book1.active)
        writer1 = pd.ExcelWriter(
            f'Full Object Data-{dir_name}.xlsx', engine='openpyxl')
        writer1.book1 = book1

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


# Tracking the objects & saving to excel sheet (does i .tif videos at a time, specified by sheet_size)

    for j in range(0, len(split_list)):

        # Defining Variables
        full_obj_df = pd.DataFrame()
        final_df = pd.DataFrame()

        for i in range(0, len(split_list[j])):

            progress.set(progress.get() + 1)
            root.update()

            # Specifing which movie the data came from
            filename = os.path.basename(split_list[j][i])
            file_num = int(filename[-6:-4])

            obj_size_list = []

            frames = tif.imread(f'{split_list[j][i]}')

            # tracking the objects & collecting obj information like position, size, brightness, ect.
            f = tp.batch(frames[:], object_diameter, invert=True,
                         engine=trk_algo, processes='auto')

            # Linking the objects / tracking their paths (msd == mean square displacement)
            linked_obj = tp.link_df(f, search_range, memory=trk_memory)
            squared_motion = tp.motion.imsd(linked_obj, pixel_size, fps)

            msd_df = squared_motion.transpose()
            msd_df.insert(
                0, "File", file_num, allow_duplicates=True)

            # Full object data option where all variables are saved (object x and y for each frame & object, lots of data!)
            if full_obj_data == True:
                df2 = linked_obj.sort_values(by=['particle', 'frame'])
                df2.insert(0, "File", file_num, allow_duplicates=True)
                full_obj_df = pd.concat([full_obj_df, df2])

            # This section is finding the # of pixels that are in each of the object (object size)
            desired_values = linked_obj[['frame', 'particle', 'mass']]
            desired_values = desired_values.sort_values(
                by=['particle', 'frame'])
            total_objs = desired_values['particle'].iloc[-1]

            # loop to calculate mean and std for the particle size * brightness, which is converted into pixels by x/255
            for object in range(0, int(total_objs)):

                mass_df = desired_values[desired_values['particle'] == object]

                # If just one data point is available, then theres no point to tracking it, so the object is skipped
                if len(mass_df) >= 1:
                    avg_mass = (mass_df['mass'].mean())/255
                    mass_std = (mass_df['mass'].std())/255

                    # Adding the mean and stdev of the object size to list
                    temp_list = [avg_mass.round(2), mass_std.round(2)]
                    obj_size_list.append(temp_list)

                else:
                    pass

            # Joining dfs
            obj_size_df = pd.DataFrame(obj_size_list, columns=[
                'Average Obj Size', 'Std of Obj Size'])

            output_df = obj_size_df.join(msd_df)
            output_df.dropna(subset=['Std of Obj Size'], inplace=True)
            final_df = pd.concat([final_df, output_df])

        # Saving as excel (The automatic naming is based on the naming convention below)
        # Naming convention: Thresh-XXXXXXXXX-01.tif
        filename = os.path.basename(split_list[j][0])
        proper_name = filename[7:-7]

        # This is me trying to fix the issue of the excel sheet not saving properly
        # Honestly Idk what this is going to do, I need to come back to this
        # Dynamic_Variable_Name = 'Sheet'
        # globals()[Dynamic_Variable_Name] = final_df

        final_df.to_excel(writer, sheet_name=proper_name)
        writer.save()

        # Full object data option
        if full_obj_data == True:
            full_obj_df.to_excel(writer1, sheet_name=proper_name)
            writer1.save()

# Incase user clicks the red x and wants to shutdown the program.
    root.protocol("WM_DELETE_WINDOW", on_closing)

    showinfo(title="Finished",
             message=f"All Files Tracked and Saved")

# Opens folder where files were saved
    folder = os.getcwd()
    os.startfile(folder)
