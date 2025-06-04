from tkinter import ttk

# Button erstellen, Text geben, Gui-Container hinzufügen und Speichern

def create_sound_buttons(parent, texts):
    buttons = []
    for text in texts:
        button = ttk.Button(parent, text=text)
        button.pack(anchor='w', padx=10, pady=2)
        buttons.append(button)
    return buttons