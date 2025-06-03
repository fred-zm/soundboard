import tkinter as tk
from tkinter import ttk
from logic import datei_oeffnen, datei_speichern, datei_beenden
from widgets import create_sound_buttons

def create_gui():
    root = tk.Tk()
    root.title("Soundboard")
    root.geometry("600x300")

    # Linker Rahmen für Buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(side='left', fill='y', padx=10, pady=10)

    # Sound-Buttons
    text_variablen = ['Sound 1', 'Sound 2', 'Sound 3', 'Sound 4']
    create_sound_buttons(button_frame, text_variablen)

    # Buttons zum Bedienen
    ttk.Button(button_frame, text='Datei öffnen', command=datei_oeffnen).pack(anchor='w', pady=5)
    ttk.Button(button_frame, text='Datei speichern', command=datei_speichern).pack(anchor='w', pady=5)
    ttk.Button(button_frame, text='Beenden', command=lambda: datei_beenden(root)).pack(anchor='w', pady=5)

    root.mainloop()