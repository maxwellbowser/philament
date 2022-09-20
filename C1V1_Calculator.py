'''
Created on Jul 1, 2022

@author: panch
'''

from tkinter import *
from tkinter import ttk
from  ttkthemes import ThemedStyle


def calculate(*args):
    # the try/except loops are needed since the entry fields are empty when
    # the program opens
    try:
        # varibles are made into floats, and calculations/names are set
        variable_c1 = float(c1.get())
        variable_v1 = float(v1.get())
        variable_c2 = float(c2.get())
        variable_v2 = float(v2.get())
        if variable_c1 == 0:
            name.set("C1")
            C1 = ((variable_c2 * variable_v2) / variable_v1)
            output.set(round(C1, 3))
        if variable_v1 == 0:
            name.set("V1")
            V1 = ((variable_c2 * variable_v2) / variable_c1)
            output.set(round(V1, 3))
        if variable_c2 == 0:
            name.set("C2")
            C2 = ((variable_c1 * variable_v1) / variable_v2)
            output.set(round(C2, 3))
        if variable_v2 == 0:
            name.set("V2")
            V2 = ((variable_c1 * variable_v1) / variable_c2)
            output.set(round(V2, 3))
        else:
            pass
    except:
        pass


# This is where all the UI stuff starts
root = Tk()

root.title("Concentration Calculator")
root.resizable(False, False)
root.geometry("470x200")

style =ThemedStyle(root)
style.set_theme('equilux')
    
# I stole this part from the tkinter website
mainframe = ttk.Frame(root, padding="5 5 10 10")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# top row labels, I used x as a spacer between variable_v1 and variable_c2
c1_label = ttk.Label(mainframe, text="C1", font=(
    "Times New Roman", 15)).grid(column=1, row=1, padx=20, pady=5)

v1_label = ttk.Label(mainframe, text="V1", font=(
    "Times New Roman", 15)).grid(column=2, row=1, padx=20, pady=5)

x = ttk.Label(mainframe, text="=").grid(column=3, row=1, padx=10)

c2_label = ttk.Label(mainframe, text="C2", font=(
    "Times New Roman", 15)).grid(column=4, row=1, padx=20, pady=5)

v2_label = ttk.Label(mainframe, text="V2", font=(
    "Times New Roman", 15)).grid(column=5, row=1, padx=20, pady=5)

# Here are the entry widgets and the equals sign
c1 = StringVar()
c1_entry = ttk.Entry(mainframe, textvariable=c1, font=(
    "Times New Roman", 15), width=5).grid(column=1, row=2, padx=20, pady=5)

v1 = StringVar()
v1_entry = ttk.Entry(mainframe, textvariable=v1, font=(
    "Times New Roman", 15), width=5).grid(column=2, row=2, padx=20, pady=5)

x = ttk.Label(mainframe, text="=", font=(
    "Times New Roman", 15)).grid(column=3, row=2, padx=10)

c2 = StringVar()
c2_entry = ttk.Entry(mainframe, textvariable=c2, font=(
    "Times New Roman", 15), width=5).grid(column=4, row=2, padx=20, pady=5)

v2 = StringVar()
v2_entry = ttk.Entry(mainframe, textvariable=v2, font=(
    "Times New Roman", 15), width=5).grid(column=5, row=2, padx=20, pady=5)

# 4th row stuff, calculate button and output stuff
ttk.Button(mainframe, text="Calculate", command=calculate
           ).grid(column=5, row=3, pady=5)

name = StringVar()
which_varible = ttk.Label(mainframe, textvariable=name, font=(
    "Times New Roman", 15)).grid(column=2, row=4, padx=0, pady=5)

connecting_label = ttk.Label(mainframe, text="is", font=(
    "Times New Roman", 15)).grid(column=3, row=4, padx=5, pady=5)

output = StringVar()
concentration_output = ttk.Label(mainframe, textvariable=output, font=(
    "Times New Roman", 15)).grid(column=4, row=4, padx=0, pady=5)

root.bind('<Return>', calculate)

mainframe.mainloop()
