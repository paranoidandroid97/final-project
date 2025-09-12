import tkinter as tk
from tkinter import filedialog
import pygame
import os
import time

# === boot ===
pygame.mixer.init()

# === globals (state of the player) ===
current_song_index = 0
playlist = []
is_paused = False
current_song = None
folder_queue = []
current_folder_index = 0
song_start_time = None
song_elapsed = 0.0
song_length = 0.0

_bg_image = None
_cover_img = None
_topbar_img = None

# === songs / folders ===
def choose_folder():
    # Pick a folder with either mp3s directly or subfolders of albums

    global folder_queue, current_folder_index
    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        return

    # if mp3s are directly inside -> treat as 1 album
    direct_mp3s = [f for f in os.listdir(folder_selected) if f.lower().endswith(".mp3")]
    if direct_mp3s:
        folder_queue = [folder_selected]
    else:
        # otherwise queue up subfolders that contain mp3s
        folder_queue = []
        for d in sorted(os.listdir(folder_selected)):
            full_path = os.path.join(folder_selected, d)
            if os.path.isdir(full_path):
                mp3s = [f for f in os.listdir(full_path) if f.lower().endswith(".mp3")]
                if mp3s:
                    folder_queue.append(full_path)

    current_folder_index = 0
    if folder_queue:
        load_folder()

def load_folder():
    # Load all songs from current folder

    global playlist, current_song_index
    if not folder_queue:
        return
    folder = folder_queue[current_folder_index]
    playlist = [
        os.path.join(folder, f)
        for f in sorted(os.listdir(folder))
        if f.lower().endswith(".mp3")
    ]
    current_song_index = 0
    if playlist:
        load_song()
        play_current()

def load_song():

    global current_song, song_length, song_start_time, song_elapsed, is_paused
    if not playlist:
        current_song = None
        song_length = 0.0
        return
    current_song = playlist[current_song_index]
    try:
        pygame.mixer.music.load(current_song)
        song_length = pygame.mixer.Sound(current_song).get_length()
    except Exception:
        song_length = 0.0
    song_start_time = None
    song_elapsed = 0.0
    is_paused = False
    update_display()

# === player engine ===
def play_current():
    # Actually play the song (had a problem there), resume from elapsed if paused

    global song_start_time, is_paused
    if not current_song:
        return
    pygame.mixer.music.play(start=song_elapsed)
    song_start_time = time.time() - song_elapsed
    is_paused = False
    update_progress()

def pause_current():
    # Pause + record elapsed time so we can resume correctly

    global song_elapsed, song_start_time, is_paused
    if not current_song:
        return
    try:
        pygame.mixer.music.pause()
    except Exception:
        pass
    if song_start_time is not None:
        song_elapsed = time.time() - song_start_time
    song_start_time = None
    is_paused = True
    update_progress()
    update_display()

def play_pause():
    # Toggle pause/play state

    global is_paused, song_start_time
    if not playlist or not current_song:
        return

    if is_paused:
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pygame.mixer.music.play(start=song_elapsed)
        song_start_time = time.time() - song_elapsed
        is_paused = False
    else:
        if pygame.mixer.music.get_busy():
            pause_current()
        else:
            play_current()
    update_display()

def next_song():
    # Jump forward, also loop folders when reaching the end

    global current_song_index, current_folder_index
    if not playlist:
        return
    current_song_index += 1
    if current_song_index >= len(playlist):
        if folder_queue:
            current_folder_index = (current_folder_index + 1) % len(folder_queue)
            load_folder()
            return
        else:
            current_song_index = 0
    load_song()
    play_current()

def prev_song():
    # Jump backwards, loop to previous folder if needed

    global current_song_index, current_folder_index
    if not playlist:
        return
    current_song_index -= 1
    if current_song_index < 0:
        if folder_queue:
            current_folder_index = (current_folder_index - 1) % len(folder_queue)
            load_folder()
            current_song_index = len(playlist) - 1
        else:
            current_song_index = 0
    load_song()
    play_current()

def check_song_end():
    # Keeps checking if song finished -> then auto next
    try:
        if playlist and current_song is not None and not is_paused:
            if song_length > 0:
                if song_start_time is not None:
                    elapsed = time.time() - song_start_time
                else:
                    elapsed = song_elapsed
                if elapsed + 0.6 >= song_length:  # +0.6 fudge for pygame timing
                    next_song()
    except Exception:
        pass
    root.after(700, check_song_end)

# === screen / text ===
def update_display():
    if not playlist or not current_song:
        title_var.set("No song playing")
        album_var.set("")
        now_playing_var.set("")
        elapsed_var.set("0:00")
        remaining_var.set("-0:00")
        canvas.delete("progress")
        return

    folder_name = os.path.basename(os.path.dirname(current_song))
    song_name = os.path.splitext(os.path.basename(current_song))[0]

    title_var.set(song_name)
    album_var.set(folder_name)
    now_playing_var.set("Now Playing")

def format_time(seconds):
    # Convert seconds to M:SS (math genius)
    try:
        s = max(0, int(seconds))
        m = s // 60
        sec = s % 60
        return f"{m}:{sec:02d}"
    except Exception:
        return "0:00"

def update_progress():
    # Draw progress bar + update timers
    global song_elapsed, song_start_time
    if not playlist or not current_song:
        elapsed_var.set("0:00")
        remaining_var.set("-0:00")
        canvas.delete("progress")
        return

    if is_paused or (song_start_time is None):
        elapsed = song_elapsed
    else:
        elapsed = time.time() - song_start_time

    elapsed = max(0.0, elapsed)
    progress = min(elapsed / song_length, 1.0) if song_length > 0 else 0.0

    canvas.delete("progress")
    progress_pixel = int(progress * inner_progress_width)
    if progress_pixel > 0:
        canvas.create_rectangle(
            0, 0, progress_pixel, progress_height,
            fill="#00BFFF", width=0, tags="progress"
        )

    elapsed_var.set(format_time(elapsed))
    remaining_var.set("-" + format_time(max(0.0, song_length - elapsed)))
    root.after(500, update_progress)

# === artwork ===
def load_cover(path="cover_placeholder.png"):
    global _cover_img
    try:
        _cover_img = tk.PhotoImage(file=path)
        cover_label.config(image=_cover_img)
    except Exception:
        cover_label.config(image="")

def load_topbar(path="TopBar.png"):
    global _topbar_img
    try:
        _topbar_img = tk.PhotoImage(file=path)
        topbar_label.config(image=_topbar_img)
    except Exception:
        topbar_label.config(image="")

# === screen frame ===
root = tk.Tk()
root.title("iPod Player")
root.geometry("390x642")
root.resizable(False, False)

main_canvas = tk.Canvas(root, width=390, height=642, highlightthickness=0)
main_canvas.place(x=0, y=0)

try:
    _bg_image = tk.PhotoImage(file="ipod_background.png")
    main_canvas.create_image(0, 0, anchor="nw", image=_bg_image)
except Exception:
    main_canvas.create_rectangle(0, 0, 390, 642, fill="#ddd")

screen_frame = tk.Frame(root, bg="white")
screen_x, screen_y, screen_w, screen_h = 33, 31, 324, 245
screen_frame.place(x=screen_x, y=screen_y, width=screen_w, height=screen_h)

# === screen elements ===
topbar_label = tk.Label(screen_frame, bg="white")
topbar_label.place(x=0, y=0, width=324, height=20)
load_topbar("TopBar.png")

now_playing_var = tk.StringVar(value="")
now_playing_label = tk.Label(screen_frame, textvariable=now_playing_var,
                             font=("Helvetica", 11, "bold"), bg="white", anchor="center")
now_playing_label.place(x=0, y=24, width=324, height=20)

cover_label = tk.Label(screen_frame, bg="white")
cover_label.place(x=30, y=50, width=130, height=130)

title_var = tk.StringVar(value="")
album_var = tk.StringVar(value="")

title_label = tk.Label(screen_frame, textvariable=title_var,
                       font=("Helvetica", 12, "bold"), bg="white", fg="black", anchor="w")
title_label.place(x=170, y=70, width=140, height=25)

album_label = tk.Label(screen_frame, textvariable=album_var,
                       font=("Helvetica", 10), bg="white", fg="black", anchor="w")
album_label.place(x=170, y=100, width=140, height=20)

# progress bar + timers
progress_y = 208
progress_height = 12

elapsed_var = tk.StringVar(value="0:00")
elapsed_label = tk.Label(screen_frame, textvariable=elapsed_var,
                         font=("Helvetica", 12), bg="white", fg="black", anchor="w")
elapsed_label.place(x=20, y=progress_y, width=50, height=progress_height)

remaining_var = tk.StringVar(value="-0:00")
remaining_label = tk.Label(screen_frame, textvariable=remaining_var,
                          font=("Helvetica", 12), bg="white", fg="black", anchor="e")
remaining_label.place(x=screen_w - 70, y=progress_y, width=50, height=progress_height)

bar_left = 70
bar_right = screen_w - 70
inner_progress_width = bar_right - bar_left
canvas = tk.Canvas(screen_frame, bg="white", highlightthickness=0)
canvas.place(x=bar_left, y=progress_y, width=inner_progress_width, height=progress_height)

load_cover("cover_placeholder.png")

# === buttons / hotspots ===
def make_hotspot(x, y, w, h, tag):
    # Invisible rectangle over button areas
    rect = main_canvas.create_rectangle(x, y, x + w, y + h, outline="", fill="")
    main_canvas.tag_bind(rect, "<Button-1>", lambda e, t=tag: hotspot_click(t))
    return rect

def hotspot_click(tag):
    if tag == "menu":
        choose_folder()
    elif tag == "prev":
        prev_song()
    elif tag == "next":
        next_song()
    elif tag == "play":
        play_pause()

# coords roughly where iPod buttons are drawn on the bg
# (bit bigger so you don't need to exactly click on the button like on the iPod)

make_hotspot(164, 362, 80, 50, "menu")
make_hotspot(82, 453, 80, 50, "prev")
make_hotspot(245, 453, 80, 50, "next")
make_hotspot(164, 545, 80, 50, "play")

# === run loop ===
root.after(700, check_song_end)
update_display()
update_progress()
root.mainloop()

#hope it's a fun gimmick
