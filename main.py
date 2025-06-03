
# ** Soundwiedergabe
# pip install pygame

import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk
import pygame

# - Hauptfenster erstellen

fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")


# - Funktionen für Text Dateien

def datei_oeffnen():
    mb.showinfo("Öffnen")
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )

def datei_speichern():
    mb.showinfo("Speichern")

def datei_beenden():
    fenster.quit()

# ** Funktionen für Sound Dateien / Benutzer Wahl ** 
# - Pygame für Sound vorbereiten
pygame.mixer.init()

# Zuordnung: Zahl => Sounddatei Pfad
sounds = {
    1: "sound1.mp3",
    2: "sound2.mp3",
    3: "sound3.mp3",
    4: "sound4.mp3",
    5: "sound5.mp3",
    6: "sound6.mp3"
}

def play_sound(note):
    sound_file = sounds.get(note)
    if sound_file:
        try:
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Fehler beim Abspielen: {e}")
    else:
        print("Ungültige Eingabe!")



# *** GUI ***
# - Button für Text Dateien
open_button = ttk.Button(fenster, text='Open a File', command=datei_oeffnen)
open_button.pack()

end_button = tk.Button(fenster, text="Beenden", command=datei_beenden)
end_button.pack()


# -  Button für Sound Dateien
jingle1 = ttk.Button(fenster, text='Song1🎶', width=20, padding=10)
jingle1.pack(side='top')

#play_button = tk.Button(fenster, text="Play")
#play_button.pack()


# - Buttons mit for Schleife erstellen
 
button_list = []
text_variable = ['sound1', 'sound2', 'sound3', 'sound4']

for elm in text_variable:
    button2 = ttk.Button(text=elm)
    button2.pack(side='left', expand=True)#wollen wir das nebeneinander haben ?
    button_list.append(button2)


# ** GUI für Sound Dateien / Benutzer Wahl ** 

Label1 = tk.Label(fenster, text="Wähle eine Zahl von 1 bis 6:", font=("Arial", 12))
Label1.pack(pady=10)

for i in range(1, 7):
    tk.Button(fenster, text=f"Sound {i}", width=10, height=2, command=lambda i=i: play_sound(i)).pack(pady=5, side='left')





# print(jingle1.keys())


# GUI starten
fenster.mainloop()