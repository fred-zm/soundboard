import tkinter as tk
from tkinter import ttk
import logic_scroll

def build_gui():
    window = tk.Tk()
    window.title("Soundboard Zukunftsmotor K17")
    window.geometry("600x600")

    # Menüleiste
    menubar = tk.Menu(window)
    window.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Datei", menu=file_menu)

    # Frames für Layout
    top_frame = ttk.Frame(window)
    top_frame.pack(side='top', padx=5, pady=0)

    bottom_frame = ttk.Frame(window)
    bottom_frame.pack(side='bottom', padx=5, pady=10)

    right_frame = ttk.Frame(window)
    right_frame.pack(side='right', padx=8, pady=2)

    # Scrollbarer Bereich für Sound-Buttons (links)
    left_container = ttk.Frame(window)
    left_container.pack(side='left', fill='both', expand=True, padx=2, pady=2)

    canvas = tk.Canvas(left_container)
    scrollbar = ttk.Scrollbar(left_container, orient='vertical', command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Menüfunktionen
    file_menu.add_command(label="🎵 Sound hinzufügen", command=lambda: logic_scroll.add_sound(scrollable_frame, 'TButton'))
    file_menu.add_separator()
    file_menu.add_command(label="❌ Beenden", command=lambda: logic_scroll.quit_program(window))

    # Styles
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10), padding=(20, 20))
    style.configure('Selected.TButton', font=('Arial', 10, 'bold'), background='#aee', width=15, padding=(20, 20))

    # Soundsteuerung (rechter Bereich)
    ttk.Button(bottom_frame, text="▶️ abspielen", command=logic_scroll.play_sound, width=20, padding=(20, 20)).pack()
    ttk.Button(bottom_frame, text="⏹️ stoppen", command=logic_scroll.stop_sound, width=20, padding=(20, 20)).pack()
    ttk.Button(bottom_frame, text="🗑️ Sound entfernen", command=lambda: logic_scroll.remove_selected_sound(scrollable_frame), width=20, padding=(20, 20)).pack()

    # Lautstärkeregler
    volume_slider = tk.Scale(bottom_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                             label="Lautstärke", command=logic_scroll.set_volume)
    volume_slider.set(70)
    logic_scroll.set_volume(70)
    volume_slider.pack()

    # Sound-Buttons laden
    logic_scroll.load_sounds_from_file(scrollable_frame, 'TButton')

    return window