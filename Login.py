import tkinter as tk
from tkinter import ttk, messagebox
from lib.functions import center_window


class Login(tk.Tk):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.width = 400
        self.height = 200

        self.title("Login")
        self.resizable(False, False)

        # GUI
        self.grid_rowconfigure([0, 1, 2], weight=1)
        self.grid_columnconfigure([0, 1], weight=1)

        ttk.Label(self, text="Username:").grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        ttk.Label(self, text="Password:").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )

        self.input_username = ttk.Entry(self)
        self.input_username.grid(row=0, column=1, padx=5, pady=5)
        self.input_password = ttk.Entry(self, show="*")
        self.input_password.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(
            self,
            text="Login",
            command=lambda: self.login_user(
                self.input_username.get(), self.input_password.get()
            ),
        ).grid(row=2, column=1, pady=10)

        self.bind(
            "<Return>",
            lambda e: self.login_user(
                self.input_username.get(), self.input_password.get()
            ),
        )
        self.input_username.focus()

        # from AI
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.transient()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.quit()

    def login_user(self, username, password):
        user = self.model.get_users(username)

        if "id" in user and user["password"] == password:
            self.model.current_user["name"] = user["username"]
            self.model.current_user["id"] = user["id"]
            self.model.authenticated = True
            self.destroy()
        else:
            messagebox.showerror(
                "Login fehlgeschlagen", "Falscher Benutzername oder Passwort."
            )

    def run(self):
        center_window(self, self.width, self.height)
        self.mainloop()
