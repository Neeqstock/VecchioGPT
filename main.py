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

def send_system_alert(message, expire_time = 1500):
    # Determine the platform (Linux or Windows)
    current_platform = platform.system()

    try:
        # Send a system alert based on the platform
        if current_platform == "Linux":
            os.system(f'notify-send --expire-time={expire_time} "{message}"')
        else:
            print("Unsupported platform. Cannot send system alert.")
    except Exception as e:
        print(f"Error sending system alert: {e}")


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
    fn = os.path.join(os.path.dirname(__file__), "prompts/" + str(prompt_number) + ".json")
    settings = read_json_file(fn)

    mergedPrompt = settings["prompt"].replace('§', user_input)

    print(settings)

    # Create a dataset using GPT
    response = openai.ChatCompletion.create(model=settings["gptModel"],
                                            messages=[{"role": "system", "content": settings["systemMessage"]},
                                            {"role": "user", "content": mergedPrompt}])
    print(response)

    return response["choices"][0]["message"]["content"]


def play_sound(file_name):
    fn = os.path.join(os.path.dirname(__file__), file_name)
    wave_obj = sa.WaveObject.from_wave_file(fn)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait for the sound to finish playing


def main():
    print("Write a keystroke to be captured by the script...")
    send_system_alert("Input prompt for VecchioGPT", 5000)
    play_sound("completed.wav")
    intercept_next_keystroke()
    send_system_alert("Running VecchioGPT...")
    pyperclip.copy(global_response)                                # Save output to clipboard
    send_system_alert("Completed.")
    play_sound("completed.wav")

if __name__ == "__main__":
    main()




