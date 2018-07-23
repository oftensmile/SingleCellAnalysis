import tkinter.filedialog
import tkinter


def get_file(title="Chose a File"):
    root = tkinter.Tk()
    fname = tkinter.filedialog.askopenfilename(title=title)
    root.destroy()
    return fname

