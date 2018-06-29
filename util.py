import tkinter.filedialog
import tkinter


def get_file():
    root = tkinter.Tk()
    # default_dir = r"C:\Users\"  # default dir
    fname = tkinter.filedialog.askopenfilename(title=u"Chose a File")
    root.destroy()
    return fname

