'''
Created on Aug 17, 2022

@author: panch
'''

from datetime import date
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import os

from PIL import Image
import cv2

import matplotlib.pyplot as plt
import numpy as np
import openpyxl as op
import pandas as pd
import tifffile as tif
import tkinter as tk
import trackpy as tp


if __name__ == '__main__':
    sheet_size = int(input('please type number of files per sheet!'))

    tp.quiet()

    # Detecting the saved & thresholded images in directory, and getting
    # filepaths into a list

    thresholded_tifs = []
    split_list = []

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

    split_list = [thresholded_tifs[i:i + sheet_size]
                  for i in range(0, len(thresholded_tifs), sheet_size)]

    # Breaking the list into  groupings

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

    for j in range(0, len(split_list)):

        for i in range(0, len(split_list[j])):

            progress.set(progress.get() + 1)
            root.update()

            # opening file
            frames = tif.imread(f'{split_list[j][i]}')

            # tracking the objects
            f = tp.batch(frames[:], 25, invert=True,
                         engine='numba', processes='auto')

            t = tp.link(f, 50, memory=5)

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

            column_one.append(df2)

            column_two.append(transposed_msd)
            # paths = tp.plot_traj(t, mpp=0.139, label=True, block=False)
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
    folder = os.getcwd()
    os.startfile(folder)
