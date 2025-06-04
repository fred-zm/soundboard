from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showinfo as mb_info

# Öffnen der Datei

def datei_oeffnen():
    filetypes = (
        ('Textdateien', '*.txt'),
        ('Alle Dateien', '*.*')
    )

    filename = fd.askopenfilename(
        title='Datei öffnen',
        initialdir='/',
        filetypes=filetypes
    )

    if filename:
        showinfo(title='Ausgewählte Datei', message=filename)

# Speichern der Datei

def datei_speichern():
    mb_info("Speichern")

# Beenden der Datei

def datei_beenden(root):
    root.quit()