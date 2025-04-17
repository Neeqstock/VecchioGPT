import sounddevice as sd
import numpy as np
import wave
import keyboard
import notifications
from settingsManager import (
    SHORTCUTS,
    SOUND_ABORT_FILENAME,
    SOUND_REC_FINISH_FILENAME,
    SOUND_REC_START_FILENAME,
)

def record_audio_until_keystroke(filename):
    # Set up parameters for recording
    sample_rate = 16000  # Whisper works well with 16kHz audio
    channels = 1  # Mono audio
    recorded_frames = []

    print(
        "\nRecording... Press {} to finish, or {} to abort.".format(
            SHORTCUTS["key_end_record"], SHORTCUTS["key_abort"]
        )
    )

    notifications.sound(SOUND_REC_START_FILENAME)
    notifications.popup(
        "Recording audio.\n{} to finish,\n{} to abort.".format(
            SHORTCUTS["key_end_record"], SHORTCUTS["key_abort"]
        ),
        3000,
    )

    # Define a callback function to capture audio data
    def callback(indata, frames, time, status):
        if status:
            print(status)  # Print any errors
        recorded_frames.append(indata.copy())

    # Start recording
    with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback):
        while True:
            # Check for key presses
            if keyboard.is_pressed(SHORTCUTS["key_abort"]):
                notifications.sound(SOUND_ABORT_FILENAME)
                notifications.popup("Recording aborted.", 1500)
                print("Recording aborted.")
                return False
            if keyboard.is_pressed(SHORTCUTS["key_end_record"]):
                notifications.sound(SOUND_REC_FINISH_FILENAME)
                notifications.popup(
                    "Recording stopped.\nSending to Whisper API for processing.", 1500
                )
                print("Recording stopped. Sending to Whisper API for processing...\n")
                break

    # Convert the recorded frames to a NumPy array
    audio_data = np.concatenate(recorded_frames, axis=0)

    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    return True
