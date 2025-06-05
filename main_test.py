#Bibliotheken importieren
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk

# Hauptfenster erstellen
window = tk.Tk()
window.title("Soundboard Zukunftsmotor K17")
window.geometry("1200x800")

top_frame =  tk.Frame(window)
top_frame.pack(side='top', padx = 5, pady=0)

bottom_frame = tk.Frame(window)
bottom_frame.pack(side='bottom', padx = 5, pady=10)

right_frame = tk.Frame(window)
right_frame.pack(side='right', padx = 8, pady=2)

left_frame = tk.Frame(window)
left_frame.pack(side='left', padx= 2, pady=2)

# Menüfunktionen
# Funktion Sound hinzufügen
def add_sound():
    filetypes = (
        ('Mp3', '*.mp3'),
        ('Wave', '*.wav')
    )

    filename = fd.askopenfilename(
        title='Sound hinzufügen',
        initialdir='/',
        filetypes=filetypes
    )

    if filename:
        showinfo(title='Ausgewählte Datei', message=filename)

# Programm beenden
def quit_program():
    window.quit()

# Sound-Button-Liste
button_list = []
sounds = ['sound1 🎶', 'sound2 🎶', 'sound3 🎶', 'sound4 🎶']

# Generiere Sound Buttons
for word in sounds:
    button = ttk.Button(window, text=word)
    button.pack(side='left', padx= 2, pady=2)
    button_list.append(button)

# Button um Sound hinzuzufügen
add_button = tk.Button(top_frame, text='Sound hinzufügen', command=add_sound)
add_button.pack()

# Play-Button
play_button = tk.Button(bottom_frame, text="Sound abspielen")
play_button.pack()

# Beenden-Button
end_button = tk.Button(bottom_frame, text="Beenden", command=quit_program,)
end_button.pack()

# GUI starten
window.mainloop()

# Jingle1 Button entfernt
# Funktion datei speichern entfernt