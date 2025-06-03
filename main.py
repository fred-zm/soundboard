import tkinter as tk
from tkinter import messagebox



def datei_oeffnen():
    messagebox.showinfo('Viel Spaß jetzt öffnen.')

def datei_speichern():
    messagebox.showinfo('Speichern')

def datei_beenden():
    fenster.quit()
# Hauptfenster erstellen

fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")

testbutton = tk.Button(text="test")
testbutton.pack()
button = tk.Button(text='Beenden', command=fenster.destroy)
button.pack()
#menü



# GUI starten
fenster.mainloop()