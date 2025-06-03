import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from lib.functions import open_file, save_file, close_window
from components.Button import Button


# Subklasse App mit vererbten Daten von Klasse Tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Soundboard")
        self.geometry("600x300")

        # Menu

        self.open_button = Button(
            master=self, displaytext="Open a File", command=open_file, row=0, column=1
        )
        self.play_button = Button(master=self, displaytext="Play", row=0, column=2)
        self.end_button = Button(
            master=self,
            displaytext="Quit",
            command=lambda: close_window(self),
            row=0,
            column=0,
        )
        # Songbuttons

        button_list = []
        button_names = [f"song {i}" for i in range(0, 5)]

        for i, name in enumerate(button_names):
            button = Button(master=self, displaytext=name, row=i + 1, column=0)
            button_list.append(button)

    def run(self):
        self.mainloop()
