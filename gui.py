from cgitb import text
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import pickle
from ttkthemes import ThemedStyle
import pandas as pd


if __name__ == "__main__":
    global pixel_size
    global min_size_trk
    global full_flmt_data
    global sheet_size
    global trk_memory
    global search_range
    global trk_algo

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

    try:
        with open('Default_values.pickle', 'rb') as f:
            past_values = pickle.load(f)

        pixel_size = past_values[0]
        min_size_trk = past_values[1]
        full_flmt_data = past_values[2]
        sheet_size = past_values[3]
        trk_memory = past_values[4]
        search_range = past_values[5]
        trk_algo = past_values[6]

    except:
        pixel_size = 0.139
        min_size_trk = 25
        full_flmt_data = False
        sheet_size = 10
        trk_memory = 5
        search_range = 35
        trk_algo = 'numba'

        # This is the order that the wanted values are saved
        Default_values = [pixel_size, min_size_trk, full_flmt_data,
                          sheet_size, trk_memory, search_range, trk_algo]

        with open('Default_values.pickle', 'wb') as f:
            pickle.dump(Default_values, f)

    tkinter_theme = 'equilux'

    root = tk.Tk()
    root.title('Welcome to Philament Tracker!')
    root.geometry('550x600')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.minsize(500, 300)
    # root.configure(background = 'grey14')

    button_frame = ttk.Frame(root,  padding="5 5 10 10")
    button_frame.grid(column=0, row=1)

    values_frame = ttk.Frame(root,  padding="5 5 10 10")
    values_frame.grid(column=0, row=0)

    options_frame = ttk.Frame(root,  padding="5 5 10 10")
    options_frame.grid(column=1, row=0)

    #style =ThemedStyle(root)
    # style.set_theme('equilux')
    ffdv = True

    # Variables being made
    # stands for full filament data variable
    ffdv = tk.BooleanVar(value=full_flmt_data)

    # Labels being made
    ttk.Label(values_frame, text="Pixel size:").grid(
        column=0, row=0, padx=5, pady=5)
    ttk.Label(values_frame, text="Min object size:").grid(
        column=0, row=1, padx=5, pady=5)
    ttk.Label(values_frame, text="# of Files per condition:\n (Excel Sheet Size)").grid(
        column=0, row=2, padx=5, pady=5)
    ttk.Label(values_frame, text="Object tracking memory:").grid(
        column=0, row=3, padx=5, pady=5)
    ttk.Label(values_frame, text="Search radius:").grid(
        column=0, row=4, padx=5, pady=5)
    ttk.Label(values_frame, text="Path linking strategy:").grid(
        column=0, row=5, padx=5, pady=5)

    # Entries being made
    full_flmt_data = ttk.Checkbutton(options_frame, text="Include full object data? \n(Warning: Large files)",
                                     variable=ffdv, onvalue=True, offvalue=False).grid(
        column=0, row=0, padx=5, pady=5)

    ttk.Entry(values_frame, textvariable=pixel_size).grid(
        column=1, row=0, padx=5, pady=5)
    ttk.Entry(values_frame, textvariable=min_size_trk).grid(
        column=1, row=1, padx=5, pady=5)
    ttk.Entry(values_frame, textvariable=sheet_size).grid(
        column=1, row=2, padx=5, pady=5)
    ttk.Entry(values_frame, textvariable=trk_memory).grid(
        column=1, row=3, padx=5, pady=5)
    ttk.Entry(values_frame, textvariable=search_range).grid(
        column=1, row=4, padx=5, pady=5)
    menubut = ttk.Menubutton(values_frame, text='Select One')
    menubut.grid(column=1, row=5, padx=5, pady=5)

    file = tk.Menu(menubut, tearoff=0)
    menubut["menu"] = file

    # Making RadioButtons
    def set_value(x):
        trk_algo = x

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

    open_button = ttk.Button(
        options_frame,
        text='Open Files',
        command=select_files
    ).grid(column=0, row=1, padx=5, pady=5)

    open_button = ttk.Button(
        options_frame,
        text='Cancel',
        command=select_files
    ).grid(column=0, row=1, padx=5, pady=5)

    root.mainloop()
    root.destroy()
