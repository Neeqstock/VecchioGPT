#!/usr/bin/python3
import openai
import pyperclip
import os
import platform
import simpleaudio as sa
from pynput import keyboard
import json


global global_response

# OpenAI key
api_key = "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"
# Initialize the OpenAI API client
openai.api_key = api_key


def on_key_press(key):
    global global_response
    global_response = chat_with_gpt(key.char)
    return False


def intercept_next_keystroke():
    # Create a keyboard listener
    listener = keyboard.Listener(on_press=on_key_press)

    # Start listening for the next keystroke
    with listener:
        listener.join()


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def chat_with_gpt(prompt_number):
    # Define the system message
    user_input = pyperclip.paste()                          # Get string from clipboard
    settings = read_json_file("prompts/" + str(prompt_number) + ".json")

    mergedPrompt = settings["prompt"].replace('§', user_input)

    print(settings)

    # Create a dataset using GPT
    response = openai.ChatCompletion.create(model=settings["gptModel"],
                                            messages=[{"role": "system", "content": settings["systemMessage"]},
                                            {"role": "user", "content": mergedPrompt}])
    print(response)

    return response["choices"][0]["message"]["content"]


def play_completion_sound():
    wave_obj = sa.WaveObject.from_wave_file('completed.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait for the sound to finish playing


def main():
    print("Write a keystroke to be captured by the script...")
    intercept_next_keystroke()
    pyperclip.copy(global_response)                                # Save output to clipboard
    play_completion_sound()


if __name__ == "__main__":
    main()




