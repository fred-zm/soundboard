import os
import json
import pygame
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk

SOUND_JSON_PATH = "sounds.json"

pygame.mixer.init()

window = tk.Tk()
window.title("Soundboard Zukunftsmotor K17")
window.geometry("600x600")

top_frame = ttk.Frame(window)
top_frame.pack(side='top', padx=5, pady=0)

bottom_frame = ttk.Frame(window)
bottom_frame.pack(side='bottom', padx=5, pady=10)

left_frame = ttk.Frame(window)
left_frame.pack(side='left', padx=2, pady=2)

right_frame = ttk.Frame(window)
right_frame.pack(side='right', padx=8, pady=2)

sound_buttons = []
selected_sound = [None]

def create_sound_button(filepath):
    button_text = os.path.splitext(os.path.basename(filepath))[0]

    def select():
        for _, btn in sound_buttons:
            btn.config(style='TButton')
        new_button.config(style='Selected.TButton')
        selected_sound[0] = filepath

    new_button = ttk.Button(left_frame, text=button_text, command=select)
    new_button.pack(padx=5, pady=5)

    sound_buttons.append((filepath, new_button))

def load_sounds_from_file():
    if not os.path.exists(SOUND_JSON_PATH):
        return

    try:
        with open(SOUND_JSON_PATH, "r", encoding="utf-8") as f:
            sound_paths = json.load(f)

        for path in sound_paths:
            if os.path.exists(path):
                create_sound_button(path)

    except Exception as e:
        print(f"Fehler beim Laden der Sounds: {e}")

def save_sounds_to_file():
    paths = [path for path, _ in sound_buttons]
    with open(SOUND_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(paths, f, indent=4)

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
        if any(existing_path == filename for existing_path, _ in sound_buttons):
            showinfo("Hinweis", "Sound wurde bereits hinzugefügt.")
            return

        create_sound_button(filename)
        showinfo(title='Sound hinzugefügt', message=os.path.basename(filename))
        save_sounds_to_file()

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

def stop_sound():
    pygame.mixer.music.stop()

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

def quit_program():
    pygame.mixer.quit()
    window.quit()

style = ttk.Style()
style.configure('TButton', font=('Arial', 10))
style.configure('Selected.TButton', font=('Arial', 10, 'bold'), background='#aee')

add_button = ttk.Button(top_frame, text='🎵 Sound hinzufügen', command=add_sound)
add_button.pack()

play_button = ttk.Button(right_frame, text="▶️ abspielen", command=play_sound)
play_button.pack()

stop_button = ttk.Button(right_frame, text="⏹️ stoppen", command=stop_sound)
stop_button.pack()

volume_slider = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                         label="Lautstärke", command=set_volume)
volume_slider.set(70)
volume_slider.pack()

end_button = ttk.Button(bottom_frame, text="❌ Beenden", command=quit_program)
end_button.pack()

load_sounds_from_file()

window.mainloop()