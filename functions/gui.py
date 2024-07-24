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
    SHORTCUTS,
    SOUND_FINISH_FILENAME,
    SOUND_START_FILENAME,
    TEMPLATES_FOLDER,
    VECCHIOGPT_LOGO_FILENAME,
)

keymap = {
    "enter": "<Return>",
    "mouse_click": "<ButtonRelease-1>",
    "up": "<Up>",
    "down": "<Down>",
}


class VecchioGPTGUI:
    def __init__(self):
        self.directory = os.path.join(os.path.dirname(__file__))
        self.history = HISTORY_FILENAME
        self.prompts_dictionary = {}
        self.possible_prompts = []
        self.selected_index = -1
        self.selected_item = -1
        self.temp_prompt_name = ""
        self.key_entry_pairs = {}
        self.data = {}

        # Title and window settings
        self.root = tk.Tk()
        self.root.title("VecchioGPT Prompt Selector")
        self.root.maxsize(700, self.root.winfo_screenheight())

        # Create a frame for the search bar and vecchio image
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(pady=5)

        # Vecchio label
        self.vecchio_label = self.create_vecchio_label(self.search_frame)

        # Search bar
        self.entry = ttk.Entry(self.search_frame, width=80, font=("Montserrat", 12))
        self.entry.insert(0, "Search prompts...")
        self.entry.pack(side=tk.RIGHT, padx=5)
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.add_placeholder)
        self.entry.bind("<KeyRelease>", self.on_search)
        self.entry.bind(SHORTCUTS["key_create_prompt"], self.on_create)
        self.entry.focus_set()

        # Prompt listbox
        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.pack(padx=5, pady=5, fill=tk.X)
        self.listbox = tk.Listbox(
            self.listbox_frame,
            selectmode=tk.SINGLE,
            activestyle="none",
            height=5,
            width=80,
            font=("Montserrat", 12),
            bd=0,
            highlightthickness=0,
            exportselection=False,
        )
        self.listbox.pack(pady=5)
        self.listbox.bind(keymap["enter"], self.on_enter)
        self.listbox.bind(SHORTCUTS["key_create_prompt"], self.on_create)
        self.listbox.bind(SHORTCUTS["key_edit_prompt"], self.on_edit)
        self.listbox.bind(keymap["up"], self.on_up_arrow)
        self.listbox.bind(keymap["down"], self.on_down_arrow)
        self.listbox.bind(keymap["mouse_click"], self.listbox_mouse)

        # Prompt info label
        self.info_label = ttk.Label(
            self.root, text="", font=("Montserrat", 12, "italic"), wraplength=700
        )
        self.info_label.pack(pady=(10, 10), padx=(5, 5), anchor="w")  # Align left

        # Additional parameters frame
        self.additional_params_frame = ttk.Frame(self.root)
        self.additional_params_frame.pack(pady=10, fill=tk.X, expand=True)

        sv_ttk.set_theme("dark")

        self.call()

    def call(self):
        self.load_prompts()
        self.show_window()

    def create_vecchio_label(self, parent):
        image = Image.open(VECCHIOGPT_LOGO_FILENAME)
        image = image.resize((55, 55))
        photo = ImageTk.PhotoImage(image)
        vecchio_label = tk.Label(parent, image=photo)
        vecchio_label.pack(side=tk.LEFT, padx=5)
        vecchio_label.image = photo
        return vecchio_label

    def clear_placeholder(self, event):
        if self.entry.get() == "Search prompts...":
            self.entry.delete(0, tk.END)

    def add_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, "Search prompts...")

    def load_prompts(self):
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
                    self.prompts_dictionary[prompt_string] = filename
                    self.possible_prompts.append(prompt_string)

        self.possible_prompts = get_sorted_history(
            self.prompts_dictionary, self.history
        )

        for prompt in self.possible_prompts:
            self.listbox.insert(tk.END, prompt)

    def on_search(self, event):
        self.selected_index = -1
        search_text = self.entry.get()
        if search_text:
            matches = process.extract(search_text, self.possible_prompts, limit=10)
            self.listbox.delete(0, tk.END)
            for match, score in matches:
                self.listbox.insert(tk.END, match)

    def on_enter(self, event):
        if self.selected_index >= 0:
            self.on_select(event)

    def on_edit(self, event):
        if self.selected_index >= 0:
            self.edit_prompt(event)
            self.load_prompts()

    def on_create(self, event):
        example_prompt = "example_prompt.json"
        shutil.copyfile(
            f"{TEMPLATES_FOLDER}/{example_prompt}",
            f"{PROMPTS_FOLDER}/{example_prompt}",
        )
        self.load_prompts()

    def listbox_mouse(self, event):
        self.selected_index = self.listbox.curselection()[0]
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.selected_index)
        self.listbox.activate(self.selected_index)
        self.selected_item = self.listbox.get(self.selected_index)
        self.display_info()

    def on_up_arrow(self, event):
        if self.entry == self.root.focus_get():
            if self.listbox.size() > 0:
                self.selected_index = 0
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(self.selected_index)
                self.listbox.activate(self.selected_index)
                self.selected_index = self.listbox.curselection()[0]
                self.selected_item = self.listbox.get(self.selected_index)
                self.display_info()
            else:
                self.selected_index = -1
        elif self.selected_index > 0:
            self.selected_index -= 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.selected_index)
            self.listbox.activate(self.selected_index)
            self.selected_index = self.listbox.curselection()[0]
            self.selected_item = self.listbox.get(self.selected_index)
            self.display_info()

    def on_down_arrow(self, event):
        if self.entry == self.root.focus_get():
            if self.listbox.size() > 0:
                self.selected_index = 0
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(self.selected_index)
                self.listbox.activate(self.selected_index)
                self.selected_index = self.listbox.curselection()[0]
                self.selected_item = self.listbox.get(self.selected_index)
                self.display_info()
            else:
                self.selected_index = -1
        elif self.selected_index < self.listbox.size() - 1:
            self.selected_index += 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.selected_index)
            self.listbox.activate(self.selected_index)
            self.selected_index = self.listbox.curselection()[0]
            self.selected_item = self.listbox.get(self.selected_index)
            self.display_info()

    def overwrite_additional_params(self):
        file_name = self.prompts_dictionary.get(self.selected_item)
        full_path = PROMPTS_FOLDER + str(file_name)

        original_json = read_json_file(full_path)

        if "additionalParams" in self.data:
            for i in range(len(self.data["additionalParams"])):
                key = self.data["additionalParams"][i]["key"]
                self.data["additionalParams"][i]["value"] = self.key_entry_pairs[
                    key
                ].get()
                if (
                    "overwrite" in self.data["additionalParams"][i]
                    and self.data["additionalParams"][i]["overwrite"]
                ):
                    original_json["additionalParams"][i]["value"] = self.data[
                        "additionalParams"
                    ][i]["value"]

        with open(full_path, "w", encoding="utf-8") as file:
            json.dump(original_json, file, indent=4, ensure_ascii=False)

    def edit_prompt(self, event):
        file_name = self.prompts_dictionary.get(self.selected_item)
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

    def on_select(self, event):

        self.root.withdraw()
        if len(self.key_entry_pairs) > 0:
            self.overwrite_additional_params()

        self.temp_prompt_name = self.selected_item

        notifications.popup('Running prompt "' + self.temp_prompt_name + '"...', 3000)
        notifications.sound(SOUND_START_FILENAME)

        clipboardContents = pyperclip.paste()
        global_response = run_prompt(
            self.prompts_dictionary.get(self.temp_prompt_name),
            self.data,
            clipboardContents,
        )

        history_put_on_top(
            self.prompts_dictionary.get(self.temp_prompt_name), self.history
        )

        if "fix-codeblocks" in self.data and self.data["fix-codeblocks"]:
            global_response = fix_codeblocks(global_response)

        pyperclip.copy(global_response)

        notifications.popup("Done!", 1500)
        notifications.sound(SOUND_FINISH_FILENAME)

        self.root.after(1500, self.root.destroy)

    def create_label_input_pairs(self, frame, additional_params):
        self.key_entry_pairs = {}
        for param in additional_params:
            key = param.get("key")
            value = param.get("value")

            label = ttk.Label(frame, text=key, font=("Montserrat", 12))
            label.grid(
                row=len(self.key_entry_pairs), column=0, sticky=tk.W, padx=10, pady=5
            )

            input_box = ttk.Entry(frame, font=("Montserrat", 12))
            input_box.insert(0, value)
            input_box.grid(
                row=len(self.key_entry_pairs), column=1, padx=10, pady=5, sticky=tk.EW
            )
            input_box.bind(keymap["enter"], self.on_enter)
            input_box.bind(SHORTCUTS["key_create_prompt"], self.on_create)
            input_box.bind(SHORTCUTS["key_edit_prompt"], self.on_edit)

            self.key_entry_pairs[key] = input_box

        # Configure grid to make input boxes expand
        for i in range(len(self.key_entry_pairs)):
            frame.grid_columnconfigure(1, weight=1)

    def display_info(self):
        if self.selected_index >= 0:
            self.selected_item = self.listbox.get(self.selected_index)
            file_name = self.prompts_dictionary.get(self.selected_item)
            self.clear_frame(self.additional_params_frame)

            if file_name:
                try:
                    with open(
                        os.path.join(PROMPTS_FOLDER, file_name),
                        encoding="utf-8",
                    ) as f:
                        self.data = json.load(f)
                        info_text = self.data["description"]
                        self.info_label.configure(text=info_text)

                        # Make additional parameters frame
                        additional_params = self.data.get("additionalParams")
                        if additional_params:
                            self.additional_params_frame.pack(fill="both", expand=True)
                            self.create_label_input_pairs(
                                self.additional_params_frame, additional_params
                            )

                except FileNotFoundError:
                    self.info_label.configure(
                        text=f"Info not available for {self.selected_item}"
                    )
            else:
                self.info_label.configure(
                    text=f"Info not available for {self.selected_item}"
                )

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        frame.pack_forget()

    def show_window(self):
        self.bring_to_front()
        self.root.mainloop()

    def bring_to_front(self):
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after_idle(self.root.attributes, "-topmost", False)


if __name__ == "__main__":
    VecchioGPTGUI()
