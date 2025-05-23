import os
import sys
import tkinter as tk
from tkinter import messagebox
import subprocess
import psutil
import requests
import shutil

LOCALAPPDATA = os.environ.get("LOCALAPPDATA")
CODEX_DIR = os.path.join(LOCALAPPDATA, "Codex")
CODEX_EXE = os.path.join(CODEX_DIR, "Codex.exe")
LAUNCHER_EXE = os.path.join(CODEX_DIR, "CodexLauncher.exe")

CODEX_URL = "https://github.com/Fir3Fly1995/PyCodex/raw/main/dist/Codex.exe"
LAUNCHER_URL = "https://github.com/Fir3Fly1995/PyCodex/raw/main/dist/CodexLauncher.exe"

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
        messagebox.showinfo("Success", f"Updated {os.path.basename(dest)} successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update: {e}")

def update_codex():
    download_and_replace(CODEX_URL, CODEX_EXE)

def update_launcher():
    download_and_replace(LAUNCHER_URL, LAUNCHER_EXE)

def return_to_launcher():
    try:
        subprocess.Popen([LAUNCHER_EXE], cwd=CODEX_DIR)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch: {e}")
    root.after(500, lambda: os._exit(0))

def exit_app():
    os._exit(0)

# Terminate Codex and Launcher on startup
kill_processes()

root = tk.Tk()
root.title("Codex Updater")
root.geometry("300x200")

btn_update_codex = tk.Button(root, text="Update Codex", width=25, command=update_codex)
btn_update_codex.pack(pady=10)

btn_update_launcher = tk.Button(root, text="Update Launcher", width=25, command=update_launcher)
btn_update_launcher.pack(pady=10)

btn_return_launcher = tk.Button(root, text="Return to Launcher", width=25, command=return_to_launcher)
btn_return_launcher.pack(pady=10)

btn_exit = tk.Button(root, text="Exit", width=25, command=exit_app)
btn_exit.pack(pady=10)

root.mainloop()