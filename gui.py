import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from PIL import Image, ImageTk
import logic

def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def build_gui():
    window = tk.Tk()
    window.title("Soundboard Zukunftsmotor K17")
    window.geometry("600x600")
    window.withdraw()
    window.resizable(False, False)

    def on_login_close():
        window.destroy()

    login = tk.Toplevel(window)
    login.title('Login')
    login.protocol("WM_DELETE_WINDOW", on_login_close)
    login.attributes('-topmost', 1)
    center_window(login, 400, 200)
    login.focus_force()
    login.grab_set()

    login.grid_rowconfigure([0, 1, 2], weight=1)
    login.grid_columnconfigure([0, 1], weight=1)

    ttk.Label(login, text='Username:').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    ttk.Label(login, text="Password:").grid(row=1, column=0, sticky='e', padx=5, pady=5)

    input_username = ttk.Entry(login)
    input_username.grid(row=0, column=1, padx=5, pady=5)
    input_password = ttk.Entry(login, show='*')
    input_password.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(login, text='Login', command=lambda: logic.login_user(input_username.get(), input_password.get(), login, start)).grid(row=2, column=1, pady=10)
    ttk.Button(login, text='Erstellen', command=lambda: open_create_user_dialog(login)).grid(row=2, column=0, pady=10)

    input_username.focus_set()

    login.bind("<Return>", lambda event: logic.login_user(input_username.get(), input_password.get(), login, start))

    def open_create_user_dialog(parent):
        dialog = tk.Toplevel(parent)
        dialog.title("Benutzer erstellen")
        dialog.transient(parent)
        dialog.grab_set()
        center_window(dialog, 300, 150)
        dialog.focus_force()

        ttk.Label(dialog, text="Neuer Benutzername:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        username_entry = ttk.Entry(dialog)
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(dialog, text="Passwort:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        def create_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if logic.create_user(username, password):
                dialog.destroy()
            else:
                mb.showerror("Fehler", "Benutzername existiert bereits oder Eingabe ist ungültig.")

        ttk.Button(dialog, text="Erstellen", command=create_user).grid(row=2, column=1, pady=10, sticky="e")

        dialog.bind("<Return>", lambda event: create_user())

        username_entry.focus_set()

    def start():
        window.deiconify()

        menubar = tk.Menu(window)
        window.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)

        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=0)
        window.grid_columnconfigure(0, weight=1)

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

        lower_frame = ttk.Frame(window)
        lower_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=10)

        lower_frame.grid_columnconfigure(0, weight=1)
        lower_frame.grid_columnconfigure(1, weight=0)
        lower_frame.grid_columnconfigure(2, weight=1)
        lower_frame.grid_columnconfigure(3, weight=0)
        lower_frame.grid_columnconfigure(4, weight=0)
        lower_frame.grid_columnconfigure(5, weight=1)

        button_frame = ttk.Frame(lower_frame)
        button_frame.grid(row=0, column=1)
        ttk.Button(button_frame, text="  ▶️", command=logic.play_sound, width=4).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="⏹️", command=logic.stop_sound, width=4).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text=" 🗑️", command=lambda: logic.remove_selected_sound(scrollable_frame), width=4).grid(row=0, column=2, padx=5)

        right_frame = ttk.Frame(lower_frame)
        right_frame.grid(row=0, column=4, sticky="e")

        volume_slider = tk.Scale(
            right_frame, from_=0, to=100, orient=tk.HORIZONTAL,
            label="Lautstärke", command=logic.set_volume, length=150
        )
        volume_slider.set(70)
        logic.set_volume(70)
        volume_slider.pack()

        logo_frame = ttk.Frame(lower_frame)
        logo_frame.grid(row=0, column=5, sticky="w", padx=(50, 10))

        try:
            logo_image = Image.open("zlogo.png")
            logo_image = logo_image.resize((40, 40))
            logo_photo = ImageTk.PhotoImage(logo_image)

            logo_label = ttk.Label(logo_frame, image=logo_photo)
            logo_label.image = logo_photo
            logo_label.pack()
        except Exception as e:
            print(f"Fehler beim Laden des Logos: {e}")

        file_menu.add_command(
            label="🎵 Sound hinzufügen",
            command=lambda: logic.add_sound(scrollable_frame, 'TButton')
        )
        file_menu.add_separator()
        file_menu.add_command(label="❌ Beenden", command=lambda: logic.quit_program(window))

        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10), width=15, padding=(10, 10))
        style.configure('Selected.TButton', font=('Arial', 10, 'bold'), background='#aee', width=15, padding=(10, 10))

        logic.load_sounds_for_user(scrollable_frame, 'TButton')

    return window