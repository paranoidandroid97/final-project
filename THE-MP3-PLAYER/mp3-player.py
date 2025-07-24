import tkinter as tk #buttons for gui
from tkinter import filedialog, PhotoImage #lets me show a picture and pop up window
import pygame #for playing music/sounds
import os #so it can access the files on my computer

# this should be the setup for the main window
root = tk.Tk() #for creating window
root.title("MP3 Player") #name of window
root.geometry("275x400") #resolution of window

# Init pygame mixer
pygame.mixer.init()

songs = []

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        os.chdir(folder)
        for file in os.listdir():
            if file.endswith(".mp3"):
                songs.append(file)

def play():
    if songs:
        pygame.mixer.music.load(songs[0])
        pygame.mixer.music.play()

def stop():
    pygame.mixer.music.stop()


# Buttons
btn_choose = tk.Button(root, text="Choose Folder", command=choose_folder)
btn_choose.pack(pady=20)

btn_play = tk.Button(root, text="Play First Song", command=play)
btn_play.pack(pady=10)

btn_stop = tk.Button(root, text="Stop", command=stop)
btn_stop.pack(pady=10)


# still working on stuff below:
# stop/play button, image(cover), playlist?, next/prev?, error message

#playlist perspective. Adding songs on top of each other like a playlist, title shwotijn, recursive checking, mutiple folders deep
root.mainloop()
