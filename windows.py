import keyboard
import functions
import pystray
from PIL import Image


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




def exit_action(icon, item):
    icon.stop()

# Create an image for the icon
image = Image.open('icon.png')  # specify the path to your icon file

# Create a menu for the icon
menu = (pystray.MenuItem('Exit', exit_action),)

# Create the icon object
icon = pystray.Icon("name", image, "My System Tray Icon", menu)

# Run the icon
icon.run()