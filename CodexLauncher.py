import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import urllib.request
import time

def launch_codex():
    codex_path = os.path.join(os.environ["LOCALAPPDATA"], "Codex", "codex.exe")
    if os.path.exists(codex_path):
        subprocess.Popen([codex_path])
        root.after(2000, root.destroy)  # Close the launcher after 2 seconds
    else:
        messagebox.showerror("Error", f"codex.exe not found at {codex_path}")

def uninstall_codex():
    codex_dir = os.path.join(os.environ["LOCALAPPDATA"], "Codex")
    uninstaller = os.path.join(codex_dir, "unins000.exe")
    if os.path.exists(uninstaller):
        subprocess.Popen([uninstaller])
        root.after(1000, lambda: os._exit(0))  # Wait 1 second, then force exit
    else:
        messagebox.showerror("Uninstall Error", "Uninstaller not found!")

def check_for_updates():
    codex_dir = os.path.join(os.environ["LOCALAPPDATA"], "Codex")
    updater_path = os.path.join(codex_dir, "CodexUpdate.exe")
    if os.path.exists(updater_path):
        try:
            subprocess.Popen([updater_path], cwd=codex_dir)
            root.after(1000, root.destroy)  # Close the launcher after 1 second
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch updater: {e}")
    else:
        messagebox.showerror("Error", f"CodexUpdate.exe not found at {updater_path}")

root = tk.Tk()
root.title("Codex Launcher")
root.geometry("300x200")

launch_btn = tk.Button(root, text="Launch Codex", command=launch_codex, width=20, height=2)
launch_btn.pack(pady=10)

update_btn = tk.Button(root, text="Check for Updates", command=check_for_updates, width=20, height=2)
update_btn.pack(pady=10)

uninstall_btn = tk.Button(root, text="Uninstall Codex", command=uninstall_codex, width=20, height=2)
uninstall_btn.pack(pady=10)

root.mainloop()