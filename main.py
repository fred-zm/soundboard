import tkinter as tk
from funktionen import datei_beenden, datei_oeffnen, buttons_erzeugen, datei_speichern

from tkinter import ttk

# Hauptfenster erstellen

fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x500")

# Menü


#zwei listen die wir brauchen
text_variable = ['sound1', 'sound2', 'sound3', 'sound4']
button_list = buttons_erzeugen(fenster, text_variable)

open_button = ttk.Button(fenster, text='Open a File', command=datei_oeffnen)
open_button.pack(side="top", anchor="w", padx=10, pady=5)

#leerer button würde löschen?
jingle1 = ttk.Button(fenster, text='Song1🎶', width=20, padding=50)
#pack einfach mehr hinzugefügt um es u "verankern(anchor)" 
jingle1.pack(side="top", anchor="w", padx=10, pady=5)

#leerer button würde löschen?
play_button = ttk.Button(fenster, text="Play")
play_button.pack(side="top", anchor="w", padx=10, pady=5)


#lambda ist eine leere funktion ist aber  damit man genau eine funktion ansagen kann 
end_button = ttk.Button(text="Beenden", command=lambda: datei_beenden(fenster))
end_button.pack(side="top", anchor="w", padx=10, pady=5)


# GUI starten
fenster.mainloop()