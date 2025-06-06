# ui.py
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import pygame

from components import (
    setup_canvas_background,
    create_info_label,
    create_sound_buttons,
    create_volume_control,
    create_loop_checkbox,
    create_bottom_buttons,
    show_login
)
from state import fenster

def start_app():
    pygame.mixer.init()

    fenster.title("Soundboard")
    fenster.geometry("600x700")
    fenster.resizable(False, False)

    canvas = tk.Canvas(fenster, width=600, height=700, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    setup_canvas_background(canvas)
    create_info_label(canvas)
    create_sound_buttons(canvas)
    create_volume_control(canvas)
    create_loop_checkbox(canvas)
    create_bottom_buttons(canvas)

    show_login(fenster, canvas)
    fenster.mainloop()
