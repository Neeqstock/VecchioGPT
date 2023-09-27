import keyboard
import subprocess

def launch_main():
    subprocess.run(["python", "main.py"])

keyboard.add_hotkey('ctrl+l', launch_main)

keyboard.wait()