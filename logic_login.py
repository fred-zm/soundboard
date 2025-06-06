import os
import json
import pygame
from tkinter import filedialog as fd, messagebox as mb
from tkinter import ttk

USER_JSON_PATH = "users.json"
current_user = {"name": None}

pygame.mixer.init()

# Globale Verwaltung der Buttons und Auswahl
sound_buttons = []
selected_sound = [None]

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
        is_logged_in = False

def create_sound_button(filepath, frame, style):
    button_text = os.path.splitext(os.path.basename(filepath))[0]

    def select():
        for _, btn in sound_buttons:
            btn.config(style=style)
        new_button.config(style='Selected.TButton')
        selected_sound[0] = filepath

    new_button = ttk.Button(frame, text=button_text, command=select)
    new_button.pack(padx=5, pady=5, fill='x', anchor='w')  # Buttons dehnen sich in der Breite
    sound_buttons.append((filepath, new_button))

def load_sounds_for_user(frame, style):
    if current_user["name"] is None:
        return

    try:
        with open(USER_JSON_PATH, "r", encoding="utf-8") as f:
            users = json.load(f)
            sound_paths = users[current_user["name"]]["sounds"]

        for path in sound_paths:
            if os.path.exists(path):
                create_sound_button(path, frame, style)
    except Exception as e:
        print(f"Fehler beim Laden der Sounds: {e}")

def save_sounds_for_user():
    if current_user["name"] is None:
        return

    try:
        with open(USER_JSON_PATH, "r+", encoding="utf-8") as f:
            users = json.load(f)
            users[current_user["name"]]["sounds"] = [p for p, _ in sound_buttons]
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

    filename = fd.askopenfilename(
        title='Sound hinzufügen',
        initialdir='./sounds',
        filetypes=filetypes
    )

    if filename:
        if any(existing_path == filename for existing_path, _ in sound_buttons):
            mb.showinfo("Hinweis", "Sound wurde bereits hinzugefügt.")
            return

        create_sound_button(filename, frame, style)
        mb.showinfo(title='Sound hinzugefügt', message=os.path.basename(filename))
        save_sounds_for_user()

def remove_selected_sound(frame):
    if selected_sound[0] is None:
        mb.showinfo("Hinweis", "Kein Sound ausgewählt!")
        return

    for i, (path, button) in enumerate(sound_buttons):
        if path == selected_sound[0]:
            button.destroy()
            del sound_buttons[i]
            selected_sound[0] = None
            save_sounds_for_user()
            mb.showinfo("Sound entfernt", "Der Sound wurde entfernt.")
            return

    mb.showinfo("Fehler", "Sound konnte nicht gefunden werden.")

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