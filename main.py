import tkinter as tk
from tkinter import messagebox, END
import json
from datetime import datetime
import os

FILE_NAME = "journal_data.json"

def load_entries():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_entries(entries):
    with open(FILE_NAME, "w") as f:
        json.dump(entries, f, indent=4)

def refresh_list(entries=None):
    listbox.delete(0, END)
    data = entries if entries else load_entries()
    for i, e in enumerate(data):
        listbox.insert(END, f"{i+1}. {e['title']} | {e.get('mood','Neutral')} | {e['date']}")

def add_entry():
    title = title_entry.get()
    content = text_area.get("1.0", END).strip()
    mood = mood_var.get()

    if title == "" or content == "":
        messagebox.showwarning("Warning", "All fields required")
        return

    entries = load_entries()

    entry = {
        "title": title,
        "content": content,
        "mood": mood,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    entries.append(entry)
    save_entries(entries)

    title_entry.delete(0, END)
    text_area.delete("1.0", END)
    refresh_list()

def view_entry(event):
    selection = listbox.curselection()
    if not selection:
        return

    index = selection[0]
    entries = load_entries()
    entry = entries[index]

    title_entry.delete(0, END)
    title_entry.insert(0, entry["title"])

    text_area.delete("1.0", END)
    text_area.insert(END, entry["content"])

    mood_var.set(entry["mood"])

def delete_entry():
    selection = listbox.curselection()
    if not selection:
        return

    entries = load_entries()
    entries.pop(selection[0])
    save_entries(entries)

    refresh_list()
    title_entry.delete(0, END)
    text_area.delete("1.0", END)

def search_entries():
    keyword = search_entry.get().lower()
    entries = load_entries()

    filtered = [
        e for e in entries
        if keyword in e["title"].lower()
        or keyword in e["content"].lower()
        or keyword in e["mood"].lower()
    ]

    refresh_list(filtered)

root = tk.Tk()
root.title("Personal Journal App")
root.geometry("700x600")
root.configure(bg="#f4f6f7")

tk.Label(root, text="Personal Journal", font=("Arial", 18, "bold"), bg="#f4f6f7").pack(pady=10)

tk.Label(root, text="Title", bg="#f4f6f7").pack()
title_entry = tk.Entry(root, width=70)
title_entry.pack(pady=5)

tk.Label(root, text="Journal Entry", bg="#f4f6f7").pack()
text_area = tk.Text(root, height=10, width=80)
text_area.pack(pady=5)

mood_var = tk.StringVar(value="Neutral")
tk.Label(root, text="Mood", bg="#f4f6f7").pack()
tk.OptionMenu(root, mood_var, "Happy", "Neutral", "Sad", "Excited", "Tired").pack(pady=5)

btn_frame = tk.Frame(root, bg="#f4f6f7")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Entry", width=15, command=add_entry).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete Entry", width=15, command=delete_entry).grid(row=0, column=1, padx=5)

tk.Label(root, text="Search", bg="#f4f6f7").pack()
search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=5)

tk.Button(root, text="Search Entries", command=search_entries).pack()

listbox = tk.Listbox(root, width=95, height=12)
listbox.pack(pady=15)
listbox.bind("<<ListboxSelect>>", view_entry)

refresh_list()

root.mainloop()