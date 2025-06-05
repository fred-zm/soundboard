import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb, filedialog as fd
from tkinter.messagebox import showinfo
import pygame
import os

# Pygame initialisieren
pygame.mixer.init()

# Fenster
fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")

# Globale Variablen
text_variable = ['yea boy', 'bom', 'thud', 'stop']
button_sounds = {"yea boy": "C:/Users/Guts/Downloads/yeah-boy-114748.mp3", "bom": "C:/Users/Guts/Downloads/alerte-346112.mp3", "thud": "C:/Users/Guts/Downloads/thud-sound-effect-319090.mp3", "stop": "C:/Users/Guts/Downloads/touching-46084.mp3"}  # Hier speichern wir: {"sound1": "C:/Pfad/datei.mp3", ...}
button_list = []

# Funktion: Sound-Datei auswählen und zuweisen
def sound_datei_zuteilen(name):
    filetypes = (
        ('Audio Dateien', '*.mp3 *.wav'),
        ('Alle Dateien', '*.*')
    )
    filename = fd.askopenfilename(
        title=f'Sound für {name} wählen',
        initialdir='/',
        filetypes=filetypes)
    
    if filename:
        button_sounds[name] = filename
        showinfo("Zugewiesen", f"{name} spielt jetzt:\n{os.path.basename(filename)}")

# Funktion: Sound abspielen
def button_sound_abspielen(name):
    pfad = button_sounds.get(name)
    if pfad:
        try:
            pygame.mixer.music.load(pfad)
            pygame.mixer.music.play()
        except Exception as e:
            showinfo("Fehler", f"Konnte Sound nicht abspielen:\n{e}")
    else:
        showinfo("Kein Sound", f"{name} hat noch keinen Sound.")

# Beenden
def datei_beenden():
    pygame.mixer.quit()
    fenster.quit()

# Dynamische Buttons mit Linksklick (Play) und Rechtsklick (Zuweisen)
for name in text_variable:
    btn = ttk.Button(fenster, text=name)
    btn.pack(side='left', expand=True, padx=8, pady=8)

    # Linksklick → Sound abspielen
    btn.config(command=lambda name=name: button_sound_abspielen(name))

    # Rechtsklick → Sound zuweisen
    btn.bind("<Button-3>", lambda event, name=name: sound_datei_zuteilen(name))

    button_list.append(btn)

# Beenden-Button
ttk.Button(fenster, text='Beenden', command=datei_beenden).pack(pady=10)

# GUI starten
fenster.mainloop()
