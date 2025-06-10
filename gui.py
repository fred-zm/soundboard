import tkinter as tk
from tkinter import ttk
import logic


def create_login_frame(gui):
    login_frame = ttk.Frame(gui.root)
    login_frame.grid_rowconfigure(0, weight=1)
    login_frame.grid_rowconfigure(1, weight=1)
    login_frame.grid_rowconfigure(2, weight=1)
    login_frame.grid_columnconfigure(0, weight=1)
    login_frame.grid_columnconfigure(1, weight=2)

    benutzer = tk.StringVar()
    ttk.Label(login_frame, text="Benutzer:", font="30").grid(column=0, row=0, sticky="es")
    ttk.Entry(login_frame, textvariable=benutzer).grid(column=1, row=0, sticky="ws")
    passwort = tk.StringVar()
    ttk.Label(login_frame, text="Passwort:", font="30").grid(column=0, row=1, sticky="en")
    ttk.Entry(login_frame, textvariable=passwort).grid(column=1, row=1, sticky="nw")
    ttk.Button(login_frame, text="Login", command=lambda: logic.login(gui.open_soundboard, benutzer.get(), passwort.get())).grid(column=1, row=2, sticky="e")

    for widget in login_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)
    return login_frame

def create_soundboard_frame(gui):
    #Main Window
    soundboard_frame = tk.Frame(gui.root)
    soundboard_frame.grid_rowconfigure(0, weight=1)
    soundboard_frame.grid_rowconfigure(1, weight=1)
    soundboard_frame.grid_columnconfigure(0, weight=1)

    # Menüleiste
    menubar = tk.Menu(soundboard_frame)
    gui.root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Datei", menu=file_menu)

    # Menüfunktionen
    file_menu.add_command(
        label="🎵 Sound hinzufügen",
        command=lambda: logic.add_sound(scrollable_frame, "TButton"),
    )
    file_menu.add_separator()
    file_menu.add_command(
        label="❌ Beenden", command=lambda: logic.quit_program(soundboard_frame)
    )


    # Frames für Layout
    top_frame = ttk.Frame(soundboard_frame)

    top_frame.grid(row=0, column=0, sticky="nsew")
    top_frame.grid_rowconfigure(0, weight=1)
    top_frame.grid_columnconfigure(0, weight=1)

    bottom_frame = ttk.Frame(soundboard_frame)
    bottom_frame.grid(row=1, column=0, sticky="nsew")
    bottom_frame.grid_rowconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(0, weight=0)
    bottom_frame.grid_columnconfigure(1, weight=0)
    bottom_frame.grid_columnconfigure(2, weight=1)
    bottom_frame.grid_columnconfigure(3, weight=0)

    # Scrollbarer Bereich für Sound-Buttons (top_frame)

    canvas = tk.Canvas(top_frame)
    scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="nsew")

    canvas.bind_all(  # MouseWheel event triggers scrollbar on canvas not just on scrollbar
        "<MouseWheel>",
        lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"),
    )


    # Styles
    style = ttk.Style()

    style.configure("TButton", font=("Arial", 10))
    style.configure(
        "Selected.TButton",
        font=("Arial", 10, "bold"),
        background="#aee",
        padding=(20, 20),
    )

    # Soundsteuerung (bottom_frame)
    ttk.Button(bottom_frame, text="▶️ abspielen", command=logic.play_sound).grid(
        row=0, column=0
    )
    ttk.Button(bottom_frame, text="⏹️ stoppen", command=logic.stop_sound).grid(
        row=0, column=1
    )
    ttk.Button(
        bottom_frame,
        text="🗑️ Sound entfernen",
        command=lambda: logic.remove_selected_sound(scrollable_frame),
    ).grid(row=0, column=3)

    # Lautstärkeregler
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
    volume_slider.grid(row=0, column=2, sticky="ew")

    # Sound-Buttons laden
    logic.load_sounds_from_file(canvas, "TButton")
    return soundboard_frame


class Gui:
    def __init__(self):
        self.is_logged_in = False
        self.quited = False
        self.root = tk.Tk()
        self.root.title("Soundboard Zukunftsmotor K17")
        self.root.geometry("1000x600")
        self.login_frame = create_login_frame(self)
        self.soundboard_frame = create_soundboard_frame(self)

    def run(self):
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_rowconfigure(0,weight=1)
        self.login_frame.grid()
        self.root.mainloop()

    def open_soundboard(self):
        self.login_frame.destroy()
        self.soundboard_frame.grid(sticky='nswe')