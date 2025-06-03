import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk


def datei_oeffnen():
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

def datei_speichern():
    mb.showinfo("Speichern")


# Hauptfenster erstellen
fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")

# Menü
button_list = []
text_variable = ['sound1', 'sound2', 'sound3', 'sound4']

open_button = ttk.Button(fenster, text='Open a File', command=datei_oeffnen)
open_button.pack()

jingle1 = ttk.Button(fenster, text='Song1🎶', width=20, padding=50)
jingle1.pack(side='left')

play_button = ttk.Button(fenster, text="Play")
play_button.pack()

for word in text_variable:
    button2 = ttk.Button(text=word)
    button2.pack(side='left', expand=True)
    button_list.append(button2)


# GUI starten
fenster.mainloop()