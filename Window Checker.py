# Codex Navigator UI v2.8 – Scroll Focus Fix & Workspace Resize

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import fitz  # PyMuPDF
import os
import sys
import subprocess
import re
from PIL import Image, ImageTk
from io import BytesIO

# Compatibility: Use Resampling for PIL >= 10
if hasattr(Image, 'Resampling'):
    RESAMPLING_MODE = Image.Resampling.LANCZOS
else:
    RESAMPLING_MODE = Image.ANTIALIAS

# --- Root Setup ---
root = tk.Tk()
root.title("Codex Visual Navigator")
root.geometry("1180x720")  # Reduced width by 100px
root.minsize(1180, 720)

pdf_path = filedialog.askopenfilename(
    title="Select a Codex PDF",
    filetypes=[("PDF files", "*.pdf")]
)

if not pdf_path:
    sys.exit()

# --- PDF Extraction ---
doc = fitz.open(pdf_path)
toc = doc.get_toc()

parsed_sections = []
for i in range(len(toc)):
    level, title, start_page = toc[i]
    if i + 1 < len(toc):
        end_page = toc[i + 1][2]
    else:
        end_page = len(doc)
    parsed_sections.append({
        "level": level,
        "title": title,
        "start": start_page,
        "end": end_page
    })

# --- UI Layout ---
top_frame = ttk.Frame(root)
top_frame.pack(fill='x')

view_mode = tk.StringVar(value="image")

exit_btn = ttk.Button(top_frame, text="Exit", command=lambda: os._exit(0))
exit_btn.pack(side='right', padx=5, pady=5)

restart_btn = ttk.Button(top_frame, text="Open Other", command=lambda: os.execl(sys.executable, sys.executable, *sys.argv))
restart_btn.pack(side='right', padx=5, pady=5)

toggle_btn = ttk.Button(top_frame, text="Toggle View Mode")
toggle_btn.pack(side='right', padx=5, pady=5)

label = ttk.Label(top_frame, text="Codex Navigator", font=("Segoe UI", 14, "bold"))
label.pack(side='left', padx=10)

main_pane = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
main_pane.pack(fill='both', expand=True)

# --- Tree Panel ---
tree_container = ttk.Frame(main_pane, width=300)
main_pane.add(tree_container, weight=1)

tree_scroll = ttk.Scrollbar(tree_container, orient="vertical")
tree_scroll.pack(side="right", fill="y")

tree = ttk.Treeview(tree_container, yscrollcommand=tree_scroll.set)
tree.pack(fill='both', expand=True, padx=5, pady=5)
tree_scroll.config(command=tree.yview)

# Scroll isolation for tree

def on_tree_scroll(event):
    tree.yview_scroll(int(-1 * (event.delta / 120)), "units")

tree.bind("<Enter>", lambda e: root.bind_all("<MouseWheel>", on_tree_scroll))
tree.bind("<Leave>", lambda e: root.unbind_all("<MouseWheel>"))

# --- Workspace Panel ---
workspace = tk.Frame(main_pane, bg="#1a1a1a")
main_pane.add(workspace, weight=3)

content_frame = ttk.Frame(workspace)
content_frame.pack(fill='both', expand=True)

selected_section = {}

# --- Content Display Functions ---
def show_section_as_image(sec):
    for widget in content_frame.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(content_frame, bg="#1a1a1a", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    v_scroll = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    v_scroll.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=v_scroll.set)

    inner_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    images = []

    for p in range(sec['start'], min(sec['end'], sec['start'] + 1)):
        try:
            pix = doc[p - 1].get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img = Image.open(BytesIO(pix.tobytes("ppm")))
            img = img.resize((800, int(800 * img.height / img.width)), RESAMPLING_MODE)
            tk_img = ImageTk.PhotoImage(img)
            images.append(tk_img)

            panel = ttk.Label(inner_frame, image=tk_img)
            panel.image = tk_img
            panel.pack(pady=10)
        except Exception as e:
            print(f"Failed to render image for page {p}: {e}")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_configure)

    def on_image_scroll(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind("<Enter>", lambda e: root.bind_all("<MouseWheel>", on_image_scroll))
    canvas.bind("<Leave>", lambda e: root.unbind_all("<MouseWheel>"))


def show_section_as_text(sec):
    for widget in content_frame.winfo_children():
        widget.destroy()

    textbox = tk.Text(content_frame, wrap='word', bg='white', fg='black', font=("Segoe UI", 12))
    textbox.pack(fill='both', expand=True)

    text = ""
    for p in range(sec['start'] - 1, sec['end'] - 1):
        try:
            text += doc[p].get_text("text") + "\n"
        except Exception as e:
            print(f"Failed to extract text for page {p + 1}: {e}")
    textbox.insert("1.0", text.strip())


# --- Tree Loader ---
parent_nodes = {}

for sec in parsed_sections:
    level = sec["level"]
    title = sec["title"]
    start, end = sec["start"], sec["end"]

    if level == 1:
        node = tree.insert("", "end", text=title, open=True, values=(start, end))
        parent_nodes[1] = node
    else:
        parent = parent_nodes.get(level - 1, "")
        node = tree.insert(parent, "end", text=title, values=(start, end))
        parent_nodes[level] = node


# --- Tree Event Handler ---
def on_tree_select(event):
    sel = tree.focus()
    if not sel:
        return
    start, end = tree.item(sel, "values")
    if start and end:
        global selected_section
        selected_section = {"title": tree.item(sel, "text"), "start": int(start), "end": int(end)}
        if view_mode.get() == "image":
            show_section_as_image(selected_section)
        else:
            show_section_as_text(selected_section)

tree.bind("<<TreeviewSelect>>", on_tree_select)

def toggle_view():
    if not selected_section:
        return
    view_mode.set("text" if view_mode.get() == "image" else "image")
    if view_mode.get() == "image":
        show_section_as_image(selected_section)
    else:
        show_section_as_text(selected_section)

toggle_btn.configure(command=toggle_view)

if parsed_sections:
    selected_section = parsed_sections[0]
    show_section_as_image(selected_section)

root.mainloop()
