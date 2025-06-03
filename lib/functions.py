from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

def open_file():
    filetypes = (
        ('mp3', '*.mp3'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )

def save_file():
    mb.showinfo("Save")

def close_window(window_object):
    window_object.quit()