#!/usr/bin/python3
import os
import platform
import functions
from pynput import keyboard
import pyperclip
import argparse

parser = argparse.ArgumentParser(
    description="""Run ChatGPT with predefined prompts using the current contents of the system clipboard. The output of the model will overwrite the contents of the clipboard.""",
    epilog="Ghe provo però vecchio bella merda vero? Sisi, si",
)
parser.add_argument(
    "--show-prompts",
    type=bool,
    default=False,
    help="Print the currently loaded prompts.",
)

args = parser.parse_args()


acceptedKeystrokes = "1234567890"


def send_system_alert(message, expire_time=1500):
    # Determine the platform (Linux or Windows)
    current_platform = platform.system()

    try:
        # Send a system alert based on the platform
        if current_platform == "Linux":
            os.system(f'notify-send --expire-time={expire_time} "{message}"')
        # else:
        # print("Unsupported platform. Cannot send system alert.")
    except Exception as e:
        print(f"Error sending system alert: {e}")


# DEPRECATED: chat_with_gpt with one argument will not work
def on_key_press(key):
    global global_response
    if key.char in acceptedKeystrokes:
        global_response = chat_with_gpt(key.char + ".json")
        return False


def on_key_release(key):
    global global_response
    if key.char in acceptedKeystrokes:
        return False


def intercept_next_keystroke():
    # Create a keyboard listener
    listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)

    # Start listening for the next keystroke
    with listener:
        listener.join()


def main():
    print("Write a keystroke to be captured by the script...")
    send_system_alert("Input prompt for VecchioGPT", 5000)
    intercept_next_keystroke()
    send_system_alert("Running VecchioGPT...")
    pyperclip.copy(global_response)  # Save output to clipboard
    send_system_alert("Completed.")


if __name__ == "__main__":
    main()
