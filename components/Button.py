from tkinter import ttk

class Button(ttk.Button):
    def __init__(self, master, displaytext, row, column, command=None, lm="pack"):
        super().__init__(master, text=displaytext, command=command)
        
        self.padx = 5
        self.pady = 5

        # self.pack(side="left", expand=True)
        self.grid(row=row, column=column, padx=self.padx, pady=self.pady)
