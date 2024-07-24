import os
import simpleaudio as sa


def play_sound(file_name):
    fn = os.path.join(os.path.dirname(__file__), file_name)
    wave_obj = sa.WaveObject.from_wave_file(fn)
    play_obj = wave_obj.play()
    play_obj.volume = 0.5  # Set volume to half the maximum
    play_obj.wait_done()  # Wait for the sound to finish playing
