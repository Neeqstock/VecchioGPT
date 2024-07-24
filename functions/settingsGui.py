import json
import tkinter as tk
from tkinter import messagebox, ttk
import sv_ttk
from settingsManager import SETTINGS_FILENAME


# Load JSON data from file
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON file: {e}")
        return {}


# Save JSON data to file
def save_json(file_path, data):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        messagebox.showinfo("Success", "Data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save JSON file: {e}")


# Update the JSON data based on user input
def update_data():
    for key in data.keys():
        if key == "sound":
            data[key] = sound_var.get()  # Get the value from the checkbox
        elif key == "popup":
            data[key] = popup_var.get()  # Get the selected value from the dropdown
        else:
            data[key] = entries[key].get()  # For other entries

    save_json(SETTINGS_FILENAME, data)
    root.destroy()  # Close the GUI after saving


# Create the main window
root = tk.Tk()
root.title("VecchioGPT Settings Editor")

sv_ttk.set_theme("dark")

# Load the JSON data
data = load_json(SETTINGS_FILENAME)

# Create a dictionary to hold the entry widgets
entries = {}

# Create a variable for the sound checkbox
sound_var = tk.BooleanVar(value=data.get("sound", False))

# Create a variable for the popup selection
popup_var = tk.StringVar(value=data.get("popup", "off"))

# Create labels and inputs for each key in the JSON data
row = 0  # Initialize row counter for grid layout
for key in data.keys():
    label = tk.Label(
        root, text=key, font=("Montserrat", 12), anchor="w"
    )  # Set font and left align
    label.grid(row=row, column=0, padx=5, pady=5, sticky="w")  # Place label in grid

    if key == "sound":
        # Create a checkbox for the sound setting
        checkbox = ttk.Checkbutton(root, variable=sound_var)
        checkbox.grid(
            row=row, column=1, padx=5, pady=5, sticky="w"
        )  # Place checkbox in grid
    elif key == "popup":
        # Create a dropdown (combobox) for the popup setting
        popup_options = ["off", "vecchio", "system"]
        popup_menu = ttk.Combobox(
            root, textvariable=popup_var, values=popup_options, state="readonly"
        )
        popup_menu.grid(
            row=row, column=1, padx=5, pady=5, sticky="ew"
        )  # Place dropdown in grid
    else:
        # Create a regular Entry for other keys
        entry = ttk.Entry(root, font=("Montserrat", 12))  # Use ttk.Entry
        entry.insert(0, data[key])  # Insert the current value
        entry.grid(
            row=row, column=1, padx=5, pady=5, sticky="ew"
        )  # Place entry in grid
        entries[key] = entry

    row += 1  # Move to the next row

# Create a save button
save_button = tk.Button(root, text="Save Changes", command=update_data)
save_button.grid(row=row, column=0, columnspan=2, pady=20)  # Center the save button

# Bind the Enter key to the update_data function
root.bind("<Return>", lambda event: update_data())

# Set focus on the first entry and the window upon start
if entries:
    entries[list(data.keys())[0]].focus_set()  # Focus on the first entry
root.focus_force()  # Focus on the window

# Set minimum width and allow resizing
root.minsize(400, 400)
root.resizable(False, False)


def bring_to_front():
    root.lift()
    root.attributes("-topmost", True)
    root.after_idle(root.attributes, "-topmost", False)


# Start the Tkinter event loop
def show_window():
    bring_to_front()
    root.mainloop()


show_window()
