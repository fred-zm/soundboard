import tkinter as tk
from tkinter import ttk
import logic

def build_gui():
    window = tk.Tk()
    window.title("Soundboard Zukunftsmotor K17")
    window.geometry("1000x600")

    menubar = tk.Menu(window)
    window.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Datei", menu=file_menu)

    file_menu.add_command(label="📂 Sound hinzufügen", command=lambda: logic.add_sound(top_frame, 'TButton'))
    file_menu.add_command(label="🗑️ Sound entfernen", command=lambda: logic.update_sound(top_frame))
    file_menu.add_separator()
    file_menu.add_command(label="❌ Beenden", command=lambda: logic.quit_program(window))

    window.grid_rowconfigure(0, weight=0)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=0)
    window.grid_columnconfigure(0, weight=1)

    # Frames

    top_frame = ttk.Frame(window)
    top_frame.grid(row=1, column=0)
    top_frame.grid_rowconfigure(0, weight=1)
    top_frame.grid_rowconfigure(1, weight=1)
    top_frame.grid_columnconfigure(0, weight=1)
    top_frame.grid_columnconfigure(1, weight=1)

    bottom_frame = ttk.Frame(window)
    bottom_frame.grid(row=2, column=0)

    # Style

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10))
    style.configure(
        "Selected.TButton",
        font=("Arial", 10, "bold"),
        background="#aee",
        padding=(20, 20),
    )

    # Buttons

    ttk.Button(bottom_frame, text="▶️ abspielen", command=logic.play_sound).pack()
    ttk.Button(bottom_frame, text="⏹️ stoppen", command=logic.stop_sound).pack()

    volume_slider = tk.Scale(
        bottom_frame,
        from_=0,
        to=100,
        orient=tk.HORIZONTAL,
        label="Lautstärke",
        command=logic.set_volume,
    )
    volume_slider.set(70)
    logic.set_volume(70)
    volume_slider.pack()

    ttk.Button(bottom_frame, text="❌ Beenden",
               command=lambda: logic.quit_program(window)).pack()

    logic.load_sounds_from_file(top_frame, 'TButton')

    return window
