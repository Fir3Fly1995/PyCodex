import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import fitz  # PyMuPDF
import re
import os
import sys
import subprocess

# --- Ask user for PDF file ---
root = tk.Tk()
root.withdraw()  # Hide main window while selecting file
pdf_path = filedialog.askopenfilename(
    title="Select a PDF file",
    filetypes=[("PDF files", "*.pdf")],
)
if not pdf_path:
    answer = messagebox.askyesno("Cancel", "Are you sure you want to cancel?\n\nPress Yes to exit and return to the launcher.\nPress No to select a file again.")
    if answer:
        # Relaunch the launcher if it exists
        launcher_path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Codex", "CodexLauncher.exe")
        if os.path.exists(launcher_path):
            subprocess.Popen([launcher_path], cwd=os.path.dirname(launcher_path))
        os._exit(0)
    else:
        # Restart the program
        python = sys.executable
        os.execl(python, python, *sys.argv)
root.deiconify()  # Show main window

PDF_PATH = pdf_path

# --- Extract PDF structure and content ---
doc = fitz.open(PDF_PATH)
toc = doc.get_toc()  # [[level, title, page], ...]
toc_with_ranges = []
for i in range(len(toc)):
    level, title, start_page = toc[i]
    end_page = toc[i+1][2] if i + 1 < len(toc) else len(doc)
    # Cap each section at the next heading of same or higher level
    for j in range(i + 1, len(toc)):
        if toc[j][0] <= level:
            end_page = toc[j][2]
            break
    toc_with_ranges.append((level, title, start_page, end_page))

sections = []
for level, title, start, end in toc_with_ranges:
    text = "\n".join([doc[pg].get_text("text") for pg in range(start - 1, end - 1)])
    sections.append({
        "level": level,
        "title": title,
        "start_page": start,
        "end_page": end,
        "text": text.strip()
    })

# --- Build nested structure: Set > Stage > Part > Subpart ---
def build_codex_structure(sections):
    codex_structure = {}
    set_name = stage_name = part_name = None
    for s in sections:
        if s["level"] == 1:
            set_name = s["title"]
            codex_structure[set_name] = {}
            stage_name = part_name = None
        elif s["level"] == 2 and set_name:
            stage_name = s["title"]
            codex_structure[set_name][stage_name] = {}
            part_name = None
        elif s["level"] == 3 and set_name and stage_name:
            part_name = s["title"]
            codex_structure[set_name][stage_name][part_name] = {
                "_home": s["text"]
            }
        elif s["level"] == 4 and set_name and stage_name and part_name:
            codex_structure[set_name][stage_name][part_name][s["title"]] = s["text"]
    return codex_structure

codex_structure = build_codex_structure(sections)

def after_dash(title):
    match = re.search(r"-\s*(.+)", title)
    return match.group(1).strip() if match else title.strip()

# --- Tkinter GUI ---
root.title("Codex")
root.geometry("1000x700")

# Home controls at the top
top_frame = ttk.Frame(root)
top_frame.pack(fill='x', pady=5)

def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)

select_file_btn = ttk.Button(top_frame, text="Select New File", command=restart_app)
select_file_btn.pack(side='left', padx=10)

def exit_and_launch_launcher():
    launcher_path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Codex", "CodexLauncher.exe")
    try:
        if os.path.exists(launcher_path):
            subprocess.Popen([launcher_path], cwd=os.path.dirname(launcher_path))
    except Exception:
        pass
    root.after(1000, lambda: os._exit(0))

exit_btn = ttk.Button(top_frame, text="Exit", command=exit_and_launch_launcher)
exit_btn.pack(side='left', padx=10)

info_label = ttk.Label(top_frame, text="More features coming soon!", font=("Segoe UI", 12, "italic"))
info_label.pack(side='left', padx=20)

# Tab Notebooks (no labels)
set_notebook = ttk.Notebook(root)
set_notebook.pack(fill='x')

stage_notebook = ttk.Notebook(root)
stage_notebook.pack(fill='x')

part_notebook = ttk.Notebook(root)
part_notebook.pack(fill='x')

subpart_notebook = ttk.Notebook(root)
subpart_notebook.pack(fill='x')

content_text = tk.Text(root, wrap='word', height=20, font=("Segoe UI", 12))
content_text.pack(fill='both', expand=True)

set_tab_names = list(codex_structure.keys())

for set_name in set_tab_names:
    frame = ttk.Frame(set_notebook)
    set_notebook.add(frame, text=after_dash(set_name))

def clear_notebook(notebook):
    for tab_id in notebook.tabs():
        notebook.forget(tab_id)

def show_stages(set_index):
    clear_notebook(stage_notebook)
    clear_notebook(part_notebook)
    clear_notebook(subpart_notebook)
    if set_index < 1 or set_index - 1 >= len(set_tab_names):
        return
    set_name = set_tab_names[set_index - 1]
    for stage in codex_structure[set_name]:
        frame = ttk.Frame(stage_notebook)
        stage_notebook.add(frame, text=after_dash(stage))

def show_parts(set_index, stage_index):
    clear_notebook(part_notebook)
    clear_notebook(subpart_notebook)
    if set_index < 1 or set_index - 1 >= len(set_tab_names):
        return
    set_name = set_tab_names[set_index - 1]
    stage_names = list(codex_structure[set_name].keys())
    if not stage_names or stage_index >= len(stage_names):
        return
    stage_name = stage_names[stage_index]
    for part in codex_structure[set_name][stage_name]:
        frame = ttk.Frame(part_notebook)
        part_notebook.add(frame, text=after_dash(part))

def show_subparts(set_index, stage_index, part_index):
    clear_notebook(subpart_notebook)
    if set_index < 1 or set_index - 1 >= len(set_tab_names):
        return
    set_name = set_tab_names[set_index - 1]
    stage_names = list(codex_structure[set_name].keys())
    if stage_index >= len(stage_names):
        return
    stage_name = stage_names[stage_index]
    part_names = list(codex_structure[set_name][stage_name].keys())
    if part_index >= len(part_names):
        return
    part_name = part_names[part_index]
    subparts = codex_structure[set_name][stage_name][part_name]
    # Add "Home" tab first if present
    if "_home" in subparts:
        frame = ttk.Frame(subpart_notebook)
        subpart_notebook.add(frame, text="Home")
    for subpart in subparts:
        if subpart == "_home":
            continue
        frame = ttk.Frame(subpart_notebook)
        subpart_notebook.add(frame, text=after_dash(subpart))

def show_content(set_index, stage_index, part_index, subpart_index=None):
    content_text.delete(1.0, tk.END)
    if set_index < 1 or set_index - 1 >= len(set_tab_names):
        return
    set_name = set_tab_names[set_index - 1]
    stage_names = list(codex_structure[set_name].keys())
    if stage_index >= len(stage_names):
        return
    stage_name = stage_names[stage_index]
    part_names = list(codex_structure[set_name][stage_name].keys())
    if part_index >= len(part_names):
        return
    part_name = part_names[part_index]
    subparts = codex_structure[set_name][stage_name][part_name]
    if isinstance(subparts, str):
        content_text.insert(tk.END, subparts)
        return
    subpart_names = list(subparts.keys())
    # If subpart_index is None or 0, show "Home" content if present
    if subpart_index is None or subpart_index == 0:
        if "_home" in subparts:
            content_text.insert(tk.END, subparts["_home"])
            return
        elif subpart_names:
            content_text.insert(tk.END, subparts[subpart_names[0]])
            return
    if subpart_index is not None and subpart_index < len(subpart_names):
        subpart_key = subpart_names[subpart_index]
        if subpart_key == "_home":
            content_text.insert(tk.END, subparts["_home"])
        else:
            content_text.insert(tk.END, subparts[subpart_key])

set_notebook.bind("<<NotebookTabChanged>>", lambda e: [
    show_stages(set_notebook.index("current")),
    show_parts(set_notebook.index("current"), 0),
    show_content(set_notebook.index("current"), 0, 0, 0)
])

stage_notebook.bind("<<NotebookTabChanged>>", lambda e: [
    show_parts(set_notebook.index("current"), stage_notebook.index("current")),
    show_content(set_notebook.index("current"), stage_notebook.index("current"), 0, 0)
])

part_notebook.bind("<<NotebookTabChanged>>", lambda e: [
    show_subparts(set_notebook.index("current"), stage_notebook.index("current"), part_notebook.index("current")),
    show_content(set_notebook.index("current"), stage_notebook.index("current"), part_notebook.index("current"), 0)
])

subpart_notebook.bind("<<NotebookTabChanged>>", lambda e:
    show_content(set_notebook.index("current"), stage_notebook.index("current"), part_notebook.index("current"), subpart_notebook.index("current"))
)

show_stages(1)
show_parts(1, 0)
show_content(1, 0, 0, 0)

root.mainloop()
