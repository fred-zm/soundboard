import os
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk

# Hauptfenster erstellen
window = tk.Tk()
window.title("Soundboard Zukunftsmotor K17")
window.geometry("1200x800")

# Frames
top_frame = tk.Frame(window)
top_frame.pack(side='top', padx=5, pady=0)

bottom_frame = tk.Frame(window)
bottom_frame.pack(side='bottom', padx=5, pady=10)

right_frame = tk.Frame(window)
right_frame.pack(side='right', padx=8, pady=2)

left_frame = tk.Frame(window)
left_frame.pack(side='left', padx=2, pady=2)

# Liste für gespeicherte Sounds (Pfad + Button)
sound_buttons = []

# Sound hinzufügen Funktion
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
        # Nur den Dateinamen (ohne Pfad) für den Button-Text
        button_text = os.path.basename(filename)

        # Button erstellen mit Dateiname
        new_button = ttk.Button(left_frame, text=button_text)
        new_button.pack(padx=5, pady=5)

        # Soundpfad speichern (später fürs Abspielen)
        sound_buttons.append((filename, new_button))

        showinfo(title='Sound hinzugefügt', message=f'{button_text} wurde hinzugefügt.')

# Programm beenden
def quit_program():
    window.quit()

# Buttons oben
add_button = tk.Button(top_frame, text='Sound hinzufügen', command=add_sound)
add_button.pack(pady=10)

# Buttons unten
play_button = tk.Button(bottom_frame, text="Sound abspielen (inaktiv)")  # Placeholder
play_button.pack(pady=5)

end_button = tk.Button(bottom_frame, text="Beenden", command=quit_program)
end_button.pack(pady=5)

# GUI starten
window.mainloop()