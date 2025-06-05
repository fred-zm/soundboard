import tkinter as tk
from tkinter import ttk
import logic


def build_gui():
    window = tk.Tk()
    window.title("Soundboard Zukunftsmotor K17")
    window.geometry("1000x600")

    window.grid_rowconfigure(0, weight=0)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=0)
    window.grid_columnconfigure(0, weight=1)

    # Frames

    top_frame = ttk.Frame(window)
    top_frame.grid(row=0, column=0)

    middle_frame = ttk.Frame(window)
    middle_frame.grid(row=1, column=0)
    middle_frame.grid_rowconfigure(0, weight=1)
    middle_frame.grid_rowconfigure(1, weight=1)
    middle_frame.grid_columnconfigure(0, weight=1)
    middle_frame.grid_columnconfigure(1, weight=1)

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

    ttk.Button(
        top_frame,
        text="🎵 Sound hinzufügen",
        padding=(20, 20),
        command=lambda: logic.add_sound(middle_frame, "TButton"),
    ).pack()

    ttk.Button(
        top_frame,
        text="🗑️ Sound entfernen",
        command=lambda: logic.update_sound(middle_frame),
    ).pack()

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

    ttk.Button(
        top_frame, text="❌ Beenden", command=lambda: logic.quit_program(window)
    ).pack()

    logic.load_sounds_from_file(middle_frame, "TButton")

    return window
