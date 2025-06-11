# main.py
import tkinter as tk
from src.gui_elements import create_main_interface, show_login_window
from src.sound_manager import SoundManager
from src.user_db import init_db

# Hauptprogramm starten
if __name__ == '__main__':
    """
    Startet die Soundboard-Anwendung.
    Diese Funktion initialisiert die Datenbank, erstellt das Hauptfenster
    und zeigt die Login- oder Registrierungsoberfläche an.
    Die SoundManager-Klasse wird instanziiert, um die Soundeinstellungen zu verwalten.
    """
    init_db()

    fenster = tk.Tk()
    fenster.title("Soundboard v1.0")
    fenster.geometry("600x700")
    fenster.resizable(False, False)
    
    canvas = tk.Canvas(fenster, width=600, height=700, bg="#ffffff")
    canvas.pack()

    sound_manager = SoundManager()

    create_main_interface(fenster, canvas, sound_manager)
    show_login_window(fenster, sound_manager)

    fenster.mainloop()