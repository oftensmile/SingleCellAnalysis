#!/usr/bin/env python
import tkinter
import tkinter.filedialog
from tkinter import simpledialog

__author__ = "Razin Shaikh and Minjie Lyu"
__credits__ = ["Razin Shaikh", "Minjie Lyu", "Vladimir Brusic"]
__version__ = "1.0"
__status__ = "Prototype"

def get_file(title="Chose a File"):
    root = tkinter.Tk()
    root.withdraw()
    fname = tkinter.filedialog.askopenfilename(title=title)
    root.destroy()
    return fname

def prompt_integer(title, prompt):
    root = tkinter.Tk()
    root.withdraw()
    number = simpledialog.askinteger(title, prompt)
    root.destroy()
    return number
