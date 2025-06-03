import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk

# Hauptfenster
fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")

# Funktion zum Dateiöffnen
def datei_oeffnen():
    mb.showinfo("Öffnen")
    filetypes = (('text files', '*.txt'), ('All files', '*.*'))
    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    if filename:
        showinfo(title='Selected File', message=filename)

# Button zur Dateiöffnen Funktion
open_button = ttk.Button(fenster, text='Open a File', command=datei_oeffnen)
open_button.pack()

# Wird aktuell nicht genutzt
###############################
# def datei_speichern():
    # mb.showinfo("Speichern")
###############################

# Funktion zum Beenden 
def datei_beenden():
    fenster.quit()

# Button zur Beenden Funktion
end_button = ttk.Button(text="Beenden", command=datei_beenden)
end_button.pack(side="bottom")

# Liste für die Schleife
button_list = []
text_variable = ['sound1', 'sound2', 'sound3', 'sound4']

# Schleife für dynamische Buttons
for word in text_variable:
    button2 = ttk.Button(text=word)
    button2.pack(anchor="w", pady="15") #anchor=w ordnet linksbündig ein 
    button_list.append(button2)

# GUI starten
fenster.mainloop()