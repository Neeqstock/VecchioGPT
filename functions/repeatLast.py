import json
import os
import pyperclip
import notifications
import prompt
from settingsManager import HISTORY_FILENAME, PROMPTS_FOLDER, SOUND_START_FILENAME, SOUND_FINISH_FILENAME


def repeat_last_prompt():
    print("Repeating last prompt on clipboard...")
    # read the last selected prompt file from the history file. It's a plain txt file with prompt file names. The file is in settingsManager HISTORY_FILENAME
    with open(HISTORY_FILENAME, "r") as file:
        last_prompt = file.readline().strip()
    
    clipboardContents = pyperclip.paste()

    notifications.popup('Running prompt "' + last_prompt + '"...', 3000)
    notifications.sound(SOUND_START_FILENAME)
    
    try:
        with open(
            os.path.join(PROMPTS_FOLDER, last_prompt),
            encoding="utf-8",
        ) as f:              
            data = json.load(f)
            result = prompt.run_prompt(last_prompt, data, clipboardContents)
    except FileNotFoundError:
        print(f"Error: unable to read the prompt file '{last_prompt}'.")

    pyperclip.copy(result)

    notifications.popup("Done!", 1500)
    notifications.sound(SOUND_FINISH_FILENAME)
