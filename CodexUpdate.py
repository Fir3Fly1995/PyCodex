import os
import sys
import tkinter as tk
from tkinter import messagebox
import subprocess
import psutil
import requests
import shutil
import webbrowser

# --- Config ---
LOCALAPPDATA = os.environ.get("LOCALAPPDATA")
CODEX_DIR = os.path.join(LOCALAPPDATA, "Codex")
CODEX_EXE = os.path.join(CODEX_DIR, "Codex.exe")
LAUNCHER_EXE = os.path.join(CODEX_DIR, "CodexLauncher.exe")
CODEX_URL = "https://github.com/Fir3Fly1995/PyCodex/raw/main/dist/Codex.exe"
LAUNCHER_URL = "https://github.com/Fir3Fly1995/PyCodex/raw/main/dist/CodexLauncher.exe"
BACKGROUND_IMAGE_PATH = r"D:\GitHub\pyCodex\Images\UpdateBG.png"

# --- Functions ---
def kill_processes():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in ("Codex.exe", "CodexLauncher.exe"):
            try:
                proc.terminate()
            except Exception:
                pass

def download_and_replace(url, dest):
    try:
        if os.path.exists(dest):
            os.remove(dest)
        r = requests.get(url, stream=True)
        with open(dest, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        # No notification here!
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update: {e}")

def update_all():
    download_and_replace(CODEX_URL, CODEX_EXE)
    download_and_replace(LAUNCHER_URL, LAUNCHER_EXE)
    exit_and_launch()  # Only exit after both updates

def exit_and_launch():
    try:
        subprocess.Popen([LAUNCHER_EXE], cwd=CODEX_DIR)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch: {e}")
    root.after(500, lambda: os._exit(0))

def close_app():
    root.after(100, lambda: os._exit(0))

def start_move(event):
    root._drag_start_x = event.x
    root._drag_start_y = event.y

def do_move(event):
    x = root.winfo_x() + (event.x - root._drag_start_x)
    y = root.winfo_y() + (event.y - root._drag_start_y)
    root.geometry(f"+{x}+{y}")

# --- Main UI ---
kill_processes()
root = tk.Tk()
root.title("Codex Updater")
root.geometry("500x500")
root.resizable(False, False)
root.overrideredirect(True)  # Remove the titlebar

# Center the window on the screen
root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (500 // 2)
y = (screen_height // 2) - (500 // 2)
root.geometry(f"500x500+{x}+{y}")

# Background image
canvas = tk.Canvas(root, width=500, height=500, highlightthickness=0, bd=0)
canvas.place(x=0, y=0)
try:
    bg_img = tk.PhotoImage(file=BACKGROUND_IMAGE_PATH)
    canvas.create_image(0, 0, anchor='nw', image=bg_img)
except Exception:
    canvas.create_rectangle(0, 0, 500, 500, fill="black")

# Black grabbable area at the top (40px)
grab_area = tk.Frame(root, height=40, bg="black", cursor="fleur", highlightthickness=0, bd=0)
grab_area.place(x=0, y=0, relwidth=1)
grab_area.lift()
grab_area.bind("<ButtonPress-1>", start_move)
grab_area.bind("<B1-Motion>", do_move)

# Update and Exit buttons with 12px spacing, centered horizontally
button_y = 250
button_width = 120  # Approximate pixel width for width=15
gap = 12

# Center of window
center_x = 250

# --- Button hover effects ---
def on_enter_black(e):
    e.widget.config(bg="#222", activebackground="#222")

def on_leave_black(e):
    e.widget.config(bg="black", activebackground="#333")

def on_enter_x(e):
    e.widget.config(bg="#ff4444", activebackground="#ff4444")

def on_leave_x(e):
    e.widget.config(bg="#cc4444", activebackground="#cc4444")

# Update button
btn_update = tk.Button(
    root, text="Update", width=15, bg="black", fg="white",
    font=("Segoe UI", 12), relief="flat", activebackground="#333",
    activeforeground="white", borderwidth=0, highlightthickness=0,
    command=update_all
)
btn_update.place(x=center_x - button_width//2 - gap//2, y=button_y, width=button_width, height=40, anchor='e')
btn_update.bind("<Enter>", on_enter_black)
btn_update.bind("<Leave>", on_leave_black)

# Exit button
btn_exit = tk.Button(
    root, text="Exit", width=15, bg="black", fg="white",
    font=("Segoe UI", 12), relief="flat", activebackground="#333",
    activeforeground="white", borderwidth=0, highlightthickness=0,
    command=exit_and_launch
)
btn_exit.place(x=center_x + button_width//2 + gap//2, y=button_y, width=button_width, height=40, anchor='w')
btn_exit.bind("<Enter>", on_enter_black)
btn_exit.bind("<Leave>", on_leave_black)

# X button in the top right corner of the black bar (40x40px, softer red bg, black X)
btn_x = tk.Button(
    root, text="✕", command=close_app, bg="#cc4444", fg="black",
    activebackground="#cc4444", activeforeground="black",
    bd=0, highlightthickness=0, relief="flat", font=("Segoe UI", 18, "bold")
)
btn_x.place(x=500-40, y=0, width=40, height=40)
btn_x.bind("<Enter>", on_enter_x)
btn_x.bind("<Leave>", on_leave_x)

# Instructions label
instructions = (
    "If you would like to update the images, please click the button below, "
    "get an image of either 504x504 or 1024x512. The long image needs to be named CodexBG "
    "and the square image named UpdateBG. This will change the images for the codex and the launcher."
)
lbl_instructions = tk.Label(
    root,
    text=instructions,
    wraplength=460,
    justify="left",
    bg="black",
    fg="white",
    font=("Segoe UI", 10)
)
lbl_instructions.place(x=20, y=320)

def open_codex_folder():
    path = os.path.normpath(CODEX_DIR)
    if os.path.exists(path):
        os.startfile(path)
    else:
        messagebox.showerror("Error", f"Folder not found:\n{path}")

btn_open_folder = tk.Button(
    root,
    text="Open Codex Image Folder",
    width=25,
    bg="#222",
    fg="white",
    font=("Segoe UI", 11),
    relief="flat",
    activebackground="#444",
    activeforeground="white",
    borderwidth=0,
    highlightthickness=0,
    command=open_codex_folder
)
btn_open_folder.place(x=140, y=400, width=220, height=36)

root.mainloop()
