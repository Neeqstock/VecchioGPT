#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import json
import functions
import pyperclip
import sv_ttk
from PIL import ImageTk, Image
import codecs

global data
global key_entry_pairs

promptsDirectoryName = os.path.join(os.path.dirname(__file__), 'prompts') # Directory containing the prompts
promptsDictionary = {}
possible_prompts = []  # List of possible prompts
selected_index = -1  # Currently selected item index
selected_item = -1
tempPromptName = ""
key_entry_pairs = {} # A dictionary containing parameters keys mapped to tkinter Entries (from the notebook)

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
		

def on_tab(event):
	if listbox.size() > 0:
		global selected_index
		listbox.focus_set()
		listbox.selection_clear(0, tk.END)
		listbox.selection_set(selected_index)
		listbox.see(selected_index)  # Scroll to the selected index
		
def overwrite_additionalParams():
	for i in range(len(data["additionalParams"])):
		key = data["additionalParams"][i]["key"]
		data["additionalParams"][i]["value"] = key_entry_pairs[key].get()
	fileName = promptsDictionary.get(selected_item)
	# Seeks the path
	fullPath = os.path.join(os.path.dirname(__file__), "prompts/" + str(fileName))
	with open(fullPath, "w", encoding="utf-8") as file:
		json.dump(data, file, indent=4, ensure_ascii=False)

def on_select(event):
	global selected_index
	global selected_item

	# Overwrite additional params to set new defaults
	if len(key_entry_pairs) > 0:
		overwrite_additionalParams()
	
	print(f"Selected Prompt: {selected_item}")
	entry.delete(0, tk.END)
	entry.insert(0, selected_item)
	global global_response
	functions.play_sound(functions.SOUND_START)
	tempPromptName = selected_item  # Store the selected item so it can destroy the root window
	root.destroy()
	global_response = functions.chat_with_gpt(promptsDictionary.get(tempPromptName))
	pyperclip.copy(global_response)
	functions.play_sound(functions.SOUND_COMPLETED)


def on_enter(event):
	# print(f"selected_index: {selected_index}\n")
	# print(f"selected_item: {selected_item}\n")
	if selected_index >= 0:
		on_select(event)
		

def on_up_arrow(event):
	global selected_index
	global selected_item
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
	global selected_index
	global selected_item
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


def clear_notebook(notebook):
	for tab in notebook.winfo_children():
		tab.destroy()
	for i in range(notebook.index("end") - 1, -1, -1):
		notebook.forget(i)

def create_label_input_pairs(frame, additional_params):
	key_entry_pairs = {}
	for param in additional_params:
		key = param.get("key")
		value = param.get("value")

		# Create a Label
		label = ttk.Label(frame, text=key, font=("Montserrat", 12))
		label.grid(row=len(key_entry_pairs), column=0, sticky=tk.W, padx=10, pady=5)

		# Create an InputBox
		input_box = ttk.Entry(frame, width=40, font=("Montserrat", 12))
		input_box.insert(0, value)  # Set default text
		input_box.grid(row=len(key_entry_pairs), column=1, pady=5)

		key_entry_pairs[key] = input_box

	return key_entry_pairs

def display_info():
	global selected_index
	global data
	if selected_index >= 0:
		selected_item = listbox.get(selected_index)
		filename = promptsDictionary.get(selected_item)
		# clear_textboxes(notebook)
		# key_entry_pairs.clear()

		if filename:
			try:
				with open(os.path.join(promptsDirectoryName, filename), encoding="utf-8") as f:
					data = json.load(f)
					info_text = data['description']
					info_label.configure(text=info_text)

					additional_params = data.get("additionalParams")

					if additional_params:
						# Create a frame for labels and input boxes
						label_text_frame = ttk.Frame(root)
						label_text_frame.pack(pady=10)

						key_entry_pairs = create_label_input_pairs(label_text_frame, additional_params)

						# Store the key_entry_pairs in a global variable for future reference
						key_entry_pairs[selected_item] = key_entry_pairs

			except FileNotFoundError:
				info_label.configure(text=f"Info not available for {selected_item}")
		else:
			info_label.configure(text=f"Info not available for {selected_item}")


def show_window():
	bring_to_front(root)
	root.mainloop()


# GUI ENTRY CODE =========================================================================================

# Populate the prompts list
for filename in os.listdir(promptsDirectoryName):
	# Check if the file is a .json file
	if filename.endswith('.json'):
		# Open the .json file
		with open(f'{promptsDirectoryName}/{filename}', encoding="utf-8") as f:
			# Load the JSON data from the file
			data = json.load(f)
			# Strcat with prompt language
			promptString = "[" + data['language'] + "] " + data['promptName']
			# Append the 'promptName' and filename to the dictionary
			promptsDictionary[promptString] = filename
			# Append the 'promptName' to the list to be used by the GUI
			possible_prompts.append(promptString)

# Define the window
# Create the main window
root = tk.Tk()
root.title("VecchioGPT")

# Import Montserrat font
from tkinter import font as tkfont
montserrat_font = tkfont.nametofont("TkDefaultFont")
montserrat_font.configure(family="Montserrat")

# VECCHIOGPT IMAGE ==========
# Open VecchioGPT image using PIL
image = Image.open(os.path.join(os.path.dirname(__file__), "VecchioGPT.png"))
image = image.resize((80, 80))
# Convert the image to Tkinter PhotoImage
photo = ImageTk.PhotoImage(image)
# Create a label and set the image
vecchioLabel = tk.Label(root, image=photo)
# Pack the label to show it in the window
vecchioLabel.pack(pady=5)

entry = ttk.Entry(root, width=80, font=("Montserrat", 12))
entry.pack(pady=5)
entry.bind("<KeyRelease>", on_search)
# entry.bind("<Tab>", on_tab)
entry.focus_set()  # Set focus on the input text box
# Add space between Notebooks and Textbox
entry.pack(pady=(5, 5))


# Create and set the listbox with an adjusted width and borderless selection
listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=5, width=80,
					 font=("Montserrat", 12), bd=0, highlightthickness=0)
listbox.pack(pady=5)
listbox.bind("<Return>", on_enter)
listbox.bind("<Up>", on_up_arrow)
listbox.bind("<Down>", on_down_arrow)

# Add space between Textbox and listbox
listbox.pack(pady=(5, 5))

# Populate the listbox with possible prompts
for prompt in possible_prompts:
	listbox.insert(tk.END, prompt)

sv_ttk.set_theme("dark")

# Create and set the InfoBox label with an adjusted width and initial text
info_label = ttk.Label(root, text="", font=("Montserrat", 12, "italic"), wraplength=800)
info_label.pack(pady=(20, 20))

# Create a Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(pady=5)

# Main entry point ===================================
if __name__ == "__main__":
	show_window()
