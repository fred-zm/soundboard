import os
import json
import pygame
from tkinter import filedialog as fd, messagebox as mb
from tkinter import ttk

SOUND_JSON_PATH = "sounds.json"

pygame.mixer.init()

# Globale Verwaltung der Buttons und Auswahl
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
    #new_button.pack(padx=5, pady=5, fill='x', anchor='w')  # Buttons dehnen sich in der Breite
    sound_buttons.append((filepath, new_button))
    refresh_sound_buttons(frame)


def refresh_sound_buttons(frame):
    column_count = 3
    row_count = len(sound_buttons)/column_count
    if row_count > int(row_count):
        row_count +=1
    row_count = int(row_count)
    for y in range(row_count):
        frame.rowconfigure(y, weight=1)
        for x in range(column_count):
            frame.columnconfigure(x, weight=1)
            button_index = x + y * column_count
            if button_index > len(sound_buttons) -1:
                return
            sound_buttons[button_index][1].grid(column=x*1, row=y, padx=5, pady=5, sticky='nesw')


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
        initialdir='./sounds',
        filetypes=filetypes
    )

    if filename:
        if any(existing_path == filename for existing_path, _ in sound_buttons):
            mb.showinfo("Hinweis", "Sound wurde bereits hinzugefügt.")
            return

        create_sound_button(filename, frame, style)
        mb.showinfo(title='Sound hinzugefügt', message=os.path.basename(filename))
        save_sounds_to_file()

def remove_selected_sound(frame):
    if selected_sound[0] is None:
        mb.showinfo("Hinweis", "Kein Sound ausgewählt!")
        return

    for i, (path, button) in enumerate(sound_buttons):
        if path == selected_sound[0]:
            button.destroy()
            del sound_buttons[i]
            selected_sound[0] = None
            save_sounds_to_file()
            mb.showinfo("Sound entfernt", "Der Sound wurde entfernt.")
            return

    refresh_sound_buttons(frame)
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


def login(gui, benutzer, passwort):
    with open("accounts.json", "r", encoding="utf-8") as f:
        accounts = json.load(f)
        try:
            if passwort == accounts[benutzer]["pass"]:
                gui.is_logged_in = True
                gui.login_window.destroy()
            else:
                mb.showerror("", "Falsches Passwort")
        except:
            mb.showerror("", "Benutzer nicht vorhanden")