import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb, filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import pygame
import os
import threading
import time

# Farben definieren
BG_COLOR = "#f0f0f0"
BTN_COLOR = "#06f5e9"

# Pygame initialisieren
pygame.mixer.init()

# Fenster
fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x700")
fenster.resizable(False, False)

# Canvas als Hintergrund
canvas = tk.Canvas(fenster, width=600, height=700, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Hintergrundbild laden und auf Canvas zeichnen
bg_image = Image.open("bar/serainfullsuit.jpg").resize((600, 700), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
canvas.bg_photo = bg_photo  # Referenz speichern!
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Info-Text
info_label = ttk.Label(
    canvas,
    text="Linksklick: Sound abspielen   |   Rechtsklick: Sound zuweisen",
    foreground="gray",
    background="#ffffff"
)
canvas.create_window(300, 30, window=info_label)

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
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)
    lautstaerke_wert_label.config(text=f"{int(float(val))} %")

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
style.configure("Custom.TCheckbutton", background=BG_COLOR)

# Sound-Buttons (zentriert)
sound_button_frame = ttk.Frame(canvas, style="BG.TFrame")
canvas.create_window(300, 100, window=sound_button_frame)
for name in text_variable:
    btn = ttk.Button(sound_button_frame, text=name, style='TButton')
    btn.pack(side='left', expand=True, padx=8, pady=8)
    btn.config(command=lambda name=name: button_sound_abspielen(name))
    btn.bind("<Button-3>", lambda event, name=name: sound_datei_zuteilen(name))
    button_list.append(btn)

# Lautstärkeregler und Wert darunter
lautstaerke_label = ttk.Label(canvas, text="Lautstärke", background=BG_COLOR)
canvas.create_window(300, 180, window=lautstaerke_label)

lautstaerke_frame = ttk.Frame(canvas, style="BG.TFrame")
canvas.create_window(300, 210, window=lautstaerke_frame)

lautstaerke_regler = ttk.Scale(
    lautstaerke_frame, from_=0, to=100, orient='horizontal',
    command=lautstaerke_setzen
)
lautstaerke_regler.set(50)
lautstaerke_regler.pack(fill='x', expand=True)

lautstaerke_wert_label = ttk.Label(canvas, text="50 %", background=BG_COLOR)
canvas.create_window(300, 240, window=lautstaerke_wert_label)

# Checkbox für Loop-Modus
loop_checkbox = ttk.Checkbutton(
    canvas, text="Loop (Sound wiederholen)", variable=loop_var, style="Custom.TCheckbutton"
)
canvas.create_window(300, 270, window=loop_checkbox)

# Button-Frame für die unteren Buttons
button_frame = ttk.Frame(canvas, style="BG.TFrame")
canvas.create_window(300, 650, window=button_frame)

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

ttk.Button(button_frame, text='Alle abspielen', command=alle_abspielen, style='TButton').pack(side='left', expand=True, padx=20)
ttk.Button(button_frame, text='Beenden', command=datei_beenden, style='TButton').pack(side='left', expand=True, padx=20)

fenster.mainloop()
