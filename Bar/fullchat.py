import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb, filedialog as fd
from tkinter.messagebox import showinfo
import pygame
import os
import threading
import time

# Farben definieren
BG_COLOR = "#f0f0f0"  # Fensterhintergrund
BTN_COLOR = "#06f5e9" # Buttonfarbe

# Pygame initialisieren
pygame.mixer.init()

# Fenster
fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")
fenster.configure(bg=BG_COLOR)  # Fensterhintergrund setzen

# Info-Text hinzufügen
info_label = ttk.Label(
    fenster,
    text="Linksklick: Sound abspielen   |   Rechtsklick: Sound zuweisen",
    foreground="gray",
    background=BG_COLOR
)
info_label.pack(pady=(8, 0))

# Globale Variablen
text_variable = ['Sound_01', 'Sound_02', 'Sound_03', 'Sound_04']
button_sounds = {"Sound_01": "example.mp3", "Sound_02": "example.mp3", "Sound_03": "example.mp3", "Sound_04": "example.mp3"}
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

# Variable für Loop-Modus
loop_var = tk.BooleanVar(value=False)

# Funktion: Sound abspielen
def button_sound_abspielen(name):
    # Wenn gerade ein Sound läuft, stoppen
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        return
    pfad = button_sounds.get(name)
    if pfad:
        try:
            pygame.mixer.music.load(pfad)
            loops = -1 if loop_var.get() else 0
            pygame.mixer.music.play(loops=loops)
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
lautstaerke_label = ttk.Label(fenster, text="Lautstärke", background=BG_COLOR)
lautstaerke_label.pack(pady=(10,0))

lautstaerke_frame = ttk.Frame(fenster, style="BG.TFrame")
lautstaerke_frame.pack(fill='x', padx=20)

lautstaerke_regler = ttk.Scale(
    lautstaerke_frame, from_=0, to=100, orient='horizontal',
    command=lautstaerke_setzen
)
lautstaerke_regler.set(50)  # Standard: 50%
lautstaerke_regler.pack(fill='x', expand=True)

# Das Label für den Wert UNTER den Regler setzen:
lautstaerke_wert_label = ttk.Label(fenster, text="50 %", background=BG_COLOR)
lautstaerke_wert_label.pack(pady=(0,10))

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
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                except Exception as e:
                    showinfo("Fehler", f"Konnte Sound nicht abspielen:\n{e}")
    threading.Thread(target=play_all, daemon=True).start()

def sound_cancel():
    pygame.mixer.music.stop()
    showinfo("Abgebrochen", "Sound wurde gestoppt.")

# Frame für die Sound-Buttons oben
sound_button_frame = ttk.Frame(fenster, style="BG.TFrame")
sound_button_frame.pack(side='top', fill='x', pady=10)

# Style anpassen
style = ttk.Style()
style.theme_use('clam')
style.configure('TButton',
    padding=6,
    relief='flat',
    background=BTN_COLOR,
    foreground="black",
    borderwidth=0,
    focusthickness=0,
    focuscolor='none'
)
style.map('TButton', background=[('active', '#04c4d6'), ('pressed', '#02a3b0')])
style.configure("BG.TFrame", background=BG_COLOR)

# Style für Checkbutton anpassen
style.configure("Custom.TCheckbutton", background=BG_COLOR)

# Dynamische Buttons mit Linksklick (Play) und Rechtsklick (Zuweisen)
for name in text_variable:
    btn = ttk.Button(sound_button_frame, text=name, style='TButton')
    btn.pack(side='left', expand=True, padx=8, pady=8)
    btn.config(command=lambda name=name: button_sound_abspielen(name))
    btn.bind("<Button-3>", lambda event, name=name: sound_datei_zuteilen(name))
    button_list.append(btn)

# Button-Frame für die unteren Buttons
button_frame = ttk.Frame(fenster, style="BG.TFrame")
button_frame.pack(side='bottom', fill='x', pady=10)

ttk.Button(button_frame, text='Alle abspielen', command=alle_abspielen, style='TButton').pack(side='left', expand=True, padx=20)
ttk.Button(button_frame, text='Beenden', command=datei_beenden, style='TButton').pack(side='left', expand=True, padx=20)

# Checkbox für Loop-Modus
loop_checkbox = ttk.Checkbutton(
    fenster, text="Loop (Sound wiederholen)", variable=loop_var, style="Custom.TCheckbutton"
)
loop_checkbox.pack(pady=(0, 10))

# GUI starten
fenster.mainloop()
