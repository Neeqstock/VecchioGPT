import keyboard
import functions
import pyperclip
import queue
import tkinter as tk
import subprocess

# Wait message string
wait_message = "Waiting for CTRL+SHIFT+(number)..."

def launch_numeral_prompt(val):
    functions.play_sound(functions.soundStart)
    
    global global_response
    global_response = functions.chat_with_gpt(str(val) + ".json")
    pyperclip.copy(global_response)

    functions.play_sound(functions.soundCompleted)
    print(wait_message)

def launch_gui_prompt():
    subprocess.call(["python", "gui.py"])
    print(wait_message)

if __name__ == "__main__":
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
    keyboard.add_hotkey("ctrl+shift+k", launch_gui_prompt)
    keyboard.wait()



    