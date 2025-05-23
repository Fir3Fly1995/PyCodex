import tkinter as tk
from tkinter import messagebox, PhotoImage
import subprocess
import os
import urllib.request

# --- Functions ---
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
    updater_url = "https://github.com/Fir3Fly1995/PyCodex/raw/main/dist/CodexUpdate.exe"
    try:
        if os.path.exists(updater_path):
            try:
                os.remove(updater_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not remove old updater: {e}")
                return
        urllib.request.urlretrieve(updater_url, updater_path)
        if os.path.exists(updater_path):
            subprocess.Popen([updater_path], cwd=codex_dir)
            root.after(1000, root.destroy)
        else:
            messagebox.showerror("Error", f"CodexUpdate.exe not found at {updater_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch or launch updater:\n{e}")

def close_launcher():
    os._exit(0)

def start_move(event):
    root._drag_start_x = event.x_root
    root._drag_start_y = event.y_root
    root._start_win_x = root.winfo_x()
    root._start_win_y = root.winfo_y()

def do_move(event):
    dx = event.x_root - root._drag_start_x
    dy = event.y_root - root._drag_start_y
    new_x = root._start_win_x + dx
    new_y = root._start_win_y + dy

    # Clamp to screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    win_width = root.winfo_width()
    win_height = root.winfo_height()
    new_x = max(0, min(new_x, screen_width - win_width))
    new_y = max(0, min(new_y, screen_height - win_height))

    root.geometry(f"+{new_x}+{new_y}")

# --- Main UI ---
root = tk.Tk()
root.geometry("1024x512")
root.configure(bg="black")
root.overrideredirect(True)

# Center the window
root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (1024 // 2)
y = (screen_height // 2) - (512 // 2)
root.geometry(f"1024x512+{x}+{y}")

canvas = tk.Canvas(root, width=1024, height=512, highlightthickness=0, bg="black")
canvas.pack(fill="both", expand=True)

# Load background
bg_path = os.path.join(os.environ["LOCALAPPDATA"], "Codex", "CodexBG.png")
if os.path.exists(bg_path):
    try:
        bg_photo = PhotoImage(file=bg_path)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.bg_photo = bg_photo
    except Exception as e:
        print(f"Failed to load background image: {e}")

# --- Top bar for dragging and close ---
top_bar = tk.Frame(root, height=40, bg="black", cursor="fleur", highlightthickness=0, bd=0)
top_bar.place(x=0, y=0, relwidth=1)
top_bar.lift()
top_bar.bind("<ButtonPress-1>", start_move)
top_bar.bind("<B1-Motion>", do_move)

def on_enter_x(e):
    e.widget.config(bg="#ff4444", activebackground="#ff4444")

def on_leave_x(e):
    e.widget.config(bg="#cc4444", activebackground="#cc4444")

btn_x = tk.Button(
    root, text="✕", command=close_launcher, bg="#cc4444", fg="black",
    font=("Segoe UI", 18, "bold"), bd=0, highlightthickness=0, relief="flat",
    activebackground="#cc4444", activeforeground="black"
)
btn_x.place(x=1024-40, y=0, width=40, height=40)
btn_x.lift()
btn_x.bind("<Enter>", on_enter_x)
btn_x.bind("<Leave>", on_leave_x)

# --- Buttons ---
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

def on_enter_btn(e):
    e.widget.config(bg="#333333", activebackground="#333333")

def on_leave_btn(e):
    e.widget.config(bg="#222222", activebackground="#444444")

launch_btn = tk.Button(root, text="Launch Codex", command=launch_codex, **button_style)
update_btn = tk.Button(root, text="Check for Updates", command=check_for_updates, **button_style)
uninstall_btn = tk.Button(root, text="Uninstall Codex", command=uninstall_codex, **button_style)

launch_btn.place(x=50, y=230)
update_btn.place(x=50, y=290)
uninstall_btn.place(x=50, y=350)

# Add hover effects
for btn in (launch_btn, update_btn, uninstall_btn):
    btn.bind("<Enter>", on_enter_btn)
    btn.bind("<Leave>", on_leave_btn)

# Version label in the bottom left corner
version_label = tk.Label(
    root,
    text="Version Number 0x1F.0x1",
    bg="black",
    fg="#888888",
    font=("Segoe UI", 8),
    anchor="w"
)
version_label.place(x=8, y=512-20)

root.mainloop()