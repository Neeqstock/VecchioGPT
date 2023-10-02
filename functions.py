#!/usr/bin/python3
import openai
import pyperclip
import os
import simpleaudio as sa
import json
from termcolor import colored

global global_response

# Settings ===============================================
SETTINGS_FILENAME = "settings.json"
NO_MODEL = "file_specific"
GPT_MODELS = ["gpt-3.5-turbo", "gpt-4", NO_MODEL]

# Model settings
def read_model():
    with open(SETTINGS_FILENAME, "r") as file:
        return json.load(file)['model']

def write_model(new_model):
    with open(SETTINGS_FILENAME, 'r') as f:
        data = json.load(f)
        data["model"] = new_model

    with open(SETTINGS_FILENAME, 'w') as f:
        json.dump(data, f, indent=4)

def next_model():
    selected_model = read_model()
    i = GPT_MODELS.index(selected_model)
    selected_model = ""
    if i + 1 < len(GPT_MODELS):
        selected_model = GPT_MODELS[i + 1]
    else:
        selected_model = GPT_MODELS[0]
    write_model(selected_model)
    print("Model changed to: " + selected_model)

# ===========================================================

# Sounds
SOUND_START = "start.wav"
SOUND_COMPLETED = "completed.wav"

# OpenAI key
def read_api_key(file_path):
    with open(file_path, 'r') as f:
        return f.readline().strip().split('=')[1]

api_key = read_api_key(os.path.join(os.path.dirname(__file__), 'openai_key.txt'))

# Initialize the OpenAI API client
openai.api_key = api_key

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def chat_with_gpt(file_name):
    # Get string from clipboard
    user_input = pyperclip.paste()
    # Seeks the file name
    fn = os.path.join(os.path.dirname(__file__), "prompts/" + str(file_name))
    # Loads the settings from fn file name
    promptJson = read_json_file(fn)
    # Replaces the § sign with the contents of the clipboard
    mergedPrompt = promptJson["prompt"].replace('§', user_input)

    # Create a dataset using GPT
    selected_model = read_model()
    if selected_model == NO_MODEL:
        selected_model = promptJson["gptModel"]

    # Print prompt name
    print("")
    print('"' + '\033[1m' + colored(promptJson["promptName"], "yellow") + '\033[0m' + '" using model "' + selected_model + '" on input:')
    print(user_input)

    response = openai.ChatCompletion.create(model=selected_model,
                                            messages=[{"role": "system", "content": promptJson["systemMessage"]},
                                            {"role": "user", "content": mergedPrompt}])

    ret = response["choices"][0]["message"]["content"]
    print("")
    print(colored('\033[1m' + "Answer" + '\033[0m', "green")  + ":")
    print(ret)
    print("")
    print("=============================================")
    print("")
    return ret


def play_sound(file_name):
    fn = os.path.join(os.path.dirname(__file__), file_name)
    wave_obj = sa.WaveObject.from_wave_file(fn)
    play_obj = wave_obj.play()
    play_obj.volume = 0.5  # Set volume to half the maximum
    play_obj.wait_done()  # Wait for the sound to finish playing

