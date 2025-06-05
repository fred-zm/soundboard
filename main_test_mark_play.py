import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk
import pygame

# Pygame Mixer initialisieren
pygame.mixer.init()

# Hauptfenster
window = tk.Tk()
window.title("Soundboard Zukunftsmotor K17")
window.geometry("1200x800")

# Frames
top_frame = tk.Frame(window)
top_frame.pack(side='top', padx=5, pady=0)

bottom_frame = tk.Frame(window)
bottom_frame.pack(side='bottom', padx=5, pady=10)

left_frame = tk.Frame(window)
left_frame.pack(side='left', padx=2, pady=2)

# Speicher für Buttons und Auswahl
sound_buttons = []         # Liste mit (pfad, button)
selected_sound = [None]    # Mutable, damit innerhalb innerer Funktionen änderbar

# Sound hinzufügen
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
        button_text = os.path.splitext(os.path.basename(filename))[0]

        # Erstelle den Button mit Auswahlfunktion
        def select():
            # Vorherige Auswahl zurücksetzen
            for _, btn in sound_buttons:
                btn.config(style='TButton')
            # Neue Auswahl setzen und optisch markieren
            new_button.config(style='Selected.TButton')
            selected_sound[0] = filename

        new_button = ttk.Button(left_frame, text=button_text, command=select)
        new_button.pack()

        sound_buttons.append((filename, new_button))
        showinfo(title='Sound hinzugefügt', message=f'{button_text} wurde hinzugefügt.')

# Sound abspielen
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

# Programm beenden
def quit_program():
    pygame.mixer.quit()
    window.quit()

# Stil für ausgewählten Button
style = ttk.Style()
style.configure('TButton', font=('Arial', 10))
style.configure('Selected.TButton', font=('Arial', 10, 'bold'), background='#aee')

# GUI-Steuerelemente
add_button = tk.Button(top_frame, text='Sound hinzufügen', command=add_sound)
add_button.pack()

play_button = tk.Button(bottom_frame, text="Sound abspielen", command=play_sound)
play_button.pack()

end_button = tk.Button(bottom_frame, text="Beenden", command=quit_program)
end_button.pack()

# GUI starten
window.mainloop()