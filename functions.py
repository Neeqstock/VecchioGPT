#!/usr/bin/python3
import openai
import pyperclip
import os
import simpleaudio as sa
import json
from termcolor import colored


global global_response

# Sounds
soundStart = "start.wav"
soundCompleted = "completed.wav"

# TestSwitch (debug)
testSwitch = False

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
    settings = read_json_file(fn)
    # Replaces the § sign with the contents of the clipboard
    mergedPrompt = settings["prompt"].replace('§', user_input)

    if(testSwitch == True):
        print(settings)

    # Print prompt name
    print()
    print('"' + '\033[1m' + colored(settings["promptName"], "yellow") + '\033[0m' + '" on input:')
    print(user_input)

    # Create a dataset using GPT
    response = openai.ChatCompletion.create(model=settings["gptModel"],
                                            messages=[{"role": "system", "content": settings["systemMessage"]},
                                            {"role": "user", "content": mergedPrompt}])
    if(testSwitch == True):
        print(response)

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
    play_obj.wait_done()  # Wait for the sound to finish playing


