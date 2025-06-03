import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


def datei_oeffnen():
    messagebox.showinfo('Viel Spaß jetzt öffnen.')
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
    messagebox.showinfo('Speichern')

def datei_beenden():
    fenster.quit()

# Hauptfenster erstellen

fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")


#button herstellen
button_open = tk.Button(text="Play")
button_end = tk.Button(text='Beenden', command=datei_beenden)
open_button = ttk.Button(
    fenster,
    text='Open a File',
    command=datei_oeffnen
)
#menü


open_button.pack()
button_open.pack()
button_end.pack()

# GUI starten
fenster.mainloop()