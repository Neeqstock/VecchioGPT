import sounddevice as sd
import numpy as np
import wave
import keyboard
import notifications
import os
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
            print(f"Status: {status}")  # Print any errors
        # Ensure indata is not empty
        if len(indata) > 0:
            recorded_frames.append(indata.copy())

    # Start recording
    with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback, dtype='int16'):
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

    # Check if we have any recorded frames
    if not recorded_frames:
        print("No audio was recorded!")
        return False

    try:
        # Convert the recorded frames to a NumPy array
        audio_data = np.concatenate(recorded_frames, axis=0)
        
        # Scale to int16 range if needed
        if audio_data.dtype != np.int16:
            audio_data = (audio_data * 32767).astype(np.int16)
            
        # Save the recorded data as a WAV file
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())
            
        # Verify file was created and has content
        if os.path.exists(filename) and os.path.getsize(filename) > 1000:
            print(f"Audio saved successfully: {filename}, size: {os.path.getsize(filename)} bytes")
            return True
        else:
            print(f"Warning: Audio file too small or not created: {filename}")
            return False
            
    except Exception as e:
        print(f"Error saving audio file: {e}")
        return False