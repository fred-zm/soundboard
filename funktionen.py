import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo




#zeigt nur denn pfad der datei die konvention ist irreführend
def datei_oeffnen():
    mb.showinfo("Öffnen")
    filetypes = (
        ('text files', '*.txt'),
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
#noch ungenutzt
def datei_speichern():
    mb.showinfo("Speichern")

#beendet das Programm 
def datei_beenden(fenster: tk.Tk):
    fenster.quit()