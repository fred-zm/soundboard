import os
import json
import pygame
from tkinter import filedialog as fd, messagebox as mb
from tkinter import ttk
import io
import connect as db

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

USER_JSON_PATH = "users.json"
current_user = {"name": None}

pygame.mixer.init()

# Globale Verwaltung der Buttons und Auswahl
sound_buttons = []
selected_sound = None

def login_user(username, password, frame, callback):
    if not os.path.exists(USER_JSON_PATH):
        mb.showerror("Fehler", "Benutzerdaten nicht gefunden.")
        return False

    user = db.get_users(username)
    if 'id' in user and user['password'] == password:
        current_user["name"] = user['username']
        current_user["id"] = user['id']
        frame.destroy()
        # db.load_sounds(user['id'])
        callback()
    else:
        mb.showerror("Login fehlgeschlagen", "Falscher Benutzername oder Passwort.")

def create_sound_button(sound, frame, style):
    button_text = "Sound" + str(len(sound_buttons))

    def select():
        for _, btn in sound_buttons:
            btn.config(style=style)
        new_button.config(style='Selected.TButton')
        global selected_sound
        selected_sound = sound

    new_button = ttk.Button(frame, text=button_text, command=select)

    # Rasterposition: nebeneinander, dann neue Zeile
    index = len(sound_buttons)
    columns_per_row = 4
    row = index // columns_per_row
    col = index % columns_per_row

    new_button.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
    frame.grid_columnconfigure(col, weight=1)

    sound_buttons.append((sound, new_button))

def load_sounds_for_user(frame, style):
    if current_user["name"] is None:
        return

    sounds = db.load_sounds(current_user["id"])
    for (sound,) in sounds:
        create_sound_button(sound, frame, style)
    if False:
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
    if current_user["id"] is None:
        return

    db.save_sounds()
    if False:
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

        # Duplikate prüfen (immer mit absoluten Pfaden)
        sound = db.add_sound(abs_filename, current_user["id"])
        if sound:
            create_sound_button(sound, frame, style)
            added_count += 1

    if added_count:
        mb.showinfo(title='Sounds hinzugefügt', message=f"{added_count} Sound(s) wurden hinzugefügt.")
        save_sounds_for_user()
    else:
        mb.showinfo("Hinweis", "Alle ausgewählten Sounds sind bereits vorhanden.")

def remove_selected_sound(frame):
    if selected_sound is None:
        mb.showinfo("Hinweis", "Kein Sound ausgewählt!")
        return

    for i, (path, button) in enumerate(sound_buttons):
        if path == selected_sound:
            button.destroy()
            del sound_buttons[i]
            selected_sound = None
            rearrange_buttons(frame)  # Neu anordnen nach Entfernen
            save_sounds_for_user()
            mb.showinfo("Sound entfernt", "Der Sound wurde entfernt.")
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
    if selected_sound:
        try:
            sound_buffer = io.BytesIO(selected_sound)
            sound = pygame.mixer.Sound(sound_buffer)
            sound.play()
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