import tkinter.filedialog
from tkinter import simpledialog
import tkinter


def get_file(title="Chose a File"):
    root = tkinter.Tk()
    fname = tkinter.filedialog.askopenfilename(title=title)
    root.destroy()
    return fname

def prompt_integer(title, prompt):
    root = tkinter.Tk()
    number = simpledialog.askinteger(title, prompt)
    root.destroy()
    return number