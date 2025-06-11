# gui_elements.py
import tkinter as tk
from tkinter import ttk, filedialog as fd
from tkinter.messagebox import showinfo
import threading
import time
import os
import pygame
from src.sound_manager import SoundManager
from PIL import Image, ImageTk
from src.user_db import check_user, add_user

btn_labels = ['Sound_01', 'Sound_02', 'Sound_03', 'Sound_04', 'Sound_05',
              'Sound_06', 'Sound_07', 'Sound_08', 'Sound_09', 'Sound_10',
              'Sound_11', 'Sound_12', 'Sound_13', 'Sound_14', 'Sound_15']

# GUI Setup-Funktionen
def create_main_interface(fenster, canvas, sound_manager):
    """
    Erstellt die Hauptoberfläche des Soundboards.
    Diese Funktion richtet die Benutzeroberfläche ein, einschließlich der Buttons für Sounds,
    Lautstärkeregler, Loop-Checkbox und andere Steuerelemente.
    :param fenster: Das Hauptfenster der Anwendung.
    :param canvas: Das Canvas-Widget, auf dem die Benutzeroberfläche gezeichnet wird.
    :param sound_manager: Eine Instanz des SoundManager, die für das Abspielen und Verwalten von Sounds zuständig ist.
    """
    BG_COLOR = "#f0f0f0"
    BTN_COLOR = "#f59506"

    # Hintergrundbild laden und auf Canvas zeichnen
    bg_image = Image.open("assets/bar/berserk.jpg").resize((600, 700), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.bg_photo = bg_photo  # Referenz speichern!
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Info-Text
    info_label = ttk.Label(
        canvas,
        text="Linksklick: Sound abspielen   |   Rechtsklick: Sound zuweisen",
        foreground="gray",
        background="#ffffff"
    )
    canvas.create_window(300, 30, window=info_label)

    # Style anpassen
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', padding=6, relief='flat', background=BTN_COLOR,
                    foreground="black", borderwidth=0, focusthickness=0, focuscolor='none')
    style.map('TButton', background=[('active', "#e73313"), ('pressed', "#e73313")])
    style.configure("BG.TFrame", background=BG_COLOR)
    style.configure("Custom.TCheckbutton", background=BG_COLOR)

    # Sound Buttons
    sound_button_frame = ttk.Frame(canvas, style="BG.TFrame")
    canvas.create_window(300, 100, window=sound_button_frame)

    for idx, name in enumerate(btn_labels):
        row = idx // 5
        col = idx % 5
        btn = ttk.Button(sound_button_frame, text=name, style='TButton')
        btn.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
        btn.config(command=lambda name=name: sound_manager.play_sound(name))
        btn.bind("<Button-3>", lambda event, name=name: assign_sound_file(name, sound_manager))

    # Lautstärkeregler
    lautstaerke_label = ttk.Label(canvas, text="Lautstärke", background=BG_COLOR)
    canvas.create_window(300, 180, window=lautstaerke_label)

    lautstaerke_frame = ttk.Frame(canvas, style="BG.TFrame")
    canvas.create_window(300, 210, window=lautstaerke_frame)

    lautstaerke_wert_label = ttk.Label(canvas, text="50 %", background=BG_COLOR)
    canvas.create_window(300, 240, window=lautstaerke_wert_label)

    def lautstaerke_setzen(val):
        """
        Setzt die Lautstärke des SoundManagers basierend auf dem Reglerwert.
        :param val: Der aktuelle Wert des Lautstärkereglers (String).
        """
        volume = float(val) / 100
        sound_manager.set_volume(volume)
        lautstaerke_wert_label.config(text=f"{int(float(val))} %")

    lautstaerke_regler = ttk.Scale(
        lautstaerke_frame, from_=0, to=100, orient='horizontal',
        command=lautstaerke_setzen
    )
    lautstaerke_regler.set(50)
    lautstaerke_regler.pack(fill='x', expand=True)

    # Loop Checkbox
    loop_var = tk.BooleanVar(value=False)

    def loop_changed():
        """
        Callback-Funktion, die aufgerufen wird, wenn die Loop-Checkbox geändert wird.
        Setzt den Loop-Modus im SoundManager basierend auf dem aktuellen Wert der Checkbox.
        """
        sound_manager.set_loop(loop_var.get())

    loop_checkbox = ttk.Checkbutton(
        canvas, text="Loop (Sound wiederholen)", variable=loop_var,
        command=loop_changed, style="Custom.TCheckbutton"
    )
    canvas.create_window(300, 270, window=loop_checkbox)

    # Untere Buttons
    button_frame = ttk.Frame(canvas, style="BG.TFrame")
    canvas.create_window(300, 650, window=button_frame)

    ttk.Button(
        button_frame, text='Alle abspielen',
        command=lambda: sound_manager.play_all_sounds(btn_labels),
        style='TButton'
    ).pack(side='left', expand=True, padx=20)

    # --- Ausloggen-Button ---
    def ausloggen():
        """
        Funktion zum Ausloggen des aktuellen Benutzers.
        Setzt den SoundManager zurück und öffnet das Login-Fenster erneut.
        """
        sound_manager.save_sounds()
        fenster.withdraw()
        show_login_window(fenster, sound_manager)

    ttk.Button(
        button_frame, text='Ausloggen',
        command=ausloggen,
        style='TButton'
    ).pack(side='left', expand=True, padx=20)

    ttk.Button(
        button_frame, text='Beenden',
        command=lambda: beenden(fenster, sound_manager),
        style='TButton'
    ).pack(side='left', expand=True, padx=20)

def assign_sound_file(name, sound_manager):
    """
    Öffnet einen Dateiauswahldialog, um eine Sounddatei für den angegebenen Button zuzuweisen.
    :param name: Der Name des Buttons, dem die Sounddatei zugewiesen werden soll.
    :param sound_manager: Eine Instanz des SoundManager, die für das Zuweisen von Sounds zuständig ist.
    """
    filetypes = (
        ('Audio Dateien', '*.mp3 *.wav'),
        ('Alle Dateien', '*.*')
    )
    filename = fd.askopenfilename(
        title=f'Sound für {name} wählen',
        initialdir='/',
        filetypes=filetypes)
    if filename:
        sound_manager.assign_sound(name, filename)
        showinfo("Zugewiesen", f"{name} spielt jetzt:\n{os.path.basename(filename)}")

def beenden(fenster, sound_manager):
    """
    Beendet die Anwendung, speichert die Soundeinstellungen und schließt das Fenster.
    :param fenster: Das Hauptfenster der Anwendung.
    :param sound_manager: Eine Instanz des SoundManager, die für das Verwalten von Sounds zuständig ist.
    """
    sound_manager.quit()
    fenster.quit()



def show_login_window(fenster, sound_manager):
    """
    Zeigt das Login-Fenster an, in dem der Benutzer sich anmelden oder registrieren kann.
    :param fenster: Das Hauptfenster der Anwendung, das im Hintergrund bleibt, während das Login-Fenster aktiv ist.
    :param sound_manager: Eine Instanz des SoundManager, die für das Abspielen von Sounds im Login-Fenster zuständig ist.
    """
    login_win = tk.Toplevel()
    login_win.title("Login")
    login_win.geometry("300x150")
    login_win.resizable(False, False)
    login_win.grab_set()

    # Spalten gleichmäßig verteilen
    login_win.grid_columnconfigure(0, weight=1)
    login_win.grid_columnconfigure(1, weight=1)

    try:
        pygame.mixer.music.load("assets/bar/funny-bgm-240795.mp3")
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Login-Musik konnte nicht geladen werden: {e}")

    ttk.Label(login_win, text="Benutzername:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    username_entry = ttk.Entry(login_win)
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    ttk.Label(login_win, text="Passwort:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    password_entry = ttk.Entry(login_win, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def check_login():
        """
        Überprüft die Anmeldedaten des Benutzers.
        Wenn die Anmeldedaten korrekt sind, wird das Login-Fenster geschlossen und das Hauptfenster angezeigt.
        Wenn die Anmeldedaten falsch sind, wird eine Fehlermeldung angezeigt und die Login-Musik wird neu gestartet.
        """
        username = username_entry.get()
        password = password_entry.get()
        if check_user(username, password):
            pygame.mixer.music.stop()
            login_win.destroy()
            fenster.deiconify()
            sound_manager.set_user(username)  # <--- Benutzer setzen!
        else:
            try:
                pygame.mixer.music.load("assets/bar/Mario.mp3")
                pygame.mixer.music.play()
                def restart_login_music():
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    try:
                        pygame.mixer.music.load("assets/bar/funny-bgm-240795.mp3")
                        pygame.mixer.music.play(-1)
                    except Exception as e:
                        print(f"Fehler beim Wiederholen der Musik: {e}")
                threading.Thread(target=restart_login_music, daemon=True).start()
            except Exception as e:
                print(f"Fehler beim Fehler-Sound: {e}")
            ttk.Label(login_win, text="Login fehlgeschlagen!", foreground="red").grid(row=3, column=0, columnspan=2)

    password_entry.bind("<Return>", lambda event: check_login())


    # --- Registrierungsfenster ---
    def open_register_window():
        """
        Öffnet ein neues Fenster zur Registrierung eines neuen Benutzers.
        In diesem Fenster kann der Benutzer einen neuen Benutzernamen und ein Passwort eingeben.
        Wenn der Benutzer erfolgreich registriert wird, wird ein neuer Ordner für den Benutzer im "sounds"-Verzeichnis erstellt.
        """
        reg_win = tk.Toplevel(login_win)
        reg_win.title("Neuer Benutzer")
        reg_win.geometry("300x150")
        reg_win.resizable(False, False)
        reg_win.grid_columnconfigure(0, weight=1)
        reg_win.grid_columnconfigure(1, weight=1)

        ttk.Label(reg_win, text="Benutzername:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        new_user_entry = ttk.Entry(reg_win)
        new_user_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(reg_win, text="Passwort:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        new_pass_entry = ttk.Entry(reg_win, show="*")
        new_pass_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        status_label = ttk.Label(reg_win, text="")
        status_label.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        def register_user():
            """
            Registriert einen neuen Benutzer mit dem eingegebenen Benutzernamen und Passwort.
            Wenn der Benutzer erfolgreich registriert wird, wird ein neuer Ordner für den Benutzer im "sounds"-Verzeichnis erstellt.
            Wenn der Benutzername bereits existiert, wird eine Fehlermeldung angezeigt.
            """
            username = new_user_entry.get()
            password = new_pass_entry.get()
            if add_user(username, password):
                user_folder = os.path.join("sounds", username)
                os.makedirs(user_folder, exist_ok=True)
                status_label.config(text="Benutzer angelegt!", foreground="green")
            else:
                status_label.config(text="Fehler: Name existiert!", foreground="red")

        # Button-Frame für Anlegen und Schließen nebeneinander
        button_row = ttk.Frame(reg_win)
        button_row.grid(row=4, column=0, columnspan=2, pady=10)
        button_row.grid_columnconfigure(0, weight=1)
        button_row.grid_columnconfigure(1, weight=1)

        anlegen_btn = ttk.Button(button_row, text="Anlegen", command=register_user)
        anlegen_btn.grid(row=0, column=0, padx=10, sticky="ew")

        schliessen_btn = ttk.Button(button_row, text="Schließen", command=reg_win.destroy)
        schliessen_btn.grid(row=0, column=1, padx=10, sticky="ew")
        
    # Button-Frame für Login und Neuer Benutzer
    button_row = ttk.Frame(login_win)
    button_row.grid(row=2, column=0, columnspan=2, pady=20)
    button_row.grid_columnconfigure(0, weight=1)
    button_row.grid_columnconfigure(1, weight=1)

    login_btn = ttk.Button(button_row, text="Login", command=check_login)
    login_btn.grid(row=0, column=0, padx=10, sticky="ew")

    neuer_benutzer_btn = ttk.Button(button_row, text="Neuer Benutzer", command=open_register_window)
    neuer_benutzer_btn.grid(row=0, column=1, padx=10, sticky="ew")

    fenster.withdraw()
