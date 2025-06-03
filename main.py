import tkinter as tk
from funktionen import datei_beenden, datei_oeffnen, datei_speichern 
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk

# Hauptfenster erstellen

fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")

# Menü


#zwei listen die wir brauchen
button_list = []
text_variable = ['sound1', 'sound2', 'sound3', 'sound4']

open_button = ttk.Button(
    fenster,
    text='Open a File',
    command=datei_oeffnen)
open_button.pack()
jingle1 = ttk.Button(fenster, text='Song1🎶', width=20, padding=50)
play_button = ttk.Button(fenster, text="Play")

play_button.pack()
for i in text_variable:
    button2 = ttk.Button(text=i)
    button2.pack(side='left', expand=True )#wollen wir das nebeneinander haben ?
    button_list.append(button2)

jingle1.pack(side='left')
end_button = ttk.Button(text="Beenden", command=datei_beenden)
end_button.pack()
for item in button2.keys():
    print(item, ':  ', button2[item])
    
 

# GUI starten
fenster.mainloop()