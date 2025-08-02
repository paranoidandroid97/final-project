import tkinter as tk
from tkinter import filedialog, PhotoImage
import pygame
import os

# This sets up the main window
root = tk.Tk()
root.title("MP3 Player")
root.geometry("275x400")

# Init pygame mixer
pygame.mixer.init()

songs = []
current_index = 0
is_paused = False  # Track whether playback is paused

# Display current song title
current_song_label = tk.Label(root, text="No song playing", font=("Courier", 10))
current_song_label.pack()

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        os.chdir(folder)
        for file in sorted(os.listdir()):
            if file.endswith(".mp3"):
                songs.append(file)
        if songs:
            current_song_label.config(text=f"Ready: {songs[current_index].replace('.mp3', '')}")

def play():
    global is_paused
    if songs:
        if is_paused:
            pygame.mixer.music.unpause()
            is_paused = False
        else:
            pygame.mixer.music.load(songs[current_index])
            pygame.mixer.music.play()
            current_song_label.config(text=f"Playing: {songs[current_index].replace('.mp3', '')}")

def stop():
    global is_paused
    pygame.mixer.music.pause()
    is_paused = True

def next_song():
    global current_index, is_paused
    if songs:
        current_index = (current_index + 1) % len(songs)
        pygame.mixer.music.load(songs[current_index])
        pygame.mixer.music.play()
        current_song_label.config(text=f"Playing: {songs[current_index].replace('.mp3', '')}")
        is_paused = False

def previous_song():
    global current_index, is_paused
    if songs:
        current_index = (current_index - 1) % len(songs)
        pygame.mixer.music.load(songs[current_index])
        pygame.mixer.music.play()
        current_song_label.config(text=f"Playing: {songs[current_index].replace('.mp3', '')}")
        is_paused = False

# Buttons
btn_choose = tk.Button(root, text="Choose Folder", command=choose_folder)
btn_choose.pack(pady=20)

btn_play = tk.Button(root, text="Play", command=play)
btn_play.pack(pady=10)

btn_stop = tk.Button(root, text="Stop", command=stop)
btn_stop.pack(pady=10)

btn_prev = tk.Button(root, text="⏮ Previous", command=previous_song)
btn_prev.pack(pady=5)

btn_next = tk.Button(root, text="Next ⏭", command=next_song)
btn_next.pack(pady=5)

# Run the app
root.mainloop()
