# Notwendige Importe
import os                                   # Betriebssystemfunktionen (z. B. Dateiname ohne Pfad)
import json                                 # Zum Speichern/Laden der Soundpfade als JSON
import pygame                               # Zum Abspielen von Sounddateien
import tkinter as tk                        # Standard-Tkinter für GUI
from tkinter import filedialog as fd        # Für Datei-Auswahl-Dialog
from tkinter.messagebox import showinfo     # Für Info-Popups
from tkinter import ttk                     # Erweiterte Widgets (z. B. schönere Buttons)

# Pfad für gespeicherte Soundliste
SOUND_JSON_PATH = "sounds.json"         # Der Pfad zur Datei, in der die Liste der hinzugefügten Sounds gespeichert wird

# Pygame Mixer initialisieren
pygame.mixer.init()         # Startet das Soundmodul von Pygame, damit wir Sounds abspielen können

# Hauptfenster
window = tk.Tk()                                    #
window.title("Soundboard Zukunftsmotor K17")        # Erstellt das Hauptfenster für das Soundboard mit festgelegter Größe und Titel
window.geometry("1200x800")                         #

# Frames für platzierung der Buttons
top_frame = ttk.Frame(window)                               #
top_frame.pack(side='top', padx=5, pady=0)                  #
                                                            #
bottom_frame = ttk.Frame(window)                            #
bottom_frame.pack(side='bottom', padx=5, pady=10)           #
                                                            # Erzeugt 4 Bereiche (Frames), um GUI-Elemente übersichtlich zu positionieren (oben, unten, links, rechts)
left_frame = ttk.Frame(window)                              #
left_frame.pack(side='left', padx=2, pady=2)                #
                                                            #
right_frame = ttk.Frame(window)                             #
right_frame.pack(side='right', padx=8, pady=2)              #

# Speicher für Buttons und Auswahl
sound_buttons = []         # Liste mit (pfad, button)
selected_sound = [None]    # damit innerhalb innerer Funktionen änderbar

# Funktion zum erstellen von Buttons beim Laden

def create_sound_button(filepath):
    button_text = os.path.splitext(os.path.basename(filepath))[0]

    def select():
        for _, btn in sound_buttons:
            btn.config(style='TButton')                         # Vorherige Auswahl optisch zurücksetzen
        new_button.config(style='Selected.TButton')             # Markiere ausgewählten Button
        selected_sound[0] = filepath                            # Merke Dateipfad

    new_button = ttk.Button(left_frame, text=button_text, command=select)
    new_button.pack(padx=5, pady=5)

    sound_buttons.append((filepath, new_button))                # Zur Buttonliste hinzufügen

# Funktion zum laden der Sounddateien
def load_sounds_from_file():
    if not os.path.exists(SOUND_JSON_PATH):
        return  # keine Datei vorhanden dann ist nichts zu laden

    try:
        with open(SOUND_JSON_PATH, "r", encoding="utf-8") as f:
            sound_paths = json.load(f)          # Lade Liste von Pfaden

        for path in sound_paths:
            if os.path.exists(path):            # Nur vorhandene Dateien verwenden
                create_sound_button(path)       # Erzeuge passenden Button

    except Exception as e:
        print(f"Fehler beim Laden der Sounds: {e}")

# Funktion um Soundliste in JSON Datei zu speichern
def save_sounds_to_file():
    paths = [path for path, _ in sound_buttons]                 # Nur die Pfade extrahieren
    with open(SOUND_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(paths, f, indent=4)                           # Speichere als JSON (lesbar formatiert)

# Funktion um Sound hinzuzufügen über Dateidialog
def add_sound():
    filetypes = (
        ('MP3 Dateien', '*.mp3'),
        ('WAV Dateien', '*.wav'),
        ('Alle Dateien', '*.*')
    )

    filename = fd.askopenfilename(
        title='Sound hinzufügen',
        initialdir='/',
        filetypes=filetypes
    )

    if filename:
        # Doppelte Einträge verhindern
        if any(existing_path == filename for existing_path, _ in sound_buttons):
            showinfo("Hinweis", "Sound wurde bereits hinzugefügt.")
            return

        create_sound_button(filename)
        showinfo(title='Sound hinzugefügt', message=os.path.basename(filename))
        save_sounds_to_file()               # Speichern nach Hinzufügen

# Funktion um Sound abzuspielen
def play_sound():
    sound_path = selected_sound[0]
    if sound_path:
        try:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        except Exception as e:
            showinfo(title="Fehler", message=f"Konnte Sound nicht abspielen:\n{e}")
    else:
        showinfo(title="Hinweis", message="Kein Sound ausgewählt!")

# Funktion um Sound zu stoppen
def stop_sound():
    pygame.mixer.music.stop()

# Funktion um die Lautstärke zu setzen (Slider -> pygame erwartet 0.0 bis 1.0)
def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

# Funktion um das Programm zu beenden
def quit_program():
    pygame.mixer.quit()         # Mixer freigeben
    window.quit()               # GUI schließen

# Stile definieren (normaler Button & ausgewählt)
style = ttk.Style()
style.configure('TButton', font=('Arial', 10))
style.configure('Selected.TButton', font=('Arial', 10, 'bold'), background='#aee')

# GUI-Steuerelemente
add_button = ttk.Button(top_frame, text='🎵 Sound hinzufügen', command=add_sound)
add_button.pack()

play_button = ttk.Button(right_frame, text="▶️ abspielen", command=play_sound)
play_button.pack()

stop_button = ttk.Button(right_frame, text="⏹️ stoppen", command=stop_sound)
stop_button.pack()

# Lautstärkeregler (Slider)
volume_slider = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                         label="Lautstärke", command=set_volume)
volume_slider.set(70)  # Anfangslautstärke
volume_slider.pack()

end_button = ttk.Button(bottom_frame, text="❌ Beenden", command=quit_program)
end_button.pack()

# Laden der gespeicherten Sounds aus der JSON Datei
load_sounds_from_file()

# GUI starten
window.mainloop()