import pygame
import time
import keyboard

def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    print("Playing... Press CTRL+SHIFT+0 to stop.")

    # Loop to keep the program running and listen for the key combination
    while pygame.mixer.music.get_busy():
        if keyboard.is_pressed("ctrl+shift+0"):  # Check if key combination is pressed
            pygame.mixer.music.stop()  # Stop the music
            print("Playback stopped.")
            break
        time.sleep(0.1)  # Limit checking frequency to 10 times per second

# Example usage
# play_mp3('path_to_your_mp3_file.mp3')