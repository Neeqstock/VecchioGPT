import pyperclip
from termcolor import colored

import mp3player
import notifications
from prompt import run_gpt
from settingsManager import (
    DEFAULT_MODEL_FOR_SPEECH,
    FILE_SPECIFIC,
    OPENAI_CLIENT,
    SOUND_FINISH_FILENAME,
    SOUND_START_FILENAME,
    SPEECH_FILENAME,
    SPEECH_TEMP_FILENAME,
    read_model,
    read_stt_model_settings,
    read_tts_model_settings,
    read_tts_voice_settings,
)
from soundRecorder import record_audio_until_keystroke


def speech_from_clipboard():
    clipboardContents = pyperclip.paste()
    print("")
    print(colored("Generating speech:\n", "red"))
    print(clipboardContents)
    print("")
    notifications.sound(SOUND_START_FILENAME)
    notifications.popup("Generating speech...", 3000)
    response = OPENAI_CLIENT.audio.speech.create(
        model=read_tts_model_settings(),
        input=clipboardContents,
        voice=read_tts_voice_settings(),
    )
    response.stream_to_file(SPEECH_TEMP_FILENAME)
    mp3player.play_mp3(SPEECH_TEMP_FILENAME)
    notifications.popup("Speech terminated!", 1500)
    print("Speech terminated!\n\n")


def speech_prompt_on_clipboard():
    # Model name
    selectedModel = read_model()
    if selectedModel == FILE_SPECIFIC:
        selectedModel = DEFAULT_MODEL_FOR_SPEECH

    # Prompt
    selectedPrompt = pyperclip.paste()

    # Record audio
    if record_audio_until_keystroke(SPEECH_FILENAME):
        audio_file = open(SPEECH_FILENAME, "rb")
        transcript = OPENAI_CLIENT.audio.transcriptions.create(
            model=read_stt_model_settings(), file=audio_file
        ).text

        # Print message
        print(
            "\n"
            + "Detected speech's "
            + colored("\033[1m" + "transcription" + "\033[0m", "green")
            + ":\n"
            + transcript
            + "\n"
        )

        notifications.sound(SOUND_START_FILENAME)
        notifications.popup("Processing speech...", 3000)

        global_response = run_gpt(
            promptName="Speech based prompt",
            model=selectedModel,
            prompt=selectedPrompt,
            systemMessage=transcript,
        )

        pyperclip.copy(global_response)

        notifications.sound(SOUND_FINISH_FILENAME)
        notifications.popup("Done!", 1500)


def speech_prompt_on_nothing():
    # Model name
    selectedModel = read_model()
    if selectedModel == FILE_SPECIFIC:
        selectedModel = DEFAULT_MODEL_FOR_SPEECH

    # Record audio
    if record_audio_until_keystroke(SPEECH_FILENAME):
        audio_file = open(SPEECH_FILENAME, "rb")
        transcript = OPENAI_CLIENT.audio.transcriptions.create(
            model=read_stt_model_settings(), file=audio_file
        ).text

        # Print message
        print(
            "\n"
            + "Detected speech's "
            + colored("\033[1m" + "transcription" + "\033[0m", "green")
            + ":\n"
            + transcript
            + "\n"
        )

        notifications.sound(SOUND_START_FILENAME)
        notifications.popup("Processing speech...", 3000)

        global_response = run_gpt(
            promptName="Speech based prompt",
            model=selectedModel,
            prompt=transcript,
            systemMessage="You're an helpful assistant.",
        )

        pyperclip.copy(global_response)

        notifications.sound(SOUND_FINISH_FILENAME)
        notifications.popup("Done!", 1500)


def speech_to_clipboard():
    # Record audio
    if record_audio_until_keystroke(SPEECH_FILENAME):
        audio_file = open(SPEECH_FILENAME, "rb")
        transcript = OPENAI_CLIENT.audio.transcriptions.create(
            model=read_stt_model_settings(), file=audio_file
        ).text

        # Put transcribed speech to clipboard
        global_response = transcript
        pyperclip.copy(global_response)

        # Print message
        print(
            "\n"
            + "Detected speech's "
            + colored("\033[1m" + "transcription" + "\033[0m", "green")
            + ":\n"
            + transcript
            + "\n"
            + "Speech has been "
            + colored("\033[1m" + "pasted to clipboard" + "\033[0m", "yellow")
            + "!"
            + "\n"
        )

        notifications.sound(SOUND_FINISH_FILENAME)
        notifications.popup("Done!", 1500)
