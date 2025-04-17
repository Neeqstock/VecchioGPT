import json
import os

from termcolor import colored

from readJson import read_json_file
from settingsManager import (
    FILE_SPECIFIC,
    OPENAI_CLIENT,
    GOOGLE_CLIENT, # Import GOOGLE_CLIENT
    PROMPTS_FOLDER,
    read_complexity_settings,
    read_model,
)

global global_response


def run_prompt(file_name, data, clipboardContents):
    # Seeks the file name
    fn = PROMPTS_FOLDER + str(file_name)
    # Loads the settings from fn file name
    jsonFile = read_json_file(fn)

    mergedSystemMessage = jsonFile["systemMessage"]
    mergedPrompt = jsonFile["prompt"]

    # Merging operation: Replace all the § and §{}
    # additional params first
    if "additionalParams" in data:
        additional_params = data["additionalParams"]
        for param in additional_params:
            key = param.get("key")
            value = param.get("value")
            mergedSystemMessage = mergedSystemMessage.replace("§{" + key + "}", value)
            mergedPrompt = mergedPrompt.replace("§{" + key + "}", value)

    # then clipboard (to avoid override-replacing of §)
    mergedSystemMessage = mergedSystemMessage.replace("§", clipboardContents)
    mergedPrompt = mergedPrompt.replace("§", clipboardContents)

    # Model name
    model = read_model()
    complexity = "ignoring"
    if model == FILE_SPECIFIC:
        try:
            complexity = jsonFile["complexity"]
        except KeyError:
            complexity = "low"
        model = read_complexity_settings(complexity)

    # Get prompt name
    promptName = jsonFile["promptName"]

    return run_gpt(promptName, model, mergedPrompt, mergedSystemMessage, complexity)


def run_gpt(promptName, model, prompt, systemMessage, complexity="ignoring"):
    # Print prompt name
    print("")
    print(
        '"'
        + "\033[1m"
        + colored(promptName, "yellow")
        + "\033[0m"
        + '", '
        + complexity
        + ' complexity, using model "'
        + model
        + '". Prompt:'
    )
    print(prompt)

    response = call_client(model, prompt, systemMessage)

    # Assuming 'response' is a ChatCompletion object for OpenAI and a different object for Gemini
    if model.startswith("gemini"):
        # Assuming Gemini response object has a 'text' attribute or similar
        # You might need to adjust this based on actual Gemini response structure
        ret = response.text # Or response.candidates[0].content.parts[0].text, check Gemini API docs
    else: # OpenAI model
        ret = response.choices[0].message.content

    print("")
    print(colored("\033[1m" + "Answer" + "\033[0m", "green") + ":")
    print(ret)
    print("")
    return ret

def call_client(model, prompt, systemMessage):
    if model.startswith("gemini"):
        # Call Gemini API
        # Gemini might not have explicit systemMessage, so prepend it to the prompt
        contents = systemMessage + "\n\n" + prompt
        response = GOOGLE_CLIENT.models.generate_content(
            model=model, contents=contents
        )
    else:
        # Call OpenAI API
        response = OPENAI_CLIENT.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": systemMessage},
                {"role": "user", "content": prompt},
            ],
        )

    return response


def overwrite_additional_params_in_file(
    data, selected_item, prompts_dictionary, base_path
):
    file_name = prompts_dictionary.get(selected_item)
    if not file_name:
        return

    full_path = os.path.join(base_path, "prompts", file_name)
    original_json = read_json_file(full_path)

    if "additionalParams" in data:
        for i in range(len(data["additionalParams"])):
            # key = data["additionalParams"][i]["key"]
            value = data["additionalParams"][i]["value"]
            if (
                "overwrite" in data["additionalParams"][i]
                and data["additionalParams"][i]["overwrite"]
            ):
                original_json["additionalParams"][i]["value"] = value

    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(original_json, file, indent=4, ensure_ascii=False)
