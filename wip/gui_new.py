#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from thefuzz import process
import os
import json
import pyperclip
import sv_ttk
from PIL import ImageTk, Image
import subprocess
import threading
import sys
import shutil

import notifications
from fixCodeblocks import fix_codeblocks
from history import get_sorted_history, history_put_on_top
from prompt import run_prompt
from readJson import read_json_file
from settingsManager import (
    HISTORY_FILENAME,
    PROMPTS_FOLDER,
    SOUND_FINISH_FILENAME,
    SOUND_START_FILENAME,
    TEMPLATES_FOLDER,
    VECCHIOGPT_LOGO_FILENAME,
)

keymap = {
    "enter": "<Return>",
    "create_prompt": "<F6>",
    "edit_prompt": "<F4>",
    "mouse_click": "<ButtonRelease-1>",
    "up": "<Up>",
    "down": "<Down>",
}

# Global variables
selected_index = -1
selected_item = -1
temp_prompt_name = ""
key_entry_pairs = {}
data = {}

# Title and window settings
root = tk.Tk()
root.title("VecchioGPT Prompt Selector")
root.maxsize(700, root.winfo_screenheight())

# Create a frame for the search bar and vecchio image
search_frame = tk.Frame(root)
search_frame.pack(pady=5)


# Vecchio label
def create_vecchio_label(parent):
    image = Image.open(VECCHIOGPT_LOGO_FILENAME)
    image = image.resize((55, 55))
    photo = ImageTk.PhotoImage(image)
    vecchio_label = tk.Label(parent, image=photo)
    vecchio_label.pack(side=tk.LEFT, padx=5)
    vecchio_label.image = photo
    return vecchio_label


vecchio_label = create_vecchio_label(search_frame)

# Search bar
entry = ttk.Entry(search_frame, width=80, font=("Montserrat", 12))
entry.insert(0, "Search prompts...")
entry.pack(side=tk.RIGHT, padx=5)
entry.bind("<FocusIn>", lambda e: clear_placeholder(e))
entry.bind("<FocusOut>", lambda e: add_placeholder(e))
entry.bind("<KeyRelease>", lambda e: on_search(e))
entry.bind(keymap["create_prompt"], lambda e: on_create(e))
entry.focus_set()

# Prompt listbox
listbox_frame = tk.Frame(root)
listbox_frame.pack(padx=5, pady=5, fill=tk.X)
listbox = tk.Listbox(
    listbox_frame,
    selectmode=tk.SINGLE,
    activestyle="none",
    height=5,
    width=80,
    font=("Montserrat", 12),
    bd=0,
    highlightthickness=0,
    exportselection=False,
)
listbox.pack(pady=5)
listbox.bind(keymap["enter"], lambda e: on_enter(e))
listbox.bind(keymap["create_prompt"], lambda e: on_create(e))
listbox.bind(keymap["edit_prompt"], lambda e: on_edit(e))
listbox.bind(keymap["up"], lambda e: on_up_arrow(e))
listbox.bind(keymap["down"], lambda e: on_down_arrow(e))
listbox.bind(keymap["mouse_click"], lambda e: listbox_mouse(e))

# Prompt info label
info_label = ttk.Label(root, text="", font=("Montserrat", 12, "italic"), wraplength=700)
info_label.pack(pady=(10, 10), padx=(5, 5), anchor="w")  # Align left

# Additional parameters frame
additional_params_frame = ttk.Frame(root)
additional_params_frame.pack(pady=10, fill=tk.X, expand=True)

sv_ttk.set_theme("dark")


def call():
    load_prompts()
    show_window()


def clear_placeholder(event):
    if entry.get() == "Search prompts...":
        entry.delete(0, tk.END)


def add_placeholder(event):
    if not entry.get():
        entry.insert(0, "Search prompts...")


def load_prompts():
    global possible_prompts
    for filename in os.listdir(PROMPTS_FOLDER):
        if filename.endswith(".json"):
            with open(f"{PROMPTS_FOLDER}/{filename}", encoding="utf-8") as f:
                data = json.load(f)
                category = (
                    f"[{data['category']}] "
                    if "category" in data and len(data["category"]) > 0
                    else ""
                )
                prompt_string = category + data["promptName"]
                prompts_dictionary[prompt_string] = filename
                possible_prompts.append(prompt_string)

    possible_prompts = get_sorted_history(prompts_dictionary, history)

    for prompt in possible_prompts:
        listbox.insert(tk.END, prompt)


def on_search(event):
    global selected_index
    selected_index = -1
    search_text = entry.get()
    if search_text:
        matches = process.extract(search_text, possible_prompts, limit=10)
        listbox.delete(0, tk.END)
        for match, score in matches:
            listbox.insert(tk.END, match)


def on_enter(event):
    if selected_index >= 0:
        on_select(event)


def on_edit(event):
    if selected_index >= 0:
        edit_prompt(event)
        load_prompts()


def on_create(event):
    example_prompt = "example_prompt.json"
    shutil.copyfile(
        f"{TEMPLATES_FOLDER}/{example_prompt}",
        f"{PROMPTS_FOLDER}/{example_prompt}",
    )
    load_prompts()


def listbox_mouse(event):
    global selected_index, selected_item
    selected_index = listbox.curselection()[0]
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(selected_index)
    listbox.activate(selected_index)
    selected_item = listbox.get(selected_index)
    display_info()


def on_up_arrow(event):
    global selected_index, selected_item
    if entry == root.focus_get():
        if listbox.size() > 0:
            selected_index = 0
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(selected_index)
            listbox.activate(selected_index)
            selected_index = listbox.curselection()[0]
            selected_item = listbox.get(selected_index)
            display_info()
        else:
            selected_index = -1
    elif selected_index > 0:
        selected_index -= 1
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(selected_index)
        listbox.activate(selected_index)
        selected_index = listbox.curselection()[0]
        selected_item = listbox.get(selected_index)
        display_info()


def on_down_arrow(event):
    global selected_index, selected_item
    if entry == root.focus_get():
        if listbox.size() > 0:
            selected_index = 0
            listbox.selection_clear(0, tk.END)
            listbox.selection_set(selected_index)
            listbox.activate(selected_index)
            selected_index = listbox.curselection()[0]
            selected_item = listbox.get(selected_index)
            display_info()
        else:
            selected_index = -1
    elif selected_index < listbox.size() - 1:
        selected_index += 1
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(selected_index)
        listbox.activate(selected_index)
        selected_index = listbox.curselection()[0]
        selected_item = listbox.get(selected_index)
        display_info()


def overwrite_additional_params():
    file_name = prompts_dictionary.get(selected_item)
    full_path = PROMPTS_FOLDER + str(file_name)

    original_json = read_json_file(full_path)

    if "additionalParams" in data:
        for i in range(len(data["additionalParams"])):
            key = data["additionalParams"][i]["key"]
            data["additionalParams"][i]["value"] = key_entry_pairs[key].get()
            if (
                "overwrite" in data["additionalParams"][i]
                and data["additionalParams"][i]["overwrite"]
            ):
                original_json["additionalParams"][i]["value"] = data[
                    "additionalParams"
                ][i]["value"]

    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(original_json, file, indent=4, ensure_ascii=False)


def edit_prompt(event):
    file_name = prompts_dictionary.get(selected_item)
    file_path = os.path.join(PROMPTS_FOLDER, file_name)

    def open_file():
        if sys.platform.startswith("linux"):
            subprocess.call(("xdg-open", file_path))
        elif sys.platform == "darwin":  # for macOS
            subprocess.call(("open", file_path))
        else:  # for Windows
            os.startfile(file_path)

    # Run the open_file function in a separate thread
    threading.Thread(target=open_file).start()


def on_select(event):
    global temp_prompt_name
    root.withdraw()
    if len(key_entry_pairs) > 0:
        overwrite_additional_params()

    temp_prompt_name = selected_item

    notifications.popup('Running prompt "' + temp_prompt_name + '"...', 3000)
    notifications.sound(SOUND_START_FILENAME)

    clipboard_contents = pyperclip.paste()
    global_response = run_prompt(
        prompts_dictionary.get(temp_prompt_name),
        data,
        clipboard_contents,
    )

    history_put_on_top(prompts_dictionary.get(temp_prompt_name), history)

    if "fix-codeblocks" in data and data["fix-codeblocks"]:
        global_response = fix_codeblocks(global_response)

    pyperclip.copy(global_response)

    notifications.popup("Done!", 1500)
    notifications.sound(SOUND_FINISH_FILENAME)

    # root.after(1500, root.destroy)


def create_label_input_pairs(frame, additional_params):
    global key_entry_pairs
    key_entry_pairs = {}
    for param in additional_params:
        key = param.get("key")
        value = param.get("value")

        label = ttk.Label(frame, text=key, font=("Montserrat", 12))
        label.grid(row=len(key_entry_pairs), column=0, sticky=tk.W, padx=10, pady=5)

        input_box = ttk.Entry(frame, font=("Montserrat", 12))
        input_box.insert(0, value)
        input_box.grid(
            row=len(key_entry_pairs), column=1, padx=10, pady=5, sticky=tk.EW
        )
        input_box.bind(keymap["enter"], lambda e: on_enter(e))
        input_box.bind(keymap["create_prompt"], lambda e: on_create(e))
        input_box.bind(keymap["edit_prompt"], lambda e: on_edit(e))

        key_entry_pairs[key] = input_box

    # Configure grid to make input boxes expand
    for i in range(len(key_entry_pairs)):
        frame.grid_columnconfigure(1, weight=1)


def display_info():
    global selected_item, data
    if selected_index >= 0:
        selected_item = listbox.get(selected_index)
        file_name = prompts_dictionary.get(selected_item)
        clear_frame(additional_params_frame)

        if file_name:
            try:
                with open(
                    os.path.join(PROMPTS_FOLDER, file_name),
                    encoding="utf-8",
                ) as f:
                    data = json.load(f)
                    info_text = data["description"]
                    info_label.configure(text=info_text)

                    # Make additional parameters frame
                    additional_params = data.get("additionalParams")
                    if additional_params:
                        additional_params_frame.pack(fill="both", expand=True)
                        create_label_input_pairs(
                            additional_params_frame, additional_params
                        )

            except FileNotFoundError:
                info_label.configure(text=f"Info not available for {selected_item}")
        else:
            info_label.configure(text=f"Info not available for {selected_item}")


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_forget()


def show_window():
    bring_to_front()
    root.mainloop()


def bring_to_front():
    root.lift()
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, "-topmost", False)


if __name__ == "__main__":
    call()
