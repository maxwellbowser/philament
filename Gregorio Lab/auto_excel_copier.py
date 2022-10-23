'''
Created on Jul 28, 2022

@author: panch
'''

from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import os

import numpy as np
import pandas as pd
import tkinter as tk

# This loop is here so that we can just copy all of the data over at once


def copier():
    # setting up frame and window for file browsing
    root = tk.Tk()
    root.title('All my homies hate carpal tunnel')
    root.resizable(True, False)
    root.geometry('300x150')
    browse_frame = ttk.Frame(root,  padding="5 5 10 10")
    browse_frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Browsing Dialog for the text files

    def select_files():
        try:

            filetypes = (
                ('Text Files', '*.txt'),
                ('All files', '*.*')
            )
            global filepath

            filepath = fd.askopenfilenames(
                title='Open files',
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

    # setting var name to be empty DataFrames
    final_df = pd.DataFrame()
    final_df2 = pd.DataFrame()

    first_columns = []
    second_columns = []

    # start of loop for copying data from i out of 10 files
    # (You could do more but we take 10 movies per slide)
    for i in range(0, len(filepath)):

        # This finds where the first section of data ends
        # by using numpy to just read just the first column,
        # this will prevent an error if the second section of data is longer than
        # the first

        file = np.genfromtxt(filepath[i], dtype='str', usecols=0)
        x = np.where(file == 'Bin')
        n = int(x[0])

    # reading .txt files & separating the two sections of data
        df = pd.read_csv(filepath[i], sep='\t', on_bad_lines='skip')

        df_val = df.iloc[:n - 1]

    # this is kind of a relic before I had the numpy section to separate the data,
    # but it works so I kept it
        df_length = len(df_val.index)

    # Copying over the columns that we actually use in our analysis
        desired_values = df_val[['Track ', 'Length', 'Distance',
                                 '#Frames', '1stFrame', 'time(s)', 'AvgPerim']]

        intermediate_df = desired_values.copy()

    # Since we are copying multiple files together, this puts a label for each
    # particle for which file it came from
        num = i + 1

        intermediate_df.insert(0, "File", num, allow_duplicates=True)

    # Final thing we do with the first section of data is append it a list, so
    # each loop can add on the next files data
        first_columns.append(intermediate_df)

    # Now we are copying over the data from the Histogram (second section)
        df2 = pd.read_csv(filepath[i],
                          sep='\t', skiprows=df_length + 1)

        histogram = df2.transpose()

    # This gets rid of the bin
        histogram.drop("Bin", axis=0, inplace=True)

        filter_histogram = histogram.dropna()

        second_columns.append(filter_histogram)

    # Finally, the lists are concatenated into the dataframes, the filenames are created
    # (we use the naming convention of Condition-Used-01.txt), and the df is saved as .xlsx

    final_df2 = pd.concat(second_columns)
    final_df = pd.concat(first_columns)

    filename = os.path.basename(filepath[0])

    length = len(filename)
    proper_name = filename[:length - 6]

    final_df2.to_excel(f"{proper_name}histogram_values.xlsx", 'Histogram Values',
                       header=None)

    final_df.to_excel(f"{proper_name}filament_values.xlsx",
                      'Filament Values', index=False)

    # This shows that the process finished, and opens the folder where the
    # files are saved
    showinfo(
        title="Saving that time big Dawg",
        message=f"Successfully copied and saved files")

    # Making it so the program can be run over and over again
    # without needing console commands

    x = input(
        f'\nLast copied dataset was: {proper_name[:-1]}\ntype 0 to restart program, type 1 to end it')
    try:
        n = int(x)
    except ValueError:
        print('Woah woah woah, thats not a number! Please try again')
        x = input(
            f'\nLast copied dataset was: {proper_name[:-1]}\ntype 0 to restart program, type 1 to end it')
        n = int(x)
    if n == 0:
        copier()
    else:
        print('Goodbye!')
        folder = os.getcwd()
        os.startfile(f'{folder}')
        pass


copier()

#os.system('start EXCEL.EXE filament_values.xlsx')
#os.system('start EXCEL.EXE histogram_values.xlsx')
