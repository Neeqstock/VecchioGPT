import keyboard
import functions
import pyperclip
import queue
import tkinter as tk
import subprocess
import os

# Wait message string
wait_message = "Waiting for CTRL+SHIFT+(key)..."

def launch_numeral_prompt(val):
    #functions.play_sound(functions.SOUND_START)
    
    global global_response
    global_response = functions.chat_with_gpt(str(val) + ".json")
    pyperclip.copy(global_response)

    #functions.play_sound(functions.SOUND_COMPLETED)
    print(wait_message)

def launch_gui_prompt():
    subprocess.call(["python", "gui.py"])
    print(wait_message)

def launch_gui_chat():
    subprocess.call(["python", "gui-chat.py"])
    print(wait_message)

def print_intro_console():
    print('\033[1m' + "Welcome to VecchioGPT!" + '\033[0m')
    print("")
    print("Selected model: " + functions.read_model())
    print("")
    print("Mapped shortcuts and prompts:")
    print("")
    for i in range(10):
        fn = os.path.join(os.path.dirname(__file__), "prompts/" + str(i) + ".json")
        data = functions.read_json_file(fn)
        print("CTRL + SHIFT + " + str(i) + ": " + data['promptName'])
    print("")
    print("CTRL + SHIFT + *: calls the fuzzy prompt selector GUI")
    print("CTRL + SHIFT + .: calls the same GUI, but with chat capabilities")
    print("")
    print("=============================================")
    print("")

if __name__ == "__main__":
    print_intro_console()
    q = queue.Queue()
    print(wait_message)
    keyboard.add_hotkey("ctrl+shift+1", lambda: launch_numeral_prompt(1))
    keyboard.add_hotkey("ctrl+shift+2", lambda: launch_numeral_prompt(2))
    keyboard.add_hotkey("ctrl+shift+3", lambda: launch_numeral_prompt(3))
    keyboard.add_hotkey("ctrl+shift+4", lambda: launch_numeral_prompt(4))
    keyboard.add_hotkey("ctrl+shift+5", lambda: launch_numeral_prompt(5))
    keyboard.add_hotkey("ctrl+shift+6", lambda: launch_numeral_prompt(6))
    keyboard.add_hotkey("ctrl+shift+7", lambda: launch_numeral_prompt(7))
    keyboard.add_hotkey("ctrl+shift+8", lambda: launch_numeral_prompt(8))
    keyboard.add_hotkey("ctrl+shift+9", lambda: launch_numeral_prompt(9))
    keyboard.add_hotkey("ctrl+shift+0", lambda: launch_numeral_prompt(0))
    keyboard.add_hotkey("ctrl+shift+*", launch_gui_prompt)
    keyboard.add_hotkey("ctrl+shift+-", functions.next_model)
    keyboard.add_hotkey("ctrl+shift+.", launch_gui_chat)
    keyboard.wait()



    