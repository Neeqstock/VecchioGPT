import json
import os
import keyboard
import queue
import subprocess

import notifications
from settingsManager import (
    GPT_MODELS,
    SHORTCUTS,
    SOUND_FINISH_FILENAME,
    read_model,
    write_model,
)
from speech import (
    speech_from_clipboard,
    speech_prompt_on_clipboard,
    speech_prompt_on_nothing,
    speech_to_clipboard,
)

# Wait message string
wait_message = "Listening for keyboard shortcuts..."


def next_model():
    selected_model = read_model()
    if selected_model in GPT_MODELS:
        i = GPT_MODELS.index(selected_model)
    else:
        i = 0
    selected_model = ""
    if i + 1 < len(GPT_MODELS):
        selected_model = GPT_MODELS[i + 1]
    else:
        selected_model = GPT_MODELS[0]
    write_model(selected_model)
    print("Model changed to: " + selected_model)
    notifications.popup("Model changed to: " + selected_model, 3000)
    notifications.sound(SOUND_FINISH_FILENAME)


def key_gui_prompt():
    subprocess.call(["python", os.path.join(os.path.dirname(__file__), "gui.py")])
    print(wait_message)


def key_settings():
    subprocess.call(
        [
            "python",
            os.path.join(os.path.dirname(__file__), "settingsGui.py"),
        ]
    )
    print(wait_message)


def key_speech_prompt_clipboard():
    speech_prompt_on_clipboard()
    print(wait_message)


def key_speech_prompt_nothing():
    speech_prompt_on_nothing()
    print(wait_message)


def key_speech_clipboard():
    speech_to_clipboard()
    print(wait_message)


def key_tts():
    speech_from_clipboard()
    print(wait_message)


def print_intro_console():
    print("\033[1m" + "Welcome to VecchioGPT!" + "\033[0m")
    print("")
    print("\033[1m" + "Selected model: " + "\033[0m" + read_model())
    print("")
    print("\033[1m" + "Mapped shortcuts:" + "\033[0m")

    # Load shortcuts from JSON file and print them with descriptions
    with open("shortcuts.json", "r") as f:
        shortcuts = json.load(f)
        for shortcut in shortcuts["shortcuts"]:
            key = shortcut["key"]
            action = shortcut["action"]
            description = action_descriptions.get(action, "No description available.")
            print(f"{key}: {description}")
    print("")


# Mapping action names to descriptions
action_descriptions = {
    "key_gui_prompt": "calls the prompt selection GUI",
    "key_next_model": "switches to the next model",
    "key_speech_prompt_clipboard": "records an audio and uses it as a request (using clipboard content as context)",
    "key_speech_prompt_nothing": "records an audio and uses it as a prompt (without using clipboard content as context)",
    "key_speech_clipboard": "records an audio, transcribes it, and simply puts the text on clipboard",
    "key_tts": "reads the contents of the clipboard out loud",
    "key_abort": "abort recording or sound playback",
    "key_end_record": "stops and confirms the recording",
    "key_settings": "opens the settings GUI",
    "key_edit_prompt": "(while in the GUI) edit the currently selected prompt file, in system editor",
    "key_create_prompt": "(while in the GUI) create a new prompt file, with default name 'example_prompt.json'",
}


if __name__ == "__main__":
    print_intro_console()
    q = queue.Queue()
    print(wait_message)

    # Map actions to functions
    action_map = {
        "key_gui_prompt": key_gui_prompt,
        "key_next_model": next_model,
        "key_speech_prompt_clipboard": key_speech_prompt_clipboard,
        "key_speech_prompt_nothing": key_speech_prompt_nothing,
        "key_speech_clipboard": key_speech_clipboard,
        "key_tts": key_tts,
        "key_settings": key_settings,
    }

    # Set up hotkeys dynamically
    for action, key in SHORTCUTS.items():  # Iterate over the items in the dictionary
        if action in action_map:
            keyboard.add_hotkey(key, action_map[action])

    keyboard.wait()
