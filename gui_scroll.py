import tkinter as tk
from tkinter import ttk
import logic_scroll


def build_gui():
    is_logged_in = False

    window = tk.Tk()
    window.title("Soundboard Zukunftsmotor K17")
    window.geometry("1000x600")
    # window.attributes('-disabled', True)

    # Loginwindow

    login = tk.Toplevel(window)
    login.geometry('400x200')
    login.attributes('-topmost', 1)
    login.title('Login')
    login.grid_rowconfigure(0, weight=1)
    login.grid_rowconfigure(1, weight=1)
    login.grid_rowconfigure(2, weight=1)
    login.grid_columnconfigure(0, weight=0)
    login.grid_columnconfigure(1, weight=1)

    # Loginwidgets

    username = ttk.Label(login, text='Username:')
    username.grid(row=0, column=0)
    password = ttk.Label(login, text="Password:")
    password.grid(row=1, column=0)

    input_username = ttk.Entry(login)
    input_username.grid(row=0, column=1)
    input_password = ttk.Entry(login)
    input_password.grid(row=1, column=1)

    submit_button = ttk.Button(login, text='Login', command=lambda: logic_scroll.login(login))
    submit_button.grid(row=2, column=1)

    if is_logged_in:

        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(0, weight=1)

        # Menüleiste
        menubar = tk.Menu(window)
        window.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)

        # Frames für Layout
        top_frame = ttk.Frame(window)

        top_frame.grid(row=0, column=0, sticky="nsew")
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(0, weight=1)

        bottom_frame = ttk.Frame(window)
        bottom_frame.grid(row=1, column=0, sticky="nsew")
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=0)
        bottom_frame.grid_columnconfigure(1, weight=0)
        bottom_frame.grid_columnconfigure(2, weight=1)
        bottom_frame.grid_columnconfigure(3, weight=0)

        # Scrollbarer Bereich für Sound-Buttons (links)

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

        # Menüfunktionen
        file_menu.add_command(
            label="🎵 Sound hinzufügen",
            command=lambda: logic_scroll.add_sound(scrollable_frame, "TButton"),
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="❌ Beenden", command=lambda: logic_scroll.quit_program(window)
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

        # Soundsteuerung (rechter Bereich)
        ttk.Button(bottom_frame, text="▶️ abspielen", command=logic_scroll.play_sound).grid(
            row=0, column=0
        )
        ttk.Button(bottom_frame, text="⏹️ stoppen", command=logic_scroll.stop_sound).grid(
            row=0, column=1
        )
        ttk.Button(
            bottom_frame,
            text="🗑️ Sound entfernen",
            command=lambda: logic_scroll.remove_selected_sound(scrollable_frame),
        ).grid(row=0, column=3)

        # Lautstärkeregler
        volume_slider = tk.Scale(
            bottom_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            label="Lautstärke",
            command=logic_scroll.set_volume,
        )
        volume_slider.set(70)
        logic_scroll.set_volume(70)
        volume_slider.grid(row=0, column=2, sticky="ew")

        # Sound-Buttons laden
        logic_scroll.load_sounds_from_file(scrollable_frame, "TButton")

    return window
