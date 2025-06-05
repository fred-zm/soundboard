import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb, filedialog as fd
from tkinter.messagebox import showinfo
import pygame
import os
import threading
import time

# Pygame initialisieren
pygame.mixer.init()

# Fenster
fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")

# Globale Variablen
text_variable = ['Name1', 'Name2', 'Name3', 'Name4']
button_sounds = {"Name1": "example.mp3", "Name2": "example.mp3", "Name3": "example.mp3", "Name4": "example.mp3"}  # Hier speichern wir: {"sound1": "C:/Pfad/datei.mp3", ...}
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


# Lautstärke-Callback
def lautstaerke_setzen(val):
    volume = float(val) / 100  # Wert von 0.0 bis 1.0
    pygame.mixer.music.set_volume(volume)
    lautstaerke_wert_label.config(text=f"{int(float(val))} %")

# Lautstärkeregler hinzufügen
lautstaerke_label = ttk.Label(fenster, text="Lautstärke")
lautstaerke_label.pack(pady=(10,0))

lautstaerke_frame = ttk.Frame(fenster)
lautstaerke_frame.pack(fill='x', padx=20)

lautstaerke_regler = ttk.Scale(
    lautstaerke_frame, from_=0, to=100, orient='horizontal',
    command=lautstaerke_setzen
)
lautstaerke_regler.set(50)  # Standard: 50%
lautstaerke_regler.pack(side='left', fill='x', expand=True)

lautstaerke_wert_label = ttk.Label(lautstaerke_frame, text="50 %")
lautstaerke_wert_label.pack(side='left', padx=(10,0), expand=True)

# Beenden
def datei_beenden():
    pygame.mixer.quit()
    fenster.quit()

def alle_abspielen():
    def play_all():
        for name in text_variable:
            pfad = button_sounds.get(name)
            if pfad:
                try:
                    pygame.mixer.music.load(pfad)
                    pygame.mixer.music.play()
                    # Warten bis der aktuelle Sound fertig ist
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                except Exception as e:
                    showinfo("Fehler", f"Konnte Sound nicht abspielen:\n{e}")
    threading.Thread(target=play_all, daemon=True).start()

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
ttk.Button(fenster, text='Alle abspielen', command=alle_abspielen).pack(pady=10)
ttk.Button(fenster, text='Beenden', command=datei_beenden).pack(pady=10)

# GUI starten
fenster.mainloop()
