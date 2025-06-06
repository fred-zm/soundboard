# sound_manager.py
import pygame
import os
import json
import time
import threading
from tkinter.messagebox import showinfo

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.SOUNDS_FILE = "data/button_sounds.json"
        self.button_sounds = {
            "Sound_01": "example.mp3",
            "Sound_02": "example.mp3",
            "Sound_03": "example.mp3",
            "Sound_04": "example.mp3",
            "Sound_05": "example.mp3",
        }
        self.loop = False
        self.load_sounds()

    def save_sounds(self):
        with open(self.SOUNDS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.button_sounds, f)

    def load_sounds(self):
        if os.path.exists(self.SOUNDS_FILE):
            with open(self.SOUNDS_FILE, "r", encoding="utf-8") as f:
                self.button_sounds = json.load(f)

    def assign_sound(self, name, path):
        self.button_sounds[name] = path

    def get_sound(self, name):
        return self.button_sounds.get(name)

    def play_sound(self, name):
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
        self.loop = loop_value

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def play_all_sounds(self, names):
        def play_all():
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
        pygame.mixer.music.stop()

    def quit(self):
        self.save_sounds()
        pygame.mixer.quit()