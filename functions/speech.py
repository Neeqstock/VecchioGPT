import os
import pyperclip
from termcolor import colored
import mp3player
import notifications
from prompt import run_gpt
from settingsManager import (
    DEFAULT_MODEL_FOR_SPEECH,
    FILE_SPECIFIC,
    OPENAI_CLIENT,
    GOOGLE_CLIENT,
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

    current_model = read_model()
    if current_model.lower().startswith("google"):
        try:
            # Use Google TTS API
            response = GOOGLE_CLIENT.generate_content(
                "Convert this text to speech",
                clipboardContents
            )
            # This is placeholder code - you'll need to implement the actual Google TTS API call
            # and save the audio to SPEECH_TEMP_FILENAME
            # For now, we'll fall back to OpenAI
            print("Google TTS not fully implemented, falling back to OpenAI")
            response = OPENAI_CLIENT.audio.speech.create(
                model=read_tts_model_settings(),
                input=clipboardContents,
                voice=read_tts_voice_settings(),
            )
            response.stream_to_file(SPEECH_TEMP_FILENAME)
        except Exception as e:
            print("An error occurred while generating speech with Google API:", e)
            # Fallback to OpenAI
            try:
                response = OPENAI_CLIENT.audio.speech.create(
                    model=read_tts_model_settings(),
                    input=clipboardContents,
                    voice=read_tts_voice_settings(),
                )
                response.stream_to_file(SPEECH_TEMP_FILENAME)
            except Exception as e:
                print("Fallback to OpenAI also failed:", e)
                return
    else:
        try:
            response = OPENAI_CLIENT.audio.speech.create(
                model=read_tts_model_settings(),
                input=clipboardContents,
                voice=read_tts_voice_settings(),
            )
            response.stream_to_file(SPEECH_TEMP_FILENAME)
        except Exception as e:
            print("An error occurred while generating speech:", e)
            return
            
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
        if not os.path.exists(SPEECH_FILENAME):
            print("Error: The audio file does not exist.")
            return

        try:
            transcript = ""
            if selectedModel.lower().startswith("google"):
                # Use Google STT API - placeholder code
                print("Using Google STT API")
                # Replace with actual Google STT implementation
                with open(SPEECH_FILENAME, "rb") as audio_file:
                    transcript = OPENAI_CLIENT.audio.transcriptions.create(
                        model=read_stt_model_settings(),
                        file=audio_file,
                        response_format="text"
                    )
            else:
                with open(SPEECH_FILENAME, "rb") as audio_file:
                    # Fix: Don't access .text property with response_format="text"
                    transcript = OPENAI_CLIENT.audio.transcriptions.create(
                        model=read_stt_model_settings(),
                        file=audio_file,
                        response_format="text"
                    )

            # Print message
            print(
                "\n" + "Detected speech's "
                + colored("\033[1m" + "transcription" + "\033[0m", "green") + ":\n"
                + transcript + "\n"
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

        except Exception as e:
            print("An error occurred during transcription:", e)


def speech_prompt_on_nothing():
    # Model name
    selectedModel = read_model()
    if selectedModel == FILE_SPECIFIC:
        selectedModel = DEFAULT_MODEL_FOR_SPEECH

    # Record audio
    if record_audio_until_keystroke(SPEECH_FILENAME):
        if not os.path.exists(SPEECH_FILENAME):
            print("Error: The audio file does not exist.")
            return

        try:
            transcript = ""
            if selectedModel.lower().startswith("google"):
                # Use Google STT API - placeholder code
                print("Using Google STT API")
                # Replace with actual Google STT implementation
                with open(SPEECH_FILENAME, "rb") as audio_file:
                    transcript = OPENAI_CLIENT.audio.transcriptions.create(
                        model=read_stt_model_settings(),
                        file=audio_file,
                        response_format="text"
                    )
            else:
                with open(SPEECH_FILENAME, "rb") as audio_file:
                    # Fix: Don't access .text property with response_format="text"
                    transcript = OPENAI_CLIENT.audio.transcriptions.create(
                        model=read_stt_model_settings(),
                        file=audio_file,
                        response_format="text"
                    )

            # Print message
            print(
                "\n" + "Detected speech's "
                + colored("\033[1m" + "transcription" + "\033[0m", "green") + ":\n"
                + transcript + "\n"
            )

            notifications.sound(SOUND_START_FILENAME)
            notifications.popup("Processing speech...", 3000)

            global_response = run_gpt(
                promptName="Speech based prompt",
                model=selectedModel,
                prompt=transcript,
                systemMessage="You're a helpful assistant.",
            )

            pyperclip.copy(global_response)
            notifications.sound(SOUND_FINISH_FILENAME)
            notifications.popup("Done!", 1500)

        except Exception as e:
            print("An error occurred during transcription:", e)


def speech_to_clipboard():
    # Record audio
    if record_audio_until_keystroke(SPEECH_FILENAME):
        if not os.path.exists(SPEECH_FILENAME) or os.path.getsize(SPEECH_FILENAME) < 1000:
            print("Error: The audio file does not exist or is too small.")
            return

        try:
            model = read_stt_model_settings()
            print(f"Using STT model: {model}")
            
            selectedModel = read_model()
            transcript = ""
            
            # Try to convert WAV to MP3 if possible (better compatibility)
            mp3_filename = SPEECH_FILENAME.replace('.wav', '.mp3')
            try:
                import subprocess
                print("Converting WAV to MP3 for better API compatibility...")
                result = subprocess.run(
                    ["ffmpeg", "-i", SPEECH_FILENAME, "-acodec", "libmp3lame", mp3_filename],
                    capture_output=True, 
                    text=True
                )
                if os.path.exists(mp3_filename) and os.path.getsize(mp3_filename) > 1000:
                    print(f"Successfully converted to MP3: {mp3_filename}")
                    audio_file_path = mp3_filename
                else:
                    print("MP3 conversion failed, using original WAV file")
                    audio_file_path = SPEECH_FILENAME
            except Exception as e:
                print(f"MP3 conversion failed: {e}, using original WAV file")
                audio_file_path = SPEECH_FILENAME
            
            # Print file details for debugging
            print(f"Audio file: {audio_file_path}, Size: {os.path.getsize(audio_file_path)} bytes")
            
            if selectedModel.lower().startswith("google"):
                # Google API implementation here
                print("Using Google STT API")
                transcript = "Google API not fully implemented - fallback to OpenAI"
                # Fall back to OpenAI for now
                
            # Use OpenAI API
            with open(audio_file_path, "rb") as audio_file:
                print(f"Sending to OpenAI API with model: {model}")
                response = OPENAI_CLIENT.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    response_format="text",
                    language="en",  # Explicitly specify English for better results
                    prompt="This is a clear speech recording that should be transcribed accurately."
                )
                if isinstance(response, str):
                    transcript = response
                else:
                    # Handle object response type
                    transcript = response.text if hasattr(response, 'text') else str(response)
                
            print(f"Raw transcription result: '{transcript}'")
            
            # Put transcribed speech to clipboard
            pyperclip.copy(transcript)

            # Print message
            print(
                "\n" + "Detected speech's "
                + colored("\033[1m" + "transcription" + "\033[0m", "green") + ":\n"
                + transcript + "\n"
                + "Speech has been "
                + colored("\033[1m" + "pasted to clipboard" + "\033[0m", "yellow") + "!"
                + "\n"
            )

            notifications.sound(SOUND_FINISH_FILENAME)
            notifications.popup("Done!", 1500)

            # Clean up temporary MP3 file if created
            if os.path.exists(mp3_filename) and mp3_filename != SPEECH_FILENAME:
                try:
                    os.remove(mp3_filename)
                except:
                    pass

        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            import traceback
            traceback.print_exc()
    # Record audio
    if record_audio_until_keystroke(SPEECH_FILENAME):
        if not os.path.exists(SPEECH_FILENAME):
            print("Error: The audio file does not exist.")
            return

        try:
            model = read_stt_model_settings()
            print("Using STT model:", model)  # Debug line
            
            selectedModel = read_model()
            transcript = ""
            
            if selectedModel.lower().startswith("google"):
                # Use Google STT API - placeholder code
                print("Using Google STT API")
                # Replace with actual Google STT implementation
                with open(SPEECH_FILENAME, "rb") as audio_file:
                    transcript = OPENAI_CLIENT.audio.transcriptions.create(
                        model=model,
                        file=audio_file,
                        response_format="text"
                    )
            else:
                with open(SPEECH_FILENAME, "rb") as audio_file:
                    # Fix: Don't access .text property with response_format="text"
                    transcript = OPENAI_CLIENT.audio.transcriptions.create(
                        model=model,
                        file=audio_file,
                        response_format="text"
                    )

            # Put transcribed speech to clipboard
            pyperclip.copy(transcript)

            # Print message
            print(
                "\n" + "Detected speech's "
                + colored("\033[1m" + "transcription" + "\033[0m", "green") + ":\n"
                + transcript + "\n"
                + "Speech has been "
                + colored("\033[1m" + "pasted to clipboard" + "\033[0m", "yellow") + "!"
                + "\n"
            )

            notifications.sound(SOUND_FINISH_FILENAME)
            notifications.popup("Done!", 1500)

        except Exception as e:
            print("An error occurred during transcription:", e)