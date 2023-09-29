#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import json
import functions
import pyperclip

# Directory containing the prompts
promptsDirectoryName = os.path.join(os.path.dirname(__file__), 'prompts')
promptsDictionary = {}
possible_prompts = []  # List of possible prompts
selected_index = -1  # Currently selected item index
tempPromptName = ""

def bring_to_front(window):
    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(window.attributes, '-topmost', False)

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
        global global_response
        functions.play_sound(functions.soundStart)
        tempPromptName = selected_item  # Store the selected item so it can destroy the root window
        root.destroy()
        global_response = functions.chat_with_gpt(promptsDictionary.get(tempPromptName))
        pyperclip.copy(global_response)
        functions.play_sound(functions.soundCompleted)

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

def show_window():
    bring_to_front(root)
    root.mainloop()

# Populate the prompts list =================
for filename in os.listdir(promptsDirectoryName):
    # Check if the file is a .json file
    if filename.endswith('.json'):
        # Open the .json file
        with open(f'{promptsDirectoryName}/{filename}') as f:
            # Load the JSON data from the file
            data = json.load(f)
            # Append the 'promptName' and filename to the dictionary
            promptsDictionary[data['promptName']] = filename
            # Append the 'promptName' to the list to be used by the GUI
            possible_prompts.append(data['promptName'])

# Define the window ====================
# Create the main window
root = tk.Tk()
root.title("VecchioGPT")

# Apply a themed style for a modern look
style = ttk.Style()
style.theme_use("clam")

# Configure the style for a modern and stylish look
style.configure("TLabel", background="#3498db", foreground="white", padding=10)
style.configure("TEntry", background="#ecf0f1", padding=10)
style.configure("TListbox", background="#ecf0f1", padding=10)

# Create and set the label
label = ttk.Label(root, text="VecchioGPT", font=("Helvetica", 14))
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

# Populate the listbox with possible prompts
for prompt in possible_prompts:
    listbox.insert(tk.END, prompt)

# Main entry point ===================================
if __name__ == "__main__":
    show_window()
