import tkinter as tk

# Funktion, um das Programm zu beenden
def beenden():
    root.destroy()

# Hauptfenster erstellen
root = tk.Tk()
root.title("Button GUI mit while-Schleife")
# Fenstergröße auf 600x300 setzen
root.geometry("600x300")

# Anzahl der Buttons
anzahl_buttons = 5
i = 0

# Erstellen der Buttons mit einer while-Schleife
while i < anzahl_buttons:
    if i == anzahl_buttons - 1:
        # Letzter Button schließt das Programm
        btn = tk.Button(root, text=f"Button {i+1}", command=beenden)
    else:
        # Andere Buttons
        btn = tk.Button(root, text=f"Button {i+1}")
    # Buttons auf der linken Seite und untereinander anordnen
    btn.pack(side=tk.TOP, anchor='w', pady=5, padx=5)
    i += 1

# Hauptloop starten
root.mainloop()