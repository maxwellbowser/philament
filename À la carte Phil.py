'''
Created on Aug 3, 2022

@author: panch
'''

from datetime import date
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


if __name__ == '__main__':

    threshold_value = 100

    root = tk.Tk()
    root.title('File Selection')
    root.resizable(False, False)
    root.geometry('300x150')
    browse_frame = ttk.Frame(root,  padding="5 5 10 10")
    browse_frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def select_files():
        try:

            filetypes = (
                ('TIFF Files', '*.tif'),
                ('All files', '*.*')
            )
            global filepath

            filepath = fd.askopenfilenames(
                title='Open files',
                initialdir=r'C:\Users\panch\Dropbox\Desktop',
                filetypes=filetypes)
            root.destroy()
            pass
        except:
            pass

    open_button = ttk.Button(
        browse_frame,
        text='Open Files',
        command=select_files
    )

    open_button.pack(expand=True)

    browse_frame.mainloop()
    rand_file_num = random.randint(0, len(filepath))


    window = tk.Tk()
    window.title('Checking Thresholding Value')
    window.resizable(False, False)
    window.geometry('400x250')

    thresh_check_frame = ttk.Frame(window, padding='5 5 10 10')
    thresh_check_frame.grid(column=0, row=0)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    checking_images = []
    try:

        loaded, checking_images = cv2.imreadmulti(
            mats=checking_images, filename = filepath[rand_file_num], flags=cv2.IMREAD_GRAYSCALE)

        value = tk.StringVar(thresh_check_frame, threshold_value)

        oldThreshold = tk.StringVar()

        def double_check():

            threshold_value = int(value.get())

            blur = cv2.medianBlur(checking_images[0], 5)

            ret, thresholded_checked = cv2.threshold(
                blur, threshold_value, 255, cv2.THRESH_BINARY_INV)

            cv2.imshow('Thresholded Image', thresholded_checked)
            cv2.imshow('Original Image', checking_images[0])

            oldThreshold.set(value.get())

            cv2.waitKey(5)

        def close():
            window.destroy()
            cv2.destroyAllWindows()
        
        double_check()

    # This is designing/setting up the window for choosing the thresholding
    # value
        old_thresh_value = ttk.Label(thresh_check_frame, textvariable=oldThreshold).grid(
            column=1, row=1, padx=20, pady=5)

        new_thresh_entry = ttk.Entry(thresh_check_frame, textvariable=value, ).grid(
            column=0, row=1, padx=20, pady=5)

        cont_but = ttk.Button(thresh_check_frame, text='Continue', command=close).grid(
            column=1, row=2, padx=20, pady=5)

        retry_but = ttk.Button(thresh_check_frame, text='Retry', command=double_check
                            ).grid(column=0, row=2, padx=20, pady=5)

        new_thresh_label = ttk.Label(thresh_check_frame, text='Old T Value').grid(
            column=1, row=0, padx=20, pady=5)

        old_thresh_label = ttk.Label(thresh_check_frame, text='New T Value').grid(
            column=0, row=0, padx=20, pady=5)

        thresh_check_frame.mainloop()

    # setting the thresholding value to be used when thresholding
        threshold_value = int(value.get())


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


        # I'm using lists instead of numpy (np) arrays because of how I chose to
        # collect and save the thresholded frames
        try:

            for i in range(0, len(filepath)):
                assert os.path.isfile(filepath[i])
                try:
                    original_images = []

                    loaded, original_images = cv2.imreadmulti(
                        mats=original_images, filename=f"{filepath[i]}", flags=cv2.IMREAD_GRAYSCALE)

                    threshold = []

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

                        threshold.append(image)

                        # Saving thresholded tiff images using tifffile
                        threshold_array = np.array(threshold)
                        tif.imwrite("Thresh-" + filename, threshold_array)

                        progress.set(i + 1)
                        root.update()

                    # since indexes start at zero, i made this variable for the
                    # message
                    num_of_files = i + 1

                except AssertionError:
                    showinfo(
                        title="Assertion Error",
                        message=f"Sorry, there was an error with file number: {i}\nPhil couldn't determine item {i} was a file or not")

            root.destroy()
            frame.mainloop()
            cv2.waitKey()

        except NameError:
            showinfo(
                title="Error",
                message=f"Sorry, Something happened")
            pass
    except(IndexError):
        showinfo(title="Phil2 Closing...", message="Goodbye!")

        
    tp.quiet()

    # Detecting the saved & thresholded images in directory, and getting
    # filepaths into a list

    thresholded_tifs = []
    thresholded_tifs = []

    flmnt_data = pd.DataFrame()
    msd_data = pd.DataFrame()
    df2 = pd.DataFrame()

    column_one = []
    column_two = []

    book = op.Workbook()
    book.remove(book.active)
    todays_date = date.today()

    writer = pd.ExcelWriter(
        f'Analyzed_Data-{todays_date}.xlsx', engine='openpyxl')
    writer.book = book

    for x in os.listdir():
        if x.endswith('.tif'):
            thresholded_tifs.append(x)
    
    # Progress bar from above
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

# Tracking the filaments & saving to excel sheet

    for i in range(0, len(thresholded_tifs[i])):

        progress.set(progress.get() + 1)
        root.update()

        frames = tif.imread(f'{thresholded_tifs[i]}')

        # tracking the objects
        f = tp.batch(frames[:], 25, invert=True,
                        engine='numba', processes='auto')

        t = tp.link_df(f, 35, memory=5)

        squared_motion = tp.motion.imsd(t, 0.139, 5)

        filename = os.path.basename(thresholded_tifs[i])

        # to specify which movie the data came from
        file_num = int(filename[-6:-4])

        # The comments below are to insert the columns for x, y, particle,
        # ect...

        desired_values = t[['frame', 'particle',
                        'x', 'y', 'mass', 'size']]

        df2 = desired_values.sort_values(by=['particle', 'frame'])

        df2.insert(0, "File", file_num, allow_duplicates=True)
        #puts in an empty column
        # df2[''] = ''

        transposed_msd = squared_motion.transpose()

        transposed_msd.insert(
            0, "File", file_num, allow_duplicates=True)

        column_one.append(df2)

        column_two.append(transposed_msd)

        paths = tp.plot_traj(t, mpp=0.139, label=True, block=False)
        paths.figure.savefig(f'{file_num}.png')

        flmnt_data = pd.concat(column_one)
        msd_data = pd.concat(column_two)
        # file_data = pd.concat(column_one)

        filename = os.path.basename(thresholded_tifs[0])

        proper_name = filename[7:-7]

        msd_data.to_excel(writer, sheet_name=proper_name)
        flmnt_data.to_excel(writer, sheet_name=proper_name)

        msd_data = []
        column_two = []
        writer.save()

    showinfo(title="Finished",
            message=f"All Files Tracked and Saved")
    folder = os.getcwd()
    os.startfile(folder)
