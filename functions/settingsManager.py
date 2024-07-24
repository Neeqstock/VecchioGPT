import json
import os

from openai import OpenAI


def load_gpt_models(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            models = data["models"]
            # Replace JSON's null with Python's None
            models = [None if model is None else model for model in models]
            return models
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
    except json.JSONDecodeError:
        print("Error: The file could not be decoded.")
    except KeyError:
        print("Error: The expected key 'models' is missing in the JSON data.")


def read_model():
    with open(SETTINGS_FILENAME, "r") as file:
        return json.load(file)["model"]


def read_complexity_settings(complexity):
    with open(SETTINGS_FILENAME, "r", encoding="utf-8") as file:
        match complexity:
            case "low":
                return json.load(file)["complexity-low_model"]
            case "high":
                return json.load(file)["complexity-high_model"]
            case "long":
                return json.load(file)["complexity-long_model"]
            case _:
                return json.load(file)["complexity-low_model"]


def write_model(new_model):
    with open(SETTINGS_FILENAME, "r") as f:
        data = json.load(f)
        data["model"] = new_model

    with open(SETTINGS_FILENAME, "w") as f:
        json.dump(data, f, indent=4)


def read_popup_settings():
    with open(SETTINGS_FILENAME, "r") as file:
        settings = json.load(file)
        if "popup" in settings:
            return settings["popup"]
        else:
            return []


def read_sound_settings():
    with open(SETTINGS_FILENAME, "r") as file:
        settings = json.load(file)
        if "sound" in settings:
            return settings["sound"]
        else:
            return []


def read_stt_model_settings():
    with open(SETTINGS_FILENAME, "r") as file:
        settings = json.load(file)
        if "speech-to-text_model" in settings:
            return settings["speech-to-text_model"]
        else:
            return []


def read_tts_model_settings():
    with open(SETTINGS_FILENAME, "r") as file:
        settings = json.load(file)
        if "text-to-speech_model" in settings:
            return settings["text-to-speech_model"]
        else:
            return []


def read_tts_voice_settings():
    with open(SETTINGS_FILENAME, "r") as file:
        settings = json.load(file)
        if "text-to-speech_voice" in settings:
            return settings["text-to-speech_voice"]
        else:
            return []


def read_api_key(file_path):
    with open(SETTINGS_FILENAME, "r") as file:
        return json.load(file)["OPENAI_API_KEY"]


def load_shortcuts(filename) -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    # Create a dictionary mapping actions to keys
    return {item["action"]: item["key"] for item in data["shortcuts"]}


def create_configs():
    # Create history if it doesn't exist
    if not os.path.exists(HISTORY_FILENAME):
        with open(HISTORY_FILENAME, "w") as f:
            pass

    # If the settings file does not exist, copy it from the templates folder
    if not os.path.exists(SETTINGS_FILENAME):
        with open(SETTINGS_FILENAME, "w") as f:
            with open(
                os.path.join(TEMPLATES_FOLDER, "settings_template.json"), "r"
            ) as template:
                f.write(template.read())

    # If the shortcuts file does not exist, copy it from the templates folder
    if not os.path.exists(SHORTCUTS_FILENAME):
        with open(SHORTCUTS_FILENAME, "w") as f:
            with open(
                os.path.join(TEMPLATES_FOLDER, "shortcuts_template.json"), "r"
            ) as template:
                f.write(template.read())
    # If the models file does not exist, copy it from the templates folder
    if not os.path.exists(MODELS_FILENAME):
        with open(MODELS_FILENAME, "w") as f:
            with open(
                os.path.join(TEMPLATES_FOLDER, "gpt_models_template.json"), "r"
            ) as template:
                f.write(template.read())


# Filenames
SETTINGS_FILENAME = os.path.join(os.path.dirname(__file__), "../settings.json")
MODELS_FILENAME = os.path.join(os.path.dirname(__file__), "../gpt_models.json")
SOUND_START_FILENAME = os.path.join(os.path.dirname(__file__), "../sounds/start.wav")
SOUND_FINISH_FILENAME = os.path.join(os.path.dirname(__file__), "../sounds/finish.wav")
SOUND_REC_START_FILENAME = os.path.join(
    os.path.dirname(__file__), "../sounds/recStart.wav"
)
SOUND_REC_FINISH_FILENAME = os.path.join(
    os.path.dirname(__file__), "../sounds/recFinish.wav"
)
SOUND_ABORT_FILENAME = os.path.join(os.path.dirname(__file__), "../sounds/abort.wav")
SPEECH_FILENAME = os.path.join(os.path.dirname(__file__), "../temp/speech.wav")
SPEECH_TEMP_FILENAME = os.path.join(
    os.path.dirname(__file__), "../temp/speech_temp.wav"
)
PROMPTS_FOLDER = os.path.join(os.path.dirname(__file__), "../prompts/")
TEMPLATES_FOLDER = os.path.join(os.path.dirname(__file__), "../templates/")
SHORTCUTS_FILENAME = os.path.join(os.path.dirname(__file__), "../shortcuts.json")
VECCHIOGPT_LOGO_FILENAME = os.path.join(os.path.dirname(__file__), "../VecchioGPT.png")
HISTORY_FILENAME = os.path.join(os.path.dirname(__file__), "../.history")

create_configs()

# Models settings
FILE_SPECIFIC = "file_specific"
GPT_MODELS = load_gpt_models(MODELS_FILENAME)
DEFAULT_MODEL_FOR_SPEECH = GPT_MODELS[0]
DEFAULT_ROLE = "system"

# OpenAI API client
OPENAI_CLIENT = OpenAI(api_key=read_api_key(SETTINGS_FILENAME))

# SHORTCUTS
SHORTCUTS = load_shortcuts(SHORTCUTS_FILENAME)

# Main that just create configs
if __name__ == "__main__":
    create_configs()
