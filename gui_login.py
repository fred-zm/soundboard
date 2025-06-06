import tkinter as tk
from tkinter import ttk
import logic_login

def build_gui():
    window = tk.Tk()
    window.title("Soundboard Zukunftsmotor K17")
    window.geometry("1000x600")
    window.withdraw()

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

    submit_button = ttk.Button(login, text='Login', command=lambda: logic_login.login_user(input_username.get(), input_password.get(), login, start))
    submit_button.grid(row=2, column=1)

    def start():
        window.deiconify()
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
        top_frame.pack(side='top', padx=5, pady=5)

        bottom_frame = ttk.Frame(window)
        bottom_frame.pack(side='bottom', fill='x', padx=5, pady=5)

        # Subframes für links, mitte, rechts im unteren Bereich
        left_spacer = ttk.Frame(bottom_frame)
        left_spacer.pack(side='left', expand=True, fill='both')

        button_frame = ttk.Frame(bottom_frame)
        button_frame.pack(side='left')

        right_spacer = ttk.Frame(bottom_frame)
        right_spacer.pack(side='left', expand=True, fill='both')

        # ⬇️ ZUERST den rechten Abstand platzieren
        right_padding = ttk.Frame(bottom_frame, width=40)
        right_padding.pack(side='right', fill='y')

        # ⬇️ DANN den Lautstärkeregler (damit er links vom Abstand sitzt)
        right_frame = ttk.Frame(bottom_frame)
        right_frame.pack(side='right')

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
        file_menu.add_command(
            label="🎵 Sound hinzufügen",
            command=lambda: logic_login.add_sound(scrollable_frame, 'TButton')
        )
        file_menu.add_separator()
        file_menu.add_command(label="❌ Beenden", command=lambda: logic_login.quit_program(window))

        # Styles
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10), width=15, padding=(10, 10))
        style.configure('Selected.TButton', font=('Arial', 10, 'bold'), background='#aee', width=15, padding=(10, 10))

        # Steuerbuttons (zentriert)
        ttk.Button(button_frame, text="  ▶️", command=logic_login.play_sound, width=4).pack(side='left', padx=10)
        ttk.Button(button_frame, text="⏹️", command=logic_login.stop_sound, width=4).pack(side='left', padx=10)
        ttk.Button(button_frame, text=" 🗑️", command=lambda: logic_login.remove_selected_sound(scrollable_frame), width=4).pack(side='left', padx=10)

        # Lautstärkeregler (rechts außen)
        volume_slider = tk.Scale(
            right_frame, from_=0, to=100, orient=tk.HORIZONTAL,
            label="Lautstärke", command=logic_login.set_volume, length=150
        )
        volume_slider.set(70)
        logic_login.set_volume(70)
        volume_slider.pack()

        # Sound-Buttons laden
        logic_login.load_sounds_for_user(scrollable_frame, 'TButton')

    return window