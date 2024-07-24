import pyaudio
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
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000  # Whisper works well with 16kHz audio

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(
        format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk
    )

    print(
        "\nRecording... Press {} to finish, or {} to abort.".format(
            SHORTCUTS["key_end_record"], SHORTCUTS["key_abort"]
        )
    )

    notifications.sound(SOUND_REC_START_FILENAME)
    notifications.popup(
        "Recording audio.\n{} to finish,\n{}to abort.".format(
            SHORTCUTS["key_end_record"], SHORTCUTS["key_abort"]
        ),
        3000,
    )

    frames = []

    # Record until the appropriate keys are pressed
    while True:
        data = stream.read(chunk)
        frames.append(data)
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

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()
    return True
