# soundboard/main.py
import tkinter as tk
from gui import SoundboardApp

def main():
    root = tk.Tk()
    app = SoundboardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
