#!/usr/bin/python3
import openai
import pyperclip
import os
import simpleaudio as sa
from pynput import keyboard
import json


global global_response

# Test Switch
testSwitch = False

# OpenAI key
api_key = "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"

# Initialize the OpenAI API client
openai.api_key = api_key

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def chat_with_gpt(prompt_number):
    # Get string from clipboard
    user_input = pyperclip.paste()
    # Seeks the file name                   
    fn = os.path.join(os.path.dirname(__file__), "prompts/" + str(prompt_number) + ".json")
    # Loads the settings from fn file name
    settings = read_json_file(fn)
    # Replaces the § sign with the contents of the clipboard
    mergedPrompt = settings["prompt"].replace('§', user_input)

    if(testSwitch == True):
        print(settings)

    # Print prompt name
    print('Computing prompt: "' + settings["promptName"] + '"...')

    # Create a dataset using GPT
    response = openai.ChatCompletion.create(model=settings["gptModel"],
                                            messages=[{"role": "system", "content": settings["systemMessage"]},
                                            {"role": "user", "content": mergedPrompt}])
    if(testSwitch == True):
        print(response)

    ret = response["choices"][0]["message"]["content"]
    print("Answer: " + ret)
    return ret


def play_sound(file_name):
    fn = os.path.join(os.path.dirname(__file__), file_name)
    wave_obj = sa.WaveObject.from_wave_file(fn)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait for the sound to finish playing


