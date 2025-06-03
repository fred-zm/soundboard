import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter import ttk

import pygame

class Sound_button:
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.widget = None

sound_buttons = []


def datei_hinzufuegen():
    filetypes = (
        ('MP3', '*.mp3'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='Downloads',
        filetypes=filetypes
    )

    if not filename:
        return
    
    button_name = sd.askstring(
        'Input', 
        'Sound Name:'
    )
    
    sound_button = Sound_button(path=filename, name=button_name)
    sound_buttons.append(sound_button)

    mb.showinfo(
        title='Selected File',
        message=filename
    )

    refresh_buttons()


def datei_speichern():
    mb.showinfo("Speichern")


def play(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()


def refresh_buttons():
    for button in sound_buttons:
        if button.widget:
            button.widget.destroy()

        button.widget = ttk.Button(
            sound_button_frm, 
            text=button.name,
            command=lambda: play(button.path)
        )
        button.widget.pack(side='top', fill='x', pady=5, padx=5)



# Hauptfenster erstellen
fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")

sound_button_frm = ttk.Frame(fenster)
sound_button_frm.pack(side='right', fill='both', expand=True, pady=10, padx=10)
control_frm = ttk.Frame(fenster)
control_frm.pack(side='left', fill='both', expand=True, pady=10, padx=10)

pygame.mixer.init()


# Menü
hinzufuegen_button = ttk.Button(control_frm, text='Open a File', command=datei_hinzufuegen)
hinzufuegen_button.pack()

# GUI starten
fenster.mainloop()

pygame.mixer.quit()