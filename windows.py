import keyboard
import functions

# Wait message string
wait_message = "Waiting for CTRL+SHIFT+(number)..."

def launch_prompt(val):
    functions.play_sound(functions.soundStart)
    functions.chat_with_gpt(val)
    functions.play_sound(functions.soundCompleted)
    print(wait_message)


if __name__ == "__main__":
    print(wait_message)
    keyboard.add_hotkey("ctrl+shift+1", lambda: launch_prompt(1))
    keyboard.add_hotkey("ctrl+shift+2", lambda: launch_prompt(2))
    keyboard.add_hotkey("ctrl+shift+3", lambda: launch_prompt(3))
    keyboard.add_hotkey("ctrl+shift+4", lambda: launch_prompt(4))
    keyboard.add_hotkey("ctrl+shift+5", lambda: launch_prompt(5))
    keyboard.add_hotkey("ctrl+shift+6", lambda: launch_prompt(6))
    keyboard.add_hotkey("ctrl+shift+7", lambda: launch_prompt(7))
    keyboard.add_hotkey("ctrl+shift+8", lambda: launch_prompt(8))
    keyboard.add_hotkey("ctrl+shift+9", lambda: launch_prompt(9))
    keyboard.add_hotkey("ctrl+shift+0", lambda: launch_prompt(0))
    keyboard.wait()