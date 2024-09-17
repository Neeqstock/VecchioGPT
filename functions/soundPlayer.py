import os
import pygame

def play_sound(file_name):
    pygame.mixer.init()  # Initialize the mixer
    fn = os.path.join(os.path.dirname(__file__), file_name)
    
    # print(f"Attempting to play sound from: {fn}")  # Debug line
    
    try:
        pygame.mixer.music.load(fn)  # Load the sound file
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play()  # Play the sound

        # Wait for the sound to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Wait a bit
    except pygame.error as e:
        print(f"Error playing sound: {e}")  # Print any error that occurs
