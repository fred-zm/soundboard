import tkinter as tk
from tkinter import ttk
import logic


class Gui:
    def login(self):
        self.login_window = tk.Tk()
        self.login_window.mainloop()

    def run(self):
        #Main Window
        self.window = tk.Tk()
        self.window.title("Soundboard Zukunftsmotor K17")
        self.window.geometry("1000x600")

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)


        # Menüleiste
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)

        # Menüfunktionen
        file_menu.add_command(
            label="🎵 Sound hinzufügen",
            command=lambda: logic.add_sound(scrollable_frame, "TButton"),
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="❌ Beenden", command=lambda: logic.quit_program(self.window)
        )


        # Frames für Layout
        top_frame = ttk.Frame(self.window)

        top_frame.grid(row=0, column=0, sticky="nsew")
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(0, weight=1)

        bottom_frame = ttk.Frame(self.window)
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


        self.window.mainloop()
