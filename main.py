import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk
import pygame # Import pygame

# Hauptfenster erstellen
fenster = tk.Tk()
fenster.title("Soundboard")
fenster.geometry("600x300")

# Initialize pygame mixer
pygame.mixer.init()

# Store the currently playing file for stop/pause functionality
current_playing_file = None

def play_mp3(filepath):
    """Plays the selected MP3 file."""
    global current_playing_file
    try:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        current_playing_file = filepath
        showinfo(title='Playing', message=f"Now playing: {filepath.split('/')[-1]}")
    except pygame.error as e:
        messagebox.showerror("Playback Error", f"Could not play MP3: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def stop_mp3():
    """Stops the currently playing MP3."""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        showinfo(title='Stopped', message="Playback stopped.")
    else:
        showinfo(title='Information', message="No MP3 is currently playing.")

def pause_unpause_mp3():
    """Pauses or unpauses the currently playing MP3."""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        showinfo(title='Paused', message="Playback paused.")
    elif pygame.mixer.music.get_pos() > -1: # Check if music is loaded and not playing (i.e., paused)
        pygame.mixer.music.unpause()
        showinfo(title='Unpaused', message="Playback unpaused.")
    else:
        showinfo(title='Information', message="No MP3 is currently playing to pause/unpause.")

def select_file():
    """Opens a file dialog to select an MP3 file and then plays it."""
    filetypes = (
        ('MP3 files', '*.mp3'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open an MP3 File',
        initialdir='/', # You might want to change this to a more common music directory
        filetypes=filetypes
    )

    if filename: # Only proceed if a file was selected
        play_mp3(filename)
    else:
        showinfo(title='No File Selected', message='No MP3 file was chosen.')

# Create buttons for opening, playing, stopping, and pausing
open_button = ttk.Button(
    fenster,
    text='Open & Play MP3',
    command=select_file
)
open_button.pack(pady=10)

stop_button = ttk.Button(
    fenster,
    text='Stop Playback',
    command=stop_mp3
)
stop_button.pack(pady=5)

pause_unpause_button = ttk.Button(
    fenster,
    text='Pause/Unpause',
    command=pause_unpause_mp3
)
pause_unpause_button.pack(pady=5)

# GUI starten
fenster.mainloop()

# Clean up pygame mixer when the window is closed
pygame.mixer.quit()