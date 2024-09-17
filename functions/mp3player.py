import simpleaudio as sa
import time
import keyboard


def play_mp3(file_path):
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()

    print("Playing... Press CTRL+SHIFT+0 to stop.")

    # Loop to keep the program running and listen for the key combination
    while play_obj.is_playing():
        if keyboard.is_pressed("ctrl+shift+0"):  # Check if key combination is pressed
            play_obj.stop()  # Stop the music
            print("Playback stopped.")
            break
        time.sleep(0.1)  # Limit checking frequency to 10 times per second