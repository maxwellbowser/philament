import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import pickle
import pandas as pd


if __name__ == "__main__":
    global pixel_size
    global object_diameter
    global full_flmt_data
    global sheet_size
    global trk_memory
    global search_range
    global trk_algo

    # Function for browse window
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

    # This try-except loop will check if the default values have already been made
    # If not, it sets them to my preset values and then saves a default_value file
    try:
        with open('Default_values.pickle', 'rb') as f:
            past_values = pickle.load(f)

        pixel_size = past_values[0]
        object_diameter = past_values[1]
        full_flmt_data = past_values[2]
        sheet_size = past_values[3]
        trk_memory = past_values[4]
        search_range = past_values[5]
        trk_algo = past_values[6]
        fps = past_values[7]

    except:
        pixel_size = 0.139
        object_diameter = 25
        full_flmt_data = False
        sheet_size = 10
        trk_memory = 5
        search_range = 35
        trk_algo = 'numba'
        fps = 5

        # This is the order that the values are saved
        Default_values = [pixel_size, object_diameter, full_flmt_data,
                          sheet_size, trk_memory, search_range, trk_algo, fps]

        with open('Default_values.pickle', 'wb') as f:
            pickle.dump(Default_values, f)

    # Setting up root & frames for the starting GUI
    root = tk.Tk()
    root.title('Welcome to Philament Tracker!')
    root.geometry('550x300')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # root.resizable(False, False)

    button_frame = ttk.Frame(root,  padding="5 5 10 10")
    button_frame.grid(column=0, row=1)

    values_frame = ttk.Frame(root,  padding="5 5 10 10", takefocus=True)
    values_frame.grid(column=0, row=0)

    options_frame = ttk.Frame(root,  padding="5 5 10 10")
    options_frame.grid(column=1, row=0)

    # Variables being made
    tk_full_flmt_data = tk.BooleanVar(value=full_flmt_data)
    tk_pixel_size = tk.DoubleVar(value=pixel_size)
    tk_object_diameter = tk.IntVar(value=object_diameter)
    tk_sheet_size = tk.IntVar(value=sheet_size)
    tk_trk_memory = tk.IntVar(value=trk_memory)
    tk_search_range = tk.IntVar(value=search_range)
    tk_fps = tk.IntVar(value=fps)

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

    # Entries being made
    full_flmt_data = ttk.Checkbutton(options_frame, text="Include full object data? \n(Warning: Large files)",
                                     variable=full_flmt_data, onvalue=True, offvalue=False).grid(
        column=0, row=0, padx=10, pady=5, sticky='N')

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
        # exit()

    # Making RadioButtons (would've made with for loop to save space, but it caused problems, and this is more readable anyways)
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
        options_frame,
        text='Open Files',
        command=select_files
    ).grid(column=1, row=1, padx=1, pady=5)

    close_button = ttk.Button(
        options_frame,
        text='Cancel',
        command=close_window
    ).grid(column=0, row=1, padx=1, pady=5)

    root.mainloop()

    # setting regular variables equal to the tkinter variables
    try:
        pixel_size = tk_pixel_size.get()
        object_diameter = tk_object_diameter.get()
        full_flmt_data = tk_full_flmt_data.get()
        sheet_size = tk_sheet_size.get()
        trk_memory = tk_trk_memory.get()
        search_range = tk_search_range.get()
        fps = tk_fps.get()
    except:
        showinfo(title='Whoops!',
                 message='Error: Invalid Input\nPlease restart program')
        exit()
    Default_values = [pixel_size, object_diameter, full_flmt_data,
                      sheet_size, trk_memory, search_range, trk_algo]

    with open('Default_values.pickle', 'wb') as f:
        pickle.dump(Default_values, f)
