import vlc
import keyboard
import time


def play_mp3(file_path):
    # Initialize VLC player
    player = vlc.MediaPlayer(file_path)

    # Play the MP3 file
    player.play()

    print("Playing... Press CTRL+SHIFT+0 to stop.")

    # Loop to keep the program running and listen for the key combination
    while player.is_playing():
        if keyboard.is_pressed("ctrl+shift+0"):  # Check if key combination is pressed
            player.stop()  # Stop the music
            print("Playback stopped.")
            break
        time.sleep(0.1)  # Limit checking frequency to 10 times per second
