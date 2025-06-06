# state.py
import tkinter as tk
from tkinter import ttk
import json
import os

fenster = tk.Tk()

BG_COLOR = "#f0f0f0"
BTN_COLOR = "#f59506"

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton',
    padding=6,
    relief='flat',
    background=BTN_COLOR,
    foreground="black",
    borderwidth=0,
    focusthickness=0,
    focuscolor='none'
)
style.map('TButton', background=[('active', "#e73313"), ('pressed', "#e73313")])
style.configure("BG.TFrame", background=BG_COLOR)
style.configure("Custom.TCheckbutton", background=BG_COLOR)
style.map('TButton', background=[('active', "#e73313"), ('pressed', "#e73313")])
style.configure("BG.TFrame", background=BG_COLOR)
style.configure("Custom.TCheckbutton", background=BG_COLOR)
text_variable = ['Sound_01', 'Sound_02', 'Sound_03', 'Sound_04', 'Sound_05']
button_list = []
SOUNDS_FILE = "button_sounds.json"
loop_var = tk.BooleanVar(value=False)

button_sounds = {name: "example.mp3" for name in text_variable}

def sounds_speichern():
    with open(SOUNDS_FILE, "w", encoding="utf-8") as f:
        json.dump(button_sounds, f)

def sounds_laden():
    global button_sounds
    if os.path.exists(SOUNDS_FILE):
        with open(SOUNDS_FILE, "r", encoding="utf-8") as f:
            button_sounds = json.load(f)

sounds_laden()
