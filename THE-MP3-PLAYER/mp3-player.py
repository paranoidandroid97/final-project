import tkinter as tk
from tkinter import filedialog
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

current_song_index = 0
playlist = []
is_paused = False

def choose_folder():
    global playlist, current_song_index
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        playlist = [os.path.join(folder_selected, f) for f in os.listdir(folder_selected) if f.endswith(".mp3")]
        current_song_index = 0
        if playlist:
            play_song()

def play_song():
    global is_paused
    is_paused = False
    pygame.mixer.music.load(playlist[current_song_index])
    pygame.mixer.music.play()
    update_display()

def toggle_play_pause():
    global is_paused
    if not playlist:
        return
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
    else:
        pygame.mixer.music.pause()
        is_paused = True
    update_display()

def next_song():
    global current_song_index
    if playlist:
        current_song_index = (current_song_index + 1) % len(playlist)
        play_song()

def prev_song():
    global current_song_index
    if playlist:
        current_song_index = (current_song_index - 1) % len(playlist)
        play_song()

def update_display():
    if playlist:
        song_name = os.path.basename(playlist[current_song_index])
        if is_paused:
            display_var.set(f"⏸ {song_name}")
        else:
            display_var.set(f"▶ {song_name}")
    else:
        display_var.set("No song playing")

# Create main window
root = tk.Tk()
root.title("iPod MP3 Player")
root.configure(bg="black")

# Screen
display_var = tk.StringVar()
display_label = tk.Label(root, textvariable=display_var, width=30, height=4,
                         bg="lightgrey", fg="white", font=("Courier", 14), relief="sunken", anchor="center")
display_label.grid(row=0, column=0, columnspan=3, pady=10)
update_display()

# Buttons — arranged in iPod wheel layout
btn_style = {"width": 6, "height": 2, "bg": "white", "fg": "black", "font": ("Arial", 12)}

# Top (Choose Folder / Menu)
choose_btn = tk.Button(root, text="Choose\nFolder", command=choose_folder, **btn_style)
choose_btn.grid(row=1, column=1, pady=5)

# Left (Previous)
prev_btn = tk.Button(root, text="⏮", command=prev_song, **btn_style)
prev_btn.grid(row=2, column=0, padx=5)

# Right (Next)
next_btn = tk.Button(root, text="⏭", command=next_song, **btn_style)
next_btn.grid(row=2, column=2, padx=5)

# Bottom (Play/Pause)
play_pause_btn = tk.Button(root, text="▶ / ⏸", command=toggle_play_pause, **btn_style)
play_pause_btn.grid(row=3, column=1, pady=5)

# Center empty space to simulate wheel feel
root.grid_rowconfigure(2, minsize=70)
root.grid_columnconfigure(1, minsize=100)

# coming soon: choosing song from tracklist on screen; better screen size/layout; background so it looks like an iPod etc.

root.mainloop()
