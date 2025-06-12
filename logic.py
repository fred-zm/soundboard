import os
import json
import pygame
from tkinter import filedialog as fd, messagebox as mb
from tkinter import ttk

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

USER_JSON_PATH = "users.json"
current_user = {"name": None}

pygame.mixer.init()

sound_buttons = []
selected_sound = [None]

def create_user(username, password):
    if not username or not password:
        return False

    if not os.path.exists(USER_JSON_PATH):
        users = {}
    else:
        with open(USER_JSON_PATH, "r", encoding="utf-8") as f:
            users = json.load(f)

    if username in users:
        return False

    users[username] = {
        "password": password,
        "sounds": []
    }

    try:
        with open(USER_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
        return True
    except Exception as e:
        print(f"Fehler beim Speichern des neuen Benutzers: {e}")
        return False

def login_user(username, password, frame, callback):
    if not os.path.exists(USER_JSON_PATH):
        mb.showerror("Fehler", "Benutzerdaten nicht gefunden.")
        return False

    with open(USER_JSON_PATH, "r", encoding="utf-8") as f:
        users = json.load(f)

    if username in users and users[username]["password"] == password:
        current_user["name"] = username
        frame.destroy()
        callback()
    else:
        mb.showerror("Login fehlgeschlagen", "Falscher Benutzername oder Passwort.")

def create_sound_button(filepath, frame, style):
    filepath = os.path.abspath(filepath)
    
    button_text = os.path.splitext(os.path.basename(filepath))[0]

    def select():
        for _, btn in sound_buttons:
            btn.config(style=style)
        new_button.config(style='Selected.TButton')
        selected_sound[0] = filepath

    new_button = ttk.Button(frame, text=button_text, command=select)

    index = len(sound_buttons)
    columns_per_row = 4
    row = index // columns_per_row
    col = index % columns_per_row

    new_button.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
    frame.grid_columnconfigure(col, weight=1)

    sound_buttons.append((filepath, new_button))

def load_sounds_for_user(frame, style):
    if current_user["name"] is None:
        return

    try:
        with open(USER_JSON_PATH, "r", encoding="utf-8") as f:
            users = json.load(f)
            sound_paths = users[current_user["name"]]["sounds"]

        for path in sound_paths:
            abs_path = os.path.join(PROJECT_DIR, path)
            if os.path.exists(abs_path):
                create_sound_button(abs_path, frame, style)
    except Exception as e:
        print(f"Fehler beim Laden der Sounds: {e}")

def save_sounds_for_user():
    if current_user["name"] is None:
        return

    try:
        with open(USER_JSON_PATH, "r+", encoding="utf-8") as f:
            users = json.load(f)
            users[current_user["name"]]["sounds"] = [os.path.relpath(p, PROJECT_DIR) for p, _ in sound_buttons]
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()
    except Exception as e:
        print(f"Fehler beim Speichern der Sounds: {e}")

def add_sound(frame, style):
    filetypes = (
        ('MP3 Dateien', '*.mp3'),
        ('WAV Dateien', '*.wav'),
        ('Alle Dateien', '*.*')
    )

    filenames = fd.askopenfilenames(
        title='Sounds hinzufügen',
        initialdir='./sounds',
        filetypes=filetypes
    )

    if not filenames:
        return

    added_count = 0
    for filename in filenames:
        abs_filename = os.path.abspath(filename)

        if any(os.path.samefile(abs_filename, existing_path) for existing_path, _ in sound_buttons):
            continue

        create_sound_button(abs_filename, frame, style)
        added_count += 1

    if added_count:
        save_sounds_for_user()
    else:
        mb.showinfo("Hinweis", "Sound(s) bereits vorhanden.")

def remove_selected_sound(frame):
    if selected_sound[0] is None:
        mb.showinfo("Hinweis", "Kein Sound ausgewählt!")
        return

    for i, (path, button) in enumerate(sound_buttons):
        if path == selected_sound[0]:
            button.destroy()
            del sound_buttons[i]
            selected_sound[0] = None
            rearrange_buttons(frame)
            save_sounds_for_user()
            return

    mb.showinfo("Fehler", "Sound konnte nicht gefunden werden.")

def rearrange_buttons(frame):
    columns_per_row = 4
    for index, (_, button) in enumerate(sound_buttons):
        row = index // columns_per_row
        col = index % columns_per_row
        button.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        frame.grid_columnconfigure(col, weight=1)

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