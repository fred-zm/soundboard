import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from style import init_style
from components.State import State
from lib.functions import center_window
from PIL import Image, ImageTk
import io, os, pygame


class App(tk.Tk):
    def __init__(self, model, master=None):
        super().__init__(master)
        self.model = model

        self.width = 600
        self.height = 600
        self.withdraw()

        self.title("Soundboard Zukunftsmotor K17")
        self.iconbitmap(r"./favicon.ico")
        self.sound_buttons = []
        self.selected_sound = None

        # self.value = tk.IntVar(value=0)

        init_style()
        pygame.mixer.init()

        # Menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Datei", menu=self.file_menu)

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Upper area
        self.upper_frame = ttk.Frame(self)
        self.upper_frame.grid(row=0, column=0, sticky="nsew")
        self.upper_frame.grid_rowconfigure(0, weight=1)
        self.upper_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.upper_frame)
        self.scrollbar = ttk.Scrollbar(
            self.upper_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.scrollable_frame.bind(  # MouseWheel event triggers scrollbar on canvas not just on scrollbar
            "<MouseWheel>",
            lambda event: self.canvas.yview_scroll(-1 * (event.delta // 120), "units"),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Unterer Bereich: Steuerung + Lautstärke
        self.lower_frame = ttk.Frame(self)
        self.lower_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=10)

        # Spaltenkonfiguration: 0 = links, 1 = Buttons, 2 = rechts, 3 = Abstand, 4 = Lautstärke, 5 = Spacer rechts außen
        self.lower_frame.grid_columnconfigure(0, weight=1)  # linker flexibler Spacer
        self.lower_frame.grid_columnconfigure(1, weight=0)  # Buttons
        self.lower_frame.grid_columnconfigure(2, weight=1)  # rechter flexibler Spacer
        self.lower_frame.grid_columnconfigure(3, weight=0)  # fester Abstand
        self.lower_frame.grid_columnconfigure(4, weight=0)  # Lautstärkeregler
        self.lower_frame.grid_columnconfigure(
            5, weight=1
        )  # rechter leerer Dehnbereich → ⬅️ DAS macht's sichtbar!

        # Steuerbuttons (zentriert)
        self.button_frame = ttk.Frame(self.lower_frame)
        self.button_frame.grid(row=0, column=1)
        self.play_button = ttk.Button(
            self.button_frame, text="  ▶️", command=self.play_sound, width=4
        ).grid(row=0, column=0, padx=5)
        self.stop_button = ttk.Button(
            self.button_frame, text="⏹️", command=self.stop_sound, width=4
        ).grid(row=0, column=1, padx=5)
        self.remove_button = ttk.Button(
            self.button_frame,
            text=" 🗑️",
            command=lambda: self.remove_selected_sound(self.scrollable_frame),
            width=4,
        ).grid(row=0, column=2, padx=5)

        # Lautstärkeregler (rechts außen in Spalte 4)
        self.right_frame = ttk.Frame(self.lower_frame)
        self.right_frame.grid(row=0, column=4, sticky="e")

        volume_slider = tk.Scale(
            self.right_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            label="Lautstärke",
            command=self.set_volume,
            length=150,
        )
        volume_slider.set(50)
        self.set_volume(50)
        volume_slider.pack()

        # Logo rechts außen (Spalte 5)
        self.logo_frame = ttk.Frame(self.lower_frame)
        self.logo_frame.grid(row=0, column=5, sticky="w", padx=(50, 10))

        # Bild laden und skalieren
        try:
            self.logo_image = Image.open("zlogo.png")  # Bilddateiname hier anpassen
            self.logo_image = self.logo_image.resize((40, 40))  # Größe anpassen
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)

            self.logo_label = ttk.Label(self.logo_frame, image=self.logo_photo)
            self.logo_label.image = (
                self.logo_photo
            )  # Referenz speichern, sonst wird es gelöscht
            self.logo_label.pack()
        except Exception as e:
            print(f"Fehler beim Laden des Logos: {e}")

        # Menüfunktionen
        self.file_menu.add_command(
            label="🎵 Sound hinzufügen",
            command=lambda: self.add_sound(self.scrollable_frame, "TButton"),
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="❌ Beenden", command=lambda: self.quit_program()
        )

        # Styles
        # style = ttk.Style()
        # style.configure("TButton", font=("Arial", 10), width=15, padding=(10, 10))
        # style.configure(
        #     "Selected.TButton",
        #     font=("Arial", 10, "bold"),
        #     background="#aee",
        #     width=15,
        #     padding=(10, 10),
        # )

        # Soundbuttons laden
        self.load_sounds_for_user(self.scrollable_frame, "TButton")

        # self.show_state = State(self, self)
        # self.show_state.pack(expand=True)

    def load_sounds_for_user(self, frame, style):
        if self.model.current_user["name"] is None:
            return

        sounds = self.model.load_sounds(self.model.current_user["id"])
        for (sound,) in sounds:
            self.create_sound_button(sound, frame, style)
        if False:
            try:
                with open(USER_JSON_PATH, "r", encoding="utf-8") as f:
                    users = json.load(f)
                    sound_paths = users[current_user["name"]]["sounds"]

                for path in sound_paths:
                    abs_path = os.path.join(PROJECT_DIR, path)
                    if os.path.exists(abs_path):
                        create_sound_button(abs_path, frame, style)
            except Exception as e:
                print(f"Fehler beim Laden der Sounds: {e}")

    def create_sound_button(self, sound, frame, style):
        button_text = "Sound" + str(len(self.sound_buttons))

        def select():
            for _, btn in self.sound_buttons:
                btn.config(style=style)
            new_button.config(style="Selected.TButton")
            self.selected_sound = sound

        new_button = ttk.Button(frame, text=button_text, command=select)

        # Rasterposition: nebeneinander, dann neue Zeile
        index = len(self.sound_buttons)
        columns_per_row = 4
        row = index // columns_per_row
        col = index % columns_per_row

        new_button.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        frame.grid_columnconfigure(col, weight=1)
        frame.grid_rowconfigure(row, weight=1)

        self.sound_buttons.append((sound, new_button))

    def save_sounds_for_user(self):
        if self.model.current_user["id"] is None:
            return

        self.model.save_sounds()
        if False:
            try:
                with open(USER_JSON_PATH, "r+", encoding="utf-8") as f:
                    users = json.load(f)
                    users[current_user["name"]]["sounds"] = [
                        os.path.relpath(p, PROJECT_DIR) for p, _ in sound_buttons
                    ]
                    f.seek(0)
                    json.dump(users, f, indent=4)
                    f.truncate()
            except Exception as e:
                print(f"Fehler beim Speichern der Sounds: {e}")

    def _rearrange_buttons(self, frame):
        columns_per_row = 4
        for index, (_, button) in enumerate(self.sound_buttons):
            row = index // columns_per_row
            col = index % columns_per_row
            button.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            frame.grid_columnconfigure(col, weight=1)
            frame.grid_rowconfigure(row, weight=1)

    def add_sound(self, frame, style):
        filetypes = (
            ("MP3 Dateien", "*.mp3"),
            ("WAV Dateien", "*.wav"),
            ("Alle Dateien", "*.*"),
        )

        filenames = filedialog.askopenfilenames(
            title="Sounds hinzufügen", initialdir="./sounds", filetypes=filetypes
        )

        if not filenames:
            return

        added_count = 0
        for filename in filenames:
            abs_filename = os.path.abspath(filename)

            # Duplikate prüfen (immer mit absoluten Pfaden)
            sound = self.model.add_sound(abs_filename, self.model.current_user["id"])
            if sound:
                self.create_sound_button(sound, frame, style)
                added_count += 1

        if added_count:
            messagebox.showinfo(
                title="Sounds hinzugefügt",
                message=f"{added_count} Sound(s) wurden hinzugefügt.",
            )
            self.save_sounds_for_user()
        else:
            messagebox.showinfo(
                "Hinweis", "Alle ausgewählten Sounds sind bereits vorhanden."
            )

    def remove_selected_sound(self, frame):
        if self.selected_sound is None:
            messagebox.showinfo("Hinweis", "Kein Sound ausgewählt!")
            return

        for i, (path, button) in enumerate(self.sound_buttons):
            if path == self.selected_sound:
                button.destroy()
                del self.sound_buttons[i]
                self.selected_sound = None
                self._rearrange_buttons(frame)  # Neu anordnen nach Entfernen
                self.save_sounds_for_user()
                messagebox.showinfo("Sound entfernt", "Der Sound wurde entfernt.")
                return

        messagebox.showinfo("Fehler", "Sound konnte nicht gefunden werden.")

    def play_sound(self):
        if self.selected_sound:
            try:
                sound_buffer = io.BytesIO(self.selected_sound)
                sound = pygame.mixer.Sound(sound_buffer)
                sound.play()
            except Exception as e:
                messagebox.showinfo(
                    title="Fehler", message=f"Konnte Sound nicht abspielen:\n{e}"
                )
        else:
            messagebox.showinfo(title="Hinweis", message="Kein Sound ausgewählt!")

    def stop_sound(self):
        pygame.mixer.stop()

    def set_volume(self, val):
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)

    def quit_program(self):
        pygame.mixer.quit()
        self.quit()

    def run(self):
        center_window(self, self.width, self.height)
        self.deiconify()
        self.mainloop()
