import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import pickle
from  ttkthemes import ThemedStyle
import pandas as pd

if __name__ == "__main__":

    

    try:
        with open('Default_values.pkl', 'rb') as f:
           past_values = pickle.load(f)
           
        pixel_size = past_values[0]
        min_size_trk = past_values[1]
        msd_data = past_values[2]
        indv_data = past_values[3]
        sheet_size = past_values[4]
        trk_memory = past_values[5]
        search_range = past_values[6]
        trk_algo = past_values[7]

    except:     
        pixel_size = 0.139
        min_size_trk = 0
        msd_data = True
        indv_data = False
        sheet_size = 10
        trk_memory = 5 
        search_range = 35
        trk_algo = 'numba'

        # This is the order that the wanted values are saved
        Default_values = [pixel_size,min_size_trk,msd_data,indv_data,sheet_size,trk_memory,search_range,trk_algo]

        with open('Default_values.pkl', 'wb') as f:
            pickle.dump(Default_values, f)

    Label_font = 'Times New Roman'
    font_size = 15
    tkinter_theme = 'equilux'
   
    root = tk.Tk()
    root.title('Welcome to Philament Tracker!')
    root.geometry('350x600')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.configure(background = 'grey14')

    button_frame = ttk.Frame(root,  padding="5 5 10 10")
    button_frame.grid(column=0, row=1)
    
    values_frame = ttk.Frame(root,  padding="5 5 10 10")
    values_frame.grid(column=0, row=0)

    options_frame = ttk.Frame(root,  padding="5 5 10 10")
    options_frame.grid(column=1, row=0)

    
    style =ThemedStyle(root)
    style.set_theme('equilux')
    

    ttk.Label(values_frame, text="Pixel size:", font=(
    Label_font, font_size)).grid(column=0, row=0, padx=5, pady=5)
    ttk.Label(values_frame, text="Min object size:", font=(
    Label_font, font_size)).grid(column=0, row=1, padx=5, pady=5)
    ttk.Label(values_frame, text="# of Files per condition:\n (Excel Sheet Size)", font=(
    Label_font, font_size)).grid(column=0, row=2, padx=5, pady=5)
    ttk.Label(values_frame, text="Object tracking memory:", font=(
    Label_font,font_size)).grid(column=0, row=3, padx=5, pady=5)
    ttk.Label(values_frame, text="Search radius:", font=(
    Label_font, font_size)).grid(column=0, row=4, padx=5, pady=5)
    ttk.Label(values_frame, text="Path linking strategy:", font=(
    Label_font, font_size)).grid(column=0, row=5, padx=5, pady=5)

'''
    ttk.Entry(values_frame, intvariable=pixel_size, font=(
    Label_font, font_size)).grid(column=1, row=0, padx=5, pady=5)
    ttk.Entry(values_frame, intvariable=min_size_trk, font=(
    Label_font, font_size)).grid(column=1, row=1, padx=5, pady=5)
    ttk.Entry(values_frame, intvariable=sheet_size, font=(
    Label_font, font_size)).grid(column=1, row=2, padx=5, pady=5)
    ttk.Entry(values_frame, intvariable=trk_memory, font=(
    Label_font,font_size)).grid(column=1, row=3, padx=5, pady=5)
    ttk.Entry(values_frame, intvariable=search_range, font=(
    Label_font, font_size)).grid(column=1, row=4, padx=5, pady=5)
    ttk.Menubutton(values_frame, intvariable=trk_algo, font=(
    Label_font, font_size)).grid(column=1, row=5, padx=5, pady=5)
'''
    



    
root.mainloop()

    