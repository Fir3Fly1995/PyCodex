import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import urllib.request
import time

# Raw URL to Codex.py (not the GitHub page URL)
GITHUB_RAW_URL = "https://github.com/Fir3Fly1995/CodexPython/blob/main/PyCodex/dist/Codex.exe"

def launch_codex():
    codex_path = os.path.join(os.environ["LOCALAPPDATA"], "Codex", "codex.exe")
    if os.path.exists(codex_path):
        subprocess.Popen([codex_path])
        root.after(4000, root.destroy)  # Close the launcher after 4 seconds
    else:
        messagebox.showerror("Error", f"codex.exe not found at {codex_path}")

def update_codex():
    codex_dir = os.path.join(os.environ["LOCALAPPDATA"], "Codex")
    codex_path = os.path.join(codex_dir, "codex.exe")
    try:
        if not os.path.exists(codex_dir):
            os.makedirs(codex_dir)
        if os.path.exists(codex_path):
            os.remove(codex_path)
            time.sleep(0.5)  # Wait a moment for file system
        urllib.request.urlretrieve(GITHUB_RAW_URL, codex_path)
        messagebox.showinfo("Update", "codex.exe updated successfully!")
    except Exception as e:
        messagebox.showerror("Update Failed", str(e))

def uninstall_codex():
    codex_dir = os.path.join(os.environ["LOCALAPPDATA"], "Codex")
    uninstaller = os.path.join(codex_dir, "unins000.exe")
    if os.path.exists(uninstaller):
        subprocess.Popen([uninstaller])
        root.after(1000, lambda: os._exit(0))  # Wait 1 second, then force exit
    else:
        messagebox.showerror("Uninstall Error", "Uninstaller not found!")

root = tk.Tk()
root.title("Codex Launcher")
root.geometry("300x200")

launch_btn = tk.Button(root, text="Launch Codex", command=launch_codex, width=20, height=2)
launch_btn.pack(pady=10)

update_btn = tk.Button(root, text="Update Codex.py", command=update_codex, width=20, height=2)
update_btn.pack(pady=10)

uninstall_btn = tk.Button(root, text="Uninstall Codex", command=uninstall_codex, width=20, height=2)
uninstall_btn.pack(pady=10)

root.mainloop()