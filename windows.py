import keyboard
import functions

wait_message = "Waiting for CTRL+SHIFT+(number)..."


def launch_prompt(val):
    functions.chat_with_gpt(val)


if __name__ == "__main__":
    print(wait_message)
    for i in range(10):
        keyboard.add_hotkey("ctrl+shift+num" + str(i), lambda: launch_prompt(i))
    keyboard.wait()