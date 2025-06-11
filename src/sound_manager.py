# sound_manager.py
import pygame
import os
import json
import time
import threading
from tkinter.messagebox import showinfo

class SoundManager:
    def __init__(self):
        """
        Initialisiert den SoundManager und lädt die Standard-Sounds.
        Diese Klasse verwaltet die Sounddateien, ermöglicht das Abspielen von Sounds
        und speichert die Benutzereinstellungen in einer JSON-Datei.
        Die Sounddateien werden in einem Ordner pro Benutzer gespeichert, der nach dem Benutzernamen benannt ist.
        Die Standard-Sounds sind Platzhalter und können vom Benutzer angepasst werden.        
        """
        pygame.mixer.init()
        self.username = None
        self.SOUNDS_FILE = None
        self.button_sounds = {
            "Sound_01": "example.mp3",
            "Sound_02": "example.mp3",
            "Sound_03": "example.mp3",
            "Sound_04": "example.mp3",
            "Sound_05": "example.mp3",
        }
        self.loop = False

    def set_user(self, username):
        """
        Setzt den Benutzernamen und initialisiert den Soundordner für diesen Benutzer.
        Erstellt den Ordner, falls er nicht existiert, und lädt die zugehörigen Sounds.
        :param username: Der Name des Benutzers, für den die Sounds gespeichert werden sollen.
        """
        self.username = username
        user_folder = os.path.join("sounds", username)
        os.makedirs(user_folder, exist_ok=True)
        self.SOUNDS_FILE = os.path.join(user_folder, "sounds.json")
        self.load_sounds()

    def save_sounds(self):
        """
        Speichert die aktuellen Soundeinstellungen in einer JSON-Datei.
        Diese Datei wird im Benutzerordner gespeichert und enthält die Zuordnungen
        von Soundnamen zu Dateipfaden.
        """
        if self.SOUNDS_FILE:
            with open(self.SOUNDS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.button_sounds, f)

    def load_sounds(self):
        """
        Lädt die Soundeinstellungen aus der JSON-Datei, die im Benutzerordner gespeichert ist.
        Wenn die Datei nicht existiert, werden Standardwerte verwendet.
        Diese Methode wird aufgerufen, wenn ein Benutzer gesetzt wird oder wenn der SoundManager initialisiert wird.
        """
        if self.SOUNDS_FILE and os.path.exists(self.SOUNDS_FILE):
            with open(self.SOUNDS_FILE, "r", encoding="utf-8") as f:
                self.button_sounds = json.load(f)
        else:
            # Standardwerte setzen, falls Datei nicht existiert
            self.button_sounds = {
                "Sound_01": "example.mp3",
                "Sound_02": "example.mp3",
                "Sound_03": "example.mp3",
                "Sound_04": "example.mp3",
                "Sound_05": "example.mp3",
            }

    def assign_sound(self, name, path):
        """
        Weist einem Soundnamen einen Dateipfad zu.
        :param name: Der Name des Sounds, der zugewiesen werden soll.
        :param path: Der Dateipfad zur Sounddatei.
        """
        self.button_sounds[name] = path

    def get_sound(self, name):
        """
        Gibt den Dateipfad des Sounds zurück, der dem angegebenen Namen zugeordnet ist.
        :param name: Der Name des Sounds, dessen Dateipfad abgerufen werden soll.
        :return: Der Dateipfad der Sounddatei oder None, wenn der Sound nicht existiert.
        """
        return self.button_sounds.get(name)

    def play_sound(self, name):
        """
        Spielt den Sound ab, der dem angegebenen Namen zugeordnet ist.
        Wenn bereits Musik abgespielt wird, wird sie gestoppt, bevor der neue Sound geladen wird.
        :param name: Der Name des Sounds, der abgespielt werden soll.
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            return
        pfad = self.get_sound(name)
        if pfad:
            try:
                pygame.mixer.music.load(pfad)
                loops = -1 if self.loop else 0
                pygame.mixer.music.play(loops=loops)
            except Exception as e:
                showinfo("Fehler", f"Konnte Sound nicht abspielen:\n{e}")
        else:
            showinfo("Kein Sound", f"{name} hat noch keinen Sound.")

    def set_loop(self, loop_value):
        """
        Setzt den Loop-Modus für die Musik.
        :param loop_value: Boolean, ob die Musik in einer Endlosschleife abgespielt werden soll.
        """
        self.loop = loop_value

    def set_volume(self, volume):
        """
        Setzt die Lautstärke der Musik.
        :param volume: Float-Wert zwischen 0.0 (stumm) und 1.0 (maximale Lautstärke
        """
        pygame.mixer.music.set_volume(volume)

    def play_all_sounds(self, names):
        """
        Spielt alle Sounds ab, die in der Liste `names` angegeben sind.
        Diese Methode lädt jeden Sound nacheinander und spielt ihn ab.
        :param names: Liste von Soundnamen, die abgespielt werden sollen.
        """
        def play_all():
            """
            Hilfsfunktion, die in einem separaten Thread läuft, um Sounds nacheinander abzuspielen.
            """
            for name in names:
                pfad = self.get_sound(name)
                if pfad:
                    try:
                        pygame.mixer.music.load(pfad)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                    except Exception as e:
                        showinfo("Fehler", f"Konnte Sound nicht abspielen:\n{e}")
        threading.Thread(target=play_all, daemon=True).start()

    def stop_music(self):
        """
        Stoppt die aktuell abgespielte Musik.
        Diese Methode wird verwendet, um die Musik zu stoppen, wenn der Benutzer dies wünscht.
        """
        pygame.mixer.music.stop()

    def quit(self):
        """
        Beendet den SoundManager und schließt den Mixer.
        Diese Methode sollte aufgerufen werden, wenn das Programm beendet wird,
        um sicherzustellen, dass alle Ressourcen freigegeben werden.
        """
        self.save_sounds()
        pygame.mixer.quit()