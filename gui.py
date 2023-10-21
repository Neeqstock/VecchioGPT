#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from thefuzz import fuzz
from thefuzz import process
import os
import sys
import json
import functions
import pyperclip
import sv_ttk
from PIL import ImageTk, Image
import codecs

# sv_ttk.set_theme("dark")
def popup_notification(message, expire_time=1500):
    if sys.platform.startswith('linux'):
        os.system(f'notify-send --expire-time={expire_time} "{message}"')
    if sys.platform.startswith('darwin'):
        os.system(f"osascript -e 'display notification \"{message}\" with title \"Notification\"'")
    elif sys.platform.startswith('win'):
        os.system(f"powershell -Command \"Add-Type -TypeDefinition @'\
                using System; \
                using System.Runtime.InteropServices; \
                public class MessageBox {{ \
                    [DllImport(\"user32.dll\", SetLastError = true)] \
                    public static extern int MessageBox(IntPtr hWnd, String text, String caption, uint type); \
                    public static void Show(string message) {{ \
                        MessageBox(IntPtr.Zero, message, \"Notification\", 0x40); \
                    }} \
                }} \
            '@; [MessageBox]::Show('{message}')\"")
    else:
        print(message)



class VecchioGPTGUI:
    """
    A GUI application that interfaces with ChatGPT.

    Attributes:
    - prompts_directory: The directory where prompt files are stored.
    - prompts_dictionary: A dictionary mapping prompt names to their corresponding filenames.
    - possible_prompts: A list of possible prompt names.
    - selected_index: The index of the currently selected prompt in the listbox.
    - selected_item: The currently selected prompt name.
    - temp_prompt_name: A temporary variable to store the selected prompt name.
    - key_entry_pairs: A dictionary mapping keys to corresponding input boxes.
    - data: A dictionary to store the data loaded from the selected prompt file.
    - root: The main Tkinter window.

    Methods:
    - __init__(self): Initializes the GUI application.
    - create_vecchio_label(self): Creates and returns a label displaying the VecchioGPT logo.
    - load_prompts(self): Loads the available prompts from the prompts directory.
    - bring_to_front(self): Brings the GUI window to the front.
    - on_search(self, event): Handles the search event and updates the listbox with matching prompts.
    - on_enter(self, event): Handles the enter event and selects the currently highlighted prompt.
    - on_up_arrow(self, event): Handles the up arrow event and moves the selection up in the listbox.
    - on_down_arrow(self, event): Handles the down arrow event and moves the selection down in the listbox.
    - overwrite_additional_params(self): Overwrites the additional parameters in the selected prompt file with the values entered in the input boxes.
    - on_select(self, event): Handles the select event and closes the GUI, copying the response to the clipboard.
    - create_label_input_pairs(self, frame, additional_params): Creates label-input pairs for the additional parameters in the selected prompt.
    - display_info(self): Displays the information and additional parameters for the selected prompt.
    - clear_frame(self, frame): Clears the contents of a Tkinter frame.
    - bring_to_front(self): Brings the GUI window to the front.
    - show_window(self): Shows the GUI window.

    """
    def __init__(self):
        """
        Initializes the GUI application.
        """
        self.prompts_directory = os.path.join(os.path.dirname(__file__), 'prompts')
        self.history = os.path.join(os.path.dirname(__file__), ".history")
        self.prompts_dictionary = {}
        self.possible_prompts = []
        self.selected_index = -1
        self.selected_item = -1
        self.temp_prompt_name = ""
        self.key_entry_pairs = {}
        self.data = {}

        self.root = tk.Tk()
        self.root.title("VecchioGPT")
        self.vecchio_label = self.create_vecchio_label()

        # Inputbox for fuzzy search of the prompts
        self.entry = ttk.Entry(self.root, width=80, font=("Montserrat", 12))
        self.entry.pack(pady=5)
        self.entry.bind("<KeyRelease>", self.on_search)
        self.entry.focus_set()

        # Listbox containing prompts
        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.pack(padx=5, pady=5, fill=tk.X)

        self.listbox = tk.Listbox(self.listbox_frame, selectmode=tk.SINGLE, height=5, width=80,
                                  font=("Montserrat", 12), bd=0, highlightthickness=0, exportselection=False)
        self.listbox.pack(pady=5)
        self.listbox.bind("<Return>", self.on_enter)
        self.listbox.bind("<Up>", self.on_up_arrow)
        self.listbox.bind("<Down>", self.on_down_arrow)
        self.listbox.bind("<ButtonRelease-1>", self.listbox_mouse)

        self.listbox.pack(side=tk.LEFT)

        # Scrollbar for the listbox
        self.listbox_scrollbar = tk.Scrollbar(self.listbox_frame, takefocus=0)
        self.listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_scrollbar.config(width=6.5)
        # Configure the listbox to use the scrollbar
        self.listbox.config(yscrollcommand=self.listbox_scrollbar.set)
        self.listbox_scrollbar.config(command=self.listbox.yview)




        # Label box containing the description of the prompt 
        self.info_label = ttk.Label(self.root, text="", font=("Montserrat", 12, "italic"), wraplength=800)
        self.info_label.pack(pady=(20, 20))

        self.label_text_frame = ttk.Frame(self.root)
        self.label_text_frame.pack(pady=10)
        self.load_prompts()
        sv_ttk.set_theme("dark")

        self.show_window()

    def create_vecchio_label(self):
        """
        Creates and returns a label displaying the VecchioGPT logo.

        Returns:
        - vecchio_label: A Tkinter label displaying the VecchioGPT logo.
        """
        image = Image.open(os.path.join(os.path.dirname(__file__), "VecchioGPT.png"))
        image = image.resize((80, 80))
        photo = ImageTk.PhotoImage(image)
        vecchio_label = tk.Label(self.root, image=photo)
        vecchio_label.pack(pady=5)
        vecchio_label.image = photo
        return vecchio_label

    def load_prompts(self):
        """
        Loads the available prompts from the prompts directory.
        """
        for filename in os.listdir(self.prompts_directory):
            if filename.endswith('.json'):
                with open(f'{self.prompts_directory}/{filename}', encoding="utf-8") as f:
                    data = json.load(f)
                    language = f"[{data['language']}] " if 'language' in data and len(data['language']) > 0 else ""
                    prompt_string = language + data['promptName']
                    self.prompts_dictionary[prompt_string] = filename
                    self.possible_prompts.append(prompt_string)

        # print(f"possible_prompts: {self.possible_prompts}\n")
        # print(f"prompts_dictionary: {self.prompts_dictionary}\n")
        self.possible_prompts = functions.sort_prompts_history(self.possible_prompts, f'{self.prompts_directory}/{self.history}')

        for prompt in self.possible_prompts:
            self.listbox.insert(tk.END, prompt)

    def bring_to_front(self):
        """
        Brings the GUI window to the front.
        """
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)

    def on_search(self, event):
        """
        Handles the search event and updates the listbox with matching prompts.

        Parameters:
        - event: The search event triggered by the user.
        """
        self.selected_index = -1
        search_text = self.entry.get()
        if search_text:
            matches = process.extract(search_text, self.possible_prompts, limit=10)
            self.listbox.delete(0, tk.END)
            for match, score in matches:
                self.listbox.insert(tk.END, match)

    def on_enter(self, event):
        """
        Handles the enter event and selects the currently highlighted prompt.

        Parameters:
        - event: The enter event triggered by the user.
        """
        if self.selected_index >= 0:
            self.on_select(event)

    def listbox_mouse(self, event):
        self.selected_index = self.listbox.curselection()[0]
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.selected_index)
        self.listbox.activate(self.selected_index)
        self.selected_item = self.listbox.get(self.selected_index)
        self.display_info()


    def on_up_arrow(self, event):
        """
        Handles the up arrow event and moves the selection up in the listbox.

        Parameters:
        - event: The up arrow event triggered by the user.
        """
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
        """
        Handles the down arrow event and moves the selection down in the listbox.

        Parameters:
        - event: The down arrow event triggered by the user.
        """
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
        """
        Overwrites the additional parameters in the selected prompt file with the values entered in the input boxes.
        """
        file_name = self.prompts_dictionary.get(self.selected_item)
        full_path = os.path.join(os.path.dirname(__file__), "prompts/" + str(file_name))

        original_json = functions.read_json_file(full_path)

        if "additionalParams" in self.data:
            for i in range(len(self.data["additionalParams"])):
                key = self.data["additionalParams"][i]["key"]
                self.data["additionalParams"][i]["value"] = self.key_entry_pairs[key].get()
                # Only overwrite prompts if their `overwrite` field is present and is set to `true`
                if "overwrite" in self.data["additionalParams"][i] and self.data["additionalParams"][i]["overwrite"]:
                    original_json["additionalParams"][i]["value"] = self.data["additionalParams"][i]["value"]

        with open(full_path, "w", encoding="utf-8") as file:
            json.dump(original_json, file, indent=4, ensure_ascii=False)

    def on_select(self, event):
        """
        Handles the select event and closes the GUI, copying the response to the clipboard.

        Parameters:
        - event: The select event triggered by the user.
        """
        if len(self.key_entry_pairs) > 0:
            self.overwrite_additional_params()

        self.temp_prompt_name = self.selected_item

        notification_type = functions.read_notification()
        # Notifications of the prompt being run 
        if "window" not in notification_type:
            self.root.destroy()
        if "sound" in notification_type:
            functions.play_sound(functions.SOUND_START)
        if "popup" in notification_type:
            popup_notification("Running prompt ...", 3000)

        # Get string from clipboard
        clipboardContents = pyperclip.paste()
        global_response = functions.chat_with_gpt(self.prompts_dictionary.get(self.temp_prompt_name), self.data, clipboardContents)
        # print(f"self.data: {self.data}")
        pyperclip.copy(global_response)
        
        # Run second ChatGPT call if LaTeX citations have to be fixed 
        if "fix-latex-citations" in self.data and self.data["fix-latex-citations"]:
                print("Fixing LaTeX citations...\n")
                functions.fix_latex_citations(clipboardContents, global_response)

        # Notifications of the job being completed 
        if "window" in notification_type:
            self.root.destroy()
        if "popup" in notification_type:
            popup_notification("Done!", 1500)
        if "sound" in notification_type:
            functions.play_sound(functions.SOUND_COMPLETED)

    def create_label_input_pairs(self, frame, additional_params):
        """
        Creates label-input pairs for the additional parameters in the selected prompt.

        Parameters:
        - frame: The Tkinter frame to add the label-input pairs to.
        - additional_params: A list of additional parameters in the selected prompt.
        """
        self.key_entry_pairs = {}
        for param in additional_params:
            key = param.get("key")
            value = param.get("value")

            label = ttk.Label(frame, text=key, font=("Montserrat", 12))
            label.grid(row=len(self.key_entry_pairs), column=0, sticky=tk.W, padx=10, pady=5)

            input_box = ttk.Entry(frame, width=40, font=("Montserrat", 12))
            input_box.insert(0, value)
            input_box.grid(row=len(self.key_entry_pairs), column=1, pady=5)
            input_box.bind("<Return>", self.on_enter)

            self.key_entry_pairs[key] = input_box

    def display_info(self):
        """
        Displays the information and additional parameters for the selected prompt.
        """
        if self.selected_index >= 0:
            self.selected_item = self.listbox.get(self.selected_index)
            file_name = self.prompts_dictionary.get(self.selected_item)
            self.clear_frame(self.label_text_frame)

            if file_name:
                try:
                    with open(os.path.join(self.prompts_directory, file_name), encoding="utf-8") as f:
                        self.data = json.load(f)
                        info_text = self.data['description']
                        self.info_label.configure(text=info_text)

                        additional_params = self.data.get("additionalParams")
                        if additional_params:
                            self.label_text_frame = ttk.Frame(self.root)
                            self.label_text_frame.pack(pady=10)

                            self.create_label_input_pairs(self.label_text_frame, additional_params)

                except FileNotFoundError:
                    self.info_label.configure(text=f"Info not available for {self.selected_item}")
            else:
                self.info_label.configure(text=f"Info not available for {self.selected_item}")

    def clear_frame(self, frame):
        """
        Clears the contents of a Tkinter frame.

        Parameters:
        - frame: The Tkinter frame to clear.
        """
        frame.destroy()

    def bring_to_front(self):
        """
        Brings the GUI window to the front.
        """
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)

    def show_window(self):
        """
        Shows the GUI window.
        """
        self.bring_to_front()
        self.root.mainloop()


if __name__ == "__main__":
    VecchioGPTGUI()
