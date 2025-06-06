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
bg_image = Image.open("bar/death.jpg").resize((600, 700), Image.LANCZOS)
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

# Login-Funktion
def show_login():
    login_win = tk.Toplevel()
    login_win.title("Login")
    login_win.geometry("300x150")
    login_win.resizable(False, False)
    login_win.grab_set()  # Fokus auf Login

    # Musik beim Öffnen abspielen
    try:
        pygame.mixer.music.load("bar/funny-bgm-240795.mp3")  # Pfad zu deiner Musikdatei
        pygame.mixer.music.play(-1)  # -1 = Endlosschleife


    except Exception as e:
        print(f"Login-Musik konnte nicht geladen werden: {e}")
    
    # Benutzername
    ttk.Label(login_win, text="Benutzername:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    username_entry = ttk.Entry(login_win)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    # Passwort
    ttk.Label(login_win, text="Passwort:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    password_entry = ttk.Entry(login_win, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Login-Logik
    def check_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "1234":
            pygame.mixer.music.stop()  # Musik stoppen nach Login
            login_win.destroy()
            fenster.deiconify()  # Hauptfenster anzeigen
        else:
            try:
                pygame.mixer.music.load("bar/Mario.mp3")  # Fehler-Sound
                pygame.mixer.music.play()
                def play_login_musik():
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    try:
                        pygame.mixer.music.load("bar/funny-bgm-240795.mp3")  # Zurück zur Login-Musik
                        pygame.mixer.music.play(-1)    
                    except Exception as e:
                        print(f"Fehler beim Abspielen des Fehler-Sounds: {e}")
                threading.Thread(target=play_login_musik, daemon=True).start()
            except Exception as e:
                print(f"Fehler beim Abspielen des Login-Sounds: {e}")
            ttk.Label(login_win, text="Login fehlgeschlagen!", foreground="red").grid(row=3, column=0, columnspan=2)
            
    # Login-Button
    login_btn = ttk.Button(login_win, text="Login", command=check_login)
    login_btn.grid(row=2, column=0, columnspan=2, pady=10)

    # Hauptfenster zunächst verstecken
    fenster.withdraw()

show_login()

fenster.mainloop()
