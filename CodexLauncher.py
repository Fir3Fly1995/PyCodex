import tkinter as tk
from tkinter import messagebox, PhotoImage
import subprocess
import sys
import os

def launch_codex():
    codex_path = os.path.join(os.environ["LOCALAPPDATA"], "Codex", "codex.exe")
    if os.path.exists(codex_path):
        subprocess.Popen([codex_path])
        root.after(2000, root.destroy)
    else:
        messagebox.showerror("Error", f"codex.exe not found at {codex_path}")

def uninstall_codex():
    codex_dir = os.path.join(os.environ["LOCALAPPDATA"], "Codex")
    uninstaller = os.path.join(codex_dir, "unins000.exe")
    if os.path.exists(uninstaller):
        subprocess.Popen([uninstaller])
        root.after(1000, lambda: os._exit(0))
    else:
        messagebox.showerror("Uninstall Error", "Uninstaller not found!")

def check_for_updates():
    codex_dir = os.path.join(os.environ["LOCALAPPDATA"], "Codex")
    updater_path = os.path.join(codex_dir, "CodexUpdate.exe")
    if os.path.exists(updater_path):
        try:
            subprocess.Popen([updater_path], cwd=codex_dir)
            root.after(1000, root.destroy)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch updater: {e}")
    else:
        messagebox.showerror("Error", f"CodexUpdate.exe not found at {updater_path}")

def close_launcher():
    os._exit(0)

def start_move(event):
    if event.y <= 40:
        root.startX = event.x_root
        root.startY = event.y_root
    else:
        root.startX = None
        root.startY = None

def do_move(event):
    if root.startX is not None and root.startY is not None:
        x = event.x_root - root.startX
        y = event.y_root - root.startY
        new_x = root.winfo_x() + x
        new_y = root.winfo_y() + y
        root.geometry(f"+{new_x}+{new_y}")
        root.startX = event.x_root
        root.startY = event.y_root

def stop_move(event):
    root.startX = None
    root.startY = None

root = tk.Tk()
root.geometry("1024x512")
root.configure(bg="black")
root.overrideredirect(True)

# Center the window on the screen
root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 1024
window_height = 512
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

canvas = tk.Canvas(root, width=1024, height=512, highlightthickness=0, bg="black")
canvas.pack(fill="both", expand=True)

canvas.bind("<ButtonPress-1>", start_move)
canvas.bind("<B1-Motion>", do_move)
canvas.bind("<ButtonRelease-1>", stop_move)

bg_path = os.path.join(os.environ["LOCALAPPDATA"], "Codex", "CodexBG.png")
if os.path.exists(bg_path):
    try:
        bg_photo = PhotoImage(file=bg_path)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.bg_photo = bg_photo
    except Exception as e:
        print(f"Failed to load background image: {e}")

button_style = {
    "bg": "#222222",
    "fg": "#ffffff",
    "activebackground": "#444444",
    "activeforeground": "#ffffff",
    "font": ("Segoe UI", 11, "bold"),
    "bd": 0,
    "highlightthickness": 0,
    "width": 20,
    "height": 2
}

launch_btn = tk.Button(root, text="Launch Codex", command=launch_codex, **button_style)
update_btn = tk.Button(root, text="Check for Updates", command=check_for_updates, **button_style)
uninstall_btn = tk.Button(root, text="Uninstall Codex", command=uninstall_codex, **button_style)

# Close button inside canvas
close_btn = tk.Button(canvas, text="X", command=close_launcher, bg="#222222", fg="#ffffff", 
                      activebackground="#aa0000", activeforeground="#ffffff", font=("Segoe UI", 10, "bold"),
                      bd=0, highlightthickness=0, width=3, height=1)

launch_btn.place(x=50, y=230)
update_btn.place(x=50, y=290)
uninstall_btn.place(x=50, y=350)
canvas.create_window(1000, 492, anchor="se", window=close_btn)

root.mainloop()
