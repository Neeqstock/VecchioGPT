import keyboard
import subprocess
import main

def launch_main():
    main.main()
    print("Waiting for CTRL+L...")
    # subprocess.run(["python", "main.py"])


if __name__ == "__main__":
    print("Waiting for CTRL+L...")
    keyboard.add_hotkey('ctrl+l', launch_main)
    keyboard.wait()