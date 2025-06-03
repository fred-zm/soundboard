from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd




#zeigt nur denn pfad der datei die konvention ist irreführend
def datei_oeffnen():
    mb.showinfo("Öffnen")
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    mb.showinfo(
        title='Selected File',
        message=filename
    )
#noch ungenutzt
def datei_speichern():
    mb.showinfo("Speichern")

#beendet das Programm 
def datei_beenden(fenster):
    fenster.quit()


#for schleife die i immer weider ersetzt mit der liste//append speichert den button für zukunft 
def buttons_erzeugen(master, texte):
    buttons = []
    for i in texte:
        button = ttk.Button(master, text=i)
        button.pack(side='top', anchor='w', padx=10, pady=5)
        buttons.append(button)
    return buttons