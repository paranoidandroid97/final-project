import tkinter as tk
from tkinter import filedialog, PhotoImage
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Global state
current_song_index = 0
playlist = []
is_paused = False
current_song = None

# --- Music control functions ---
def choose_folder():
    global playlist, current_song_index
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        playlist = [os.path.join(folder_selected, f) for f in os.listdir(folder_selected) if f.endswith(".mp3")]
        playlist.sort()
        current_song_index = 0
        if playlist:
            load_song()

def load_song():
    global current_song, is_paused
    current_song = playlist[current_song_index]
    pygame.mixer.music.load(current_song)
    display_var.set(f"Loaded:\n{os.path.basename(current_song)}")
    is_paused = False

def play_pause():
    global is_paused
    if not playlist:
        return
    if is_paused:
        pygame.mixer.music.unpause()
        display_var.set(f"▶ {os.path.basename(current_song)}")
        is_paused = False
    else:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            display_var.set(f"⏸ {os.path.basename(current_song)}")
        else:
            pygame.mixer.music.play()
            display_var.set(f"▶ {os.path.basename(current_song)}")
        is_paused = not is_paused

def next_song():
    global current_song_index
    if playlist:
        current_song_index = (current_song_index + 1) % len(playlist)
        load_song()
        pygame.mixer.music.play()
        display_var.set(f"▶ {os.path.basename(current_song)}")

def prev_song():
    global current_song_index
    if playlist:
        current_song_index = (current_song_index - 1) % len(playlist)
        load_song()
        pygame.mixer.music.play()
        display_var.set(f"▶ {os.path.basename(current_song)}")

# --- GUI setup ---
root = tk.Tk()
root.title("iPod Player")
root.geometry("390x642")
root.resizable(False, False)

# Background image
bg_image = PhotoImage(file="ipod_background.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Screen area
display_var = tk.StringVar()
display_label = tk.Label(
    root,
    textvariable=display_var,
    font=("Courier", 14, "bold"),
    fg="white",
    bg="black",
    anchor="n"
)
display_label.place(x=33, y=31, width=324, height=245)
display_var.set("No song playing")

# Buttons positioned like iPod
menu_btn = tk.Button(root, text="MENU", command=choose_folder)
menu_btn.place(x=164, y=362, width=50, height=29)

prev_btn = tk.Button(root, text="⏪", command=prev_song)
prev_btn.place(x=82, y=453, width=50, height=29)

next_btn = tk.Button(root, text="⏩", command=next_song)
next_btn.place(x=245, y=453, width=50, height=29)

play_pause_btn = tk.Button(root, text="▶️⏸", command=play_pause)
play_pause_btn.place(x=164, y=545, width=50, height=29)

# Run app
root.mainloop()
