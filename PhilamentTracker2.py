'''
Created on Aug 9, 2022

@author: panch
'''

from datetime import date
import multiprocessing
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import os

import cv2

import numpy as np
import openpyxl as op
import pandas as pd
import tifffile as tif
import tkinter as tk
import trackpy as tp
import random
from multiprocessing import freeze_support
from statistics import mean, stdev

# This program is meant to take input of prerecorded .tif videos of bright objects on a dark background
# and output thresholded .tif videos, along with an excel sheet of the mean squared displacement of each
# object for all the imported videos!

# All code and comments written by Ryan Bowser (@maxwellbowser on github, ryanbowser@arizona.edu)
# Feel free to send me an email if you have any questions!

if __name__ == '__main__':

    # This line is neccesary for proper running after being compiled with pyinstaller
    multiprocessing.freeze_support()

    print("""

    ▒▐█▒▐█▒▐█▀▀▒██░░░▒██░░░▒▐█▀▀█▌░░▒█▒█▒█ 
    ▒▐████▒▐█▀▀▒██░░░▒██░░░▒▐█▄▒█▌░░░▀░▀░▀ 
    ▒▐█▒▐█▒▐█▄▄▒██▄▄█▒██▄▄█▒▐██▄█▌░░▒▄▒▄▒▄ 
    
    Welcome to Phil 2.0!
    
    Please enter the number of files you would like per list:
    
    ** Also please take a second to make sure the folder this program is located in
    is free of all .tif files!!! **
    
    
    .▀█▀.█▄█.█▀█.█▄.█.█▄▀　█▄█.█▀█.█─█
    ─.█.─█▀█.█▀█.█.▀█.█▀▄　─█.─█▄█.█▄█

    """)

# Sheet size formatting the excel file at the end
    sheet_size = int(input())

    # Setting up window and File Browsing
    root = tk.Tk()
    root.title('File Selection')
    root.resizable(False, False)
    root.geometry('300x150')
    browse_frame = ttk.Frame(root,  padding="5 5 10 10")
    browse_frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def select_files():

        filetypes = (
            ('TIFF Files', '*.tif'),
            ('All files', '*.*')
        )
        filepath = []

        filepath = fd.askopenfilenames(
            title='Open files',
            initialdir=r'C:\Users\Desktop',
            filetypes=filetypes)

        return filepath

    filepath = select_files()

    root.destroy()

    # Gui to help user find best thresholding value for videos
    # (Picks a random chosen video to use)

    # For larger sample sizes more videos will be tested
    # Always at least 1 video, and capped at 5 if 200+ videos are being analyzed
    multiples_of_50 = len(filepath) // 50
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
            range(0, len(filepath)), num_files_for_threshold)
        thresh_values = []
    except:
        print('Please re-run program, and make sure to select files!')
        exit()

    # running the thresholding picker gui
    for i in range(0, len(rand_file_num)):

        def close():
            window.destroy()
            cv2.destroyAllWindows()

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
        window.geometry('400x250')

        thresh_check_frame = ttk.Frame(window, padding='5 5 10 10')
        thresh_check_frame.grid(column=0, row=0)
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

        checking_images = []

        loaded, checking_images = cv2.imreadmulti(
            mats=checking_images, filename=filepath[rand_file_num[i]], flags=cv2.IMREAD_GRAYSCALE)

        # Here 100 is just a default value for the thresholding
        value = tk.IntVar(thresh_check_frame, 100)

        # Widgets! I chose not to show threshold value to eliminate human bias
        # So you can't say "eh i'll just go to threshold value N everytime"

        slider = ttk.Scale(thresh_check_frame, from_=0, to=255, orient='horizontal',
                           variable=value, command=double_check, length=200).grid(column=0, row=1)

        cont_but = ttk.Button(thresh_check_frame, text='Continue', command=close).grid(
            column=1, row=1, padx=10, pady=5)

        old_thresh_label = ttk.Label(thresh_check_frame, text='Determining Thresholding Value:',
                                     font=('Arial', 12)).grid(column=0, row=0, padx=20, pady=10)

        double_check(0)
        thresh_check_frame.mainloop()
        thresh_values.append(value.get())

    # setting the thresholding value to be used when thresholding
    threshold_value = int(mean(thresh_values))

    # Progress bar design
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

    # Start of the actual program, and the thresholding and saving of files
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

                    blur = cv2.medianBlur(original_images[x], 5)

                    ret, image = cv2.threshold(
                        blur, threshold_value, 255, cv2.THRESH_BINARY_INV)

                    '''
                    If I was using np arrays, i wouldn't be able to append each browse_frame to the
                    list. This is because when you append matrices to np arrays, they are
                    appended to a COPY of the array, not the original array. Because I
                    chose to use a for loop, using np arrays didn't fit or make sense.
        
                    (Sorry for the long comment, but I figure its better to have these
                    in case someone needs to understand what i'm doing)
                    '''

                    threshold_images.append(image)

                    # Saving thresholded tiff images using tifffile
                    threshold_array = np.array(threshold_images)
                    tif.imwrite("Thresh-" + filename, threshold_array)

                    progress.set(i + 1)
                    root.update()

            except AssertionError:
                showinfo(
                    title="Assertion Error",
                    message=f"Sorry, there was an error with: {filename[i]}\nPhil couldn't determine if it is a file or not.\nPlease try again.")

        root.destroy()
        frame.mainloop()
        cv2.waitKey()

    except NameError:
        showinfo(
            title="Error",
            message=f"Sorry, Something happened")
        pass

    # By finding all filepaths that end in .tif in the working directory (where the thresholded videos are saved)
    # This function is able to automatically find the filepaths for the newly thresholded videos

    # Some things are commented out, because I'm not using those data but i want to be able to enable it
    # for other people eventually

    tp.quiet()

    # Defining Variables
    thresholded_tifs = []
    split_list = []
    flmnt_data = pd.DataFrame()
    msd_data = pd.DataFrame()
    # df2 = pd.DataFrame()

    # column_one = []
    column_two = []

    # This allows for saving multiple sheets to the same excel file w/o overwriting
    book = op.Workbook()
    book.remove(book.active)
    todays_date = date.today()
    writer = pd.ExcelWriter(
        f'Analyzed_Data-{todays_date}.xlsx', engine='openpyxl')
    writer.book = book

    for x in os.listdir():
        if x.endswith('.tif'):
            thresholded_tifs.append(x)

    # Breaking the list into nested lists, that will separate different samples
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


# Tracking the filaments & saving to excel sheet (does n .tif videos at a time, specified by sheet_size)

    for j in range(0, len(split_list)):

        for i in range(0, len(split_list[j])):

            progress.set(progress.get() + 1)
            root.update()

            frames = tif.imread(f'{split_list[j][i]}')

            # tracking the objects
            f = tp.batch(frames[:], 25, invert=True,
                         engine='numba', processes='auto')

            t = tp.link_df(f, 35, memory=5)

            squared_motion = tp.motion.imsd(t, 0.139, 5)

            filename = os.path.basename(split_list[j][i])

            # to specify which movie the data came from
            file_num = int(filename[-6:-4])
            # The comments below are to insert the columns for x, y, particle,
            # ect...

            # desired_values = t[['frame', 'particle',
            #                    'x', 'y', 'mass', 'size']]

            # df2 = desired_values.sort_values(by=['particle', 'frame'])

            # df2.insert(0, "File", file_num, allow_duplicates=True)
            # puts in an empty column
            # df2[''] = ''

            transposed_msd = squared_motion.transpose()

            transposed_msd.insert(
                0, "File", file_num, allow_duplicates=True)

            # column_one.append(df2)

            column_two.append(transposed_msd)

            #paths = tp.plot_traj(t, mpp=0.139, label=True, block=False)
            # paths.figure.savefig(f'{file_num}.png')

        # flmnt_data = pd.concat(column_one)
        msd_data = pd.concat(column_two)
        # file_data = pd.concat(column_one)

        filename = os.path.basename(split_list[j][0])

        proper_name = filename[7:-7]

        msd_data.to_excel(writer, sheet_name=proper_name)
        # file_data.to_excel(writer, sheet_name=proper_name)

        msd_data = []
        column_two = []
        writer.save()

    showinfo(title="Finished",
             message=f"All Files Tracked and Saved")

# Opens folder where files were saved
    folder = os.getcwd()
    os.startfile(folder)
