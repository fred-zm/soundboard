import tkinter as tk
from tkinter import ttk
import logic

def build_gui():
    window = tk.Tk()
    window.title("Soundboard Zukunftsmotor K17")
    window.geometry("600x600")

    menubar = tk.Menu(window)
    window.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Datei", menu=file_menu)

    file_menu.add_command(label="📂 Sound hinzufügen", command=lambda: logic.add_sound(left_frame, 'TButton'))
    file_menu.add_separator()
    file_menu.add_command(label="❌ Beenden", command=lambda: logic.quit_program(window))

    top_frame = ttk.Frame(window)
    top_frame.pack(side='top', padx=5, pady=0)

    bottom_frame = ttk.Frame(window)
    bottom_frame.pack(side='bottom', padx=5, pady=10)

    left_frame = ttk.Frame(window)
    left_frame.pack(side='left', padx=2, pady=2)

    right_frame = ttk.Frame(window)
    right_frame.pack(side='right', padx=8, pady=2)

    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10))
    style.configure('Selected.TButton', font=('Arial', 10, 'bold'), background='#aee', padding=(20, 20))

    ttk.Button(right_frame, text="🎶 abspielen", command=logic.play_sound).pack()
    ttk.Button(right_frame, text="🙊 stoppen", command=logic.stop_sound).pack()

    volume_slider = tk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                             label="Lautstärke", command=logic.set_volume)
    volume_slider.set(70)
    logic.set_volume(70)
    volume_slider.pack()

    logic.load_sounds_from_file(left_frame, 'TButton')

    return window