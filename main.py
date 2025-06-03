import tkinter as tk


# Hauptfenster erstellen
fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")

testbutton = tk.Button(text="test")
testbutton.grid(column=1, row=1)

# GUI starten
fenster.mainloop()