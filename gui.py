#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# List of possible prompts
possible_prompts = [
    "Hello, how are you?",
    "What's the weather like today?",
    "Tell me a joke.",
    "What's your name?",
    "What's the capital of France?",
    "How does photosynthesis work?",
    "What's the meaning of life?"
]

selected_index = -1  # Currently selected item index

def on_search(event):
    global selected_index
    search_text = entry.get()
    if search_text:
        # Use fuzzy matching to find similar prompts
        matches = process.extract(search_text, possible_prompts, scorer=fuzz.token_sort_ratio, limit=5)
        listbox.delete(0, tk.END)
        for match, score in matches:
            listbox.insert(tk.END, match)
        selected_index = -1  # Reset selected index

def on_select(event):
    if listbox.curselection():
        global selected_index
        selected_index = listbox.curselection()[0]
        selected_item = listbox.get(selected_index)
        print(f"Selected Prompt: {selected_item}")
        entry.delete(0, tk.END)
        entry.insert(0, selected_item)

def on_tab(event):
    if listbox.size() > 0:
        listbox.focus_set()
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(selected_index)

def on_enter(event):
    if selected_index >= 0:
        on_select(event)

def on_up_arrow(event):
    global selected_index
    if selected_index > 0:
        selected_index -= 1
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(selected_index)
        listbox.activate(selected_index)

def on_down_arrow(event):
    global selected_index
    if selected_index < listbox.size() - 1:
        selected_index += 1
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(selected_index)
        listbox.activate(selected_index)

# Create the main window
root = tk.Tk()
root.title("Modern GUI")

# Apply a themed style for a modern look
style = ttk.Style()
style.theme_use("clam")

# Create and set the label
label = ttk.Label(root, text="This is my GUI", font=("Helvetica", 14))
label.pack(pady=10)

# Create and set the entry widget
entry = ttk.Entry(root, width=30, font=("Helvetica", 12))
entry.pack(pady=5)
entry.bind("<KeyRelease>", on_search)
entry.bind("<Tab>", on_tab)
entry.focus_set()  # Set focus on the input text box

# Create and set the listbox
listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=5, font=("Helvetica", 12))
listbox.pack(pady=5)
listbox.bind("<Return>", on_enter)
listbox.bind("<Up>", on_up_arrow)
listbox.bind("<Down>", on_down_arrow)

# Start the GUI event loop
root.mainloop()

