import os
import json
import pygame
from tkinter import filedialog as fd, messagebox as mb
from tkinter import ttk

SOUND_JSON_PATH = "sounds.json"

pygame.mixer.init()

sound_buttons = []
selected_sound = [None]

def create_sound_button(filepath, frame, style):
    button_text = os.path.splitext(os.path.basename(filepath))[0]

    def select():
        for _, btn in sound_buttons:
            btn.config(style=style)
        new_button.config(style='Selected.TButton')
        selected_sound[0] = filepath

    new_button = ttk.Button(frame, text=button_text, command=select)
    new_button.pack(padx=5, pady=5)
    sound_buttons.append((filepath, new_button))

def load_sounds_from_file(frame, style):
    if not os.path.exists(SOUND_JSON_PATH):
        return

    try:
        with open(SOUND_JSON_PATH, "r", encoding="utf-8") as f:
            sound_paths = json.load(f)

        for path in sound_paths:
            if os.path.exists(path):
                create_sound_button(path, frame, style)
    except Exception as e:
        print(f"Fehler beim Laden der Sounds: {e}")

def save_sounds_to_file():
    paths = [path for path, _ in sound_buttons]
    with open(SOUND_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(paths, f, indent=4)

def add_sound(frame, style):
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
        if any(existing_path == filename for existing_path, _ in sound_buttons):
            mb.showinfo("Hinweis", "Sound wurde bereits hinzugefügt.")
            return

        create_sound_button(filename, frame, style)
        mb.showinfo(title='Sound hinzugefügt', message=os.path.basename(filename))
        save_sounds_to_file()

def play_sound():
    sound_path = selected_sound[0]
    if sound_path:
        try:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        except Exception as e:
            mb.showinfo(title="Fehler", message=f"Konnte Sound nicht abspielen:\n{e}")
    else:
        mb.showinfo(title="Hinweis", message="Kein Sound ausgewählt!")

def stop_sound():
    pygame.mixer.music.stop()

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def quit_program(window):
    pygame.mixer.quit()
    window.quit()