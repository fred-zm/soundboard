import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import logic

def build_gui():
    window = tk.Tk()
    window.title("Soundboard Zukunftsmotor K17")
    window.geometry("600x600")
    window.withdraw()
    window.resizable(False, False)

    # Login Window

    def on_login_close():
        window.destroy()  # Beendet das gesamte Programm

    login = tk.Toplevel(window)
    login.protocol("WM_DELETE_WINDOW", on_login_close)
    login.geometry('400x200')
    login.attributes('-topmost', 1)
    login.title('Login')
    login.grid_rowconfigure([0, 1, 2], weight=1)
    login.grid_columnconfigure([0, 1], weight=1)

    ttk.Label(login, text='Username:').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    ttk.Label(login, text="Password:").grid(row=1, column=0, sticky='e', padx=5, pady=5)

    input_username = ttk.Entry(login)
    input_username.grid(row=0, column=1, padx=5, pady=5)
    input_password = ttk.Entry(login, show='*')
    input_password.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(
        login, text='Login',
        command=lambda: logic.login_user(input_username.get(), input_password.get(), login, start)
    ).grid(row=2, column=1, pady=10)

    def start():
        window.deiconify()

        # Menüleiste
        menubar = tk.Menu(window)
        window.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)

        # Gesamtlayout (2 Zeilen: oben Inhalt, unten Steuerung)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=0)
        window.grid_columnconfigure(0, weight=1)

        # --- OBERER TEIL: Scrollbare Sound-Buttons ---
        upper_frame = ttk.Frame(window)
        upper_frame.grid(row=0, column=0, sticky='nsew')
        upper_frame.grid_rowconfigure(0, weight=1)
        upper_frame.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(upper_frame)
        scrollbar = ttk.Scrollbar(upper_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Unterer Bereich: Steuerung + Lautstärke
        lower_frame = ttk.Frame(window)
        lower_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=10)

        # Spaltenkonfiguration: 0 = links, 1 = Buttons, 2 = rechts, 3 = Abstand, 4 = Lautstärke, 5 = Spacer rechts außen
        lower_frame.grid_columnconfigure(0, weight=1)  # linker flexibler Spacer
        lower_frame.grid_columnconfigure(1, weight=0)  # Buttons
        lower_frame.grid_columnconfigure(2, weight=1)  # rechter flexibler Spacer
        lower_frame.grid_columnconfigure(3, weight=0)  # fester Abstand
        lower_frame.grid_columnconfigure(4, weight=0)  # Lautstärkeregler
        lower_frame.grid_columnconfigure(5, weight=1)  # rechter leerer Dehnbereich → ⬅️ DAS macht's sichtbar!

        # Steuerbuttons (zentriert)
        button_frame = ttk.Frame(lower_frame)
        button_frame.grid(row=0, column=1)
        ttk.Button(button_frame, text="  ▶️", command=logic.play_sound, width=4).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="⏹️", command=logic.stop_sound, width=4).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text=" 🗑️", command=lambda: logic.remove_selected_sound(scrollable_frame), width=4).grid(row=0, column=2, padx=5)

        # Lautstärkeregler (rechts außen in Spalte 4)
        right_frame = ttk.Frame(lower_frame)
        right_frame.grid(row=0, column=4, sticky="e")

        volume_slider = tk.Scale(
            right_frame, from_=0, to=100, orient=tk.HORIZONTAL,
            label="Lautstärke", command=logic.set_volume, length=150
        )
        volume_slider.set(70)
        logic.set_volume(70)
        volume_slider.pack()

        # Logo rechts außen (Spalte 5)
        logo_frame = ttk.Frame(lower_frame)
        logo_frame.grid(row=0, column=5, sticky="w", padx=(50, 10))

        # Bild laden und skalieren
        try:
            logo_image = Image.open("zlogo.png")  # Bilddateiname hier anpassen
            logo_image = logo_image.resize((40, 40))  # Größe anpassen
            logo_photo = ImageTk.PhotoImage(logo_image)

            logo_label = ttk.Label(logo_frame, image=logo_photo)
            logo_label.image = logo_photo  # Referenz speichern, sonst wird es gelöscht
            logo_label.pack()
        except Exception as e:
            print(f"Fehler beim Laden des Logos: {e}")

        # Menüfunktionen
        file_menu.add_command(
            label="🎵 Sound hinzufügen",
            command=lambda: logic.add_sound(scrollable_frame, 'TButton')
        )
        file_menu.add_separator()
        file_menu.add_command(label="❌ Beenden", command=lambda: logic.quit_program(window))

        # Styles
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10), width=15, padding=(10, 10))
        style.configure('Selected.TButton', font=('Arial', 10, 'bold'), background='#aee', width=15, padding=(10, 10))

        # Soundbuttons laden
        logic.load_sounds_for_user(scrollable_frame, 'TButton')

    return window