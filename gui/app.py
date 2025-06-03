import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import os
import pygame

from logic import SoundboardState  # Achte auf korrekten Importpfad

class SoundboardApp:
    def __init__(self, root):
        """ 
        Initialisiert die Soundboard-Anwendung.
        Erstellt das Hauptfenster, das Menü und die Buttons.
        :param root: Das Hauptfenster der Anwendung (Instanz von tk.Tk)
        """
        self.root = root
        self.root.title("Soundboard")

        # pygame für Audio
        pygame.mixer.init()

        self.state = SoundboardState()

        self._setup_menu()
        self._setup_buttons()

    def _setup_menu(self):
        """ 
        Erstellt das Menü für die Anwendung.
        Ermöglicht das Laden von Sounddateien und Beenden der Anwendung.
        """
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Sounddatei laden", command=self._load_file)
        file_menu.add_command(label="Beenden", command=self.root.quit)
        menubar.add_cascade(label="Datei", menu=file_menu)
        self.root.config(menu=menubar)

    def _setup_buttons(self):
        """
        Erstellt die 6 Buttons für das Soundboard.
        Jeder Button kann eine Sounddatei zugewiesen bekommen.
        Die Buttons sind in einem 2x3 Grid angeordnet.
        Jeder Button hat eine eigene Callback-Funktion, die den zugewiesenen Sound abspielt.
        """
        self.buttons = []
        for i in range(6):
            btn = ttk.Button(self.root, text=f"Button {i + 1}", command=lambda i=i: self._on_button_click(i))
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=10, ipadx=10, ipady=10)
            self.buttons.append(btn)

    def _load_file(self):
        """
        Lädt eine Sounddatei und weist sie einem Button zu.
        Der Benutzer wählt den Button und die Sounddatei aus.
        Der Benutzer kann optional einen Namen für den Button eingeben.
        Wenn kein Name eingegeben wird, wird der Dateiname als Label verwendet.
        :return: None
        :raises: Exception bei Fehlern während des Datei-Ladevorgangs
        """
        filepath = filedialog.askopenfilename(filetypes=[("Sound-Dateien", "*.mp3 *.wav")])
        if not filepath:
            return  # kein Pfad ausgewählt → nichts tun

        index = simpledialog.askinteger("Button wählen", "Gib die Button-Nummer (1–6) ein:", 
                                        minvalue=1, maxvalue=6, parent=self.root)
        if index is None:
            return  # kein Button ausgewählt → nichts tun

        try:
            custom_name = simpledialog.askstring("Name eingeben", "Gib einen Namen für den Button ein (optional):",
                                                 parent=self.root)
            if not custom_name:
                custom_name = os.path.basename(filepath)

            self.state.assign_sound(index - 1, filepath, custom_name)
            self.buttons[index - 1].config(text=custom_name)
            print(f"Sound '{filepath}' wurde Button {index} als '{custom_name}' zugewiesen.")
        except Exception as e:
            print("Fehler bei der Button-Zuweisung:", e)

    def _on_button_click(self, index):
        """
        Reagiert auf Klicks auf die Buttons.
        Spielt den zugewiesenen Sound ab, wenn vorhanden.
        :param index: Index des geklickten Buttons (0-5)
        :return: None
        """
        filepath = self.state.get_sound(index)
        if filepath:
            try:
                print(f"Spiele Sound: {filepath}")
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Fehler beim Abspielen des Sounds: {e}")
        else:
            print(f"Kein Sound für Button {index + 1} zugewiesen.")
