#!/usr/bin/python3
import openai
import pyperclip
import os
import simpleaudio as sa
import json
from termcolor import colored
import hashlib
import re


global global_response

# Settings ===============================================
SETTINGS_FILENAME = os.path.join(os.path.dirname(__file__), 'settings.json')
NO_MODEL = "file_specific"
GPT_MODELS = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", NO_MODEL]
DEFAULT_ROLE = "system"

# Model settings
def read_model():
	with open(SETTINGS_FILENAME, "r") as file:
		return json.load(file)['model']

def write_model(new_model):
	with open(SETTINGS_FILENAME, 'r') as f:
		data = json.load(f)
		data["model"] = new_model

	with open(SETTINGS_FILENAME, 'w') as f:
		json.dump(data, f, indent=4)

def next_model():

	selected_model = read_model()
	i = GPT_MODELS.index(selected_model)
	selected_model = ""
	if i + 1 < len(GPT_MODELS):
		selected_model = GPT_MODELS[i + 1]
	else:
		selected_model = GPT_MODELS[0]
	write_model(selected_model)
	print("Model changed to: " + selected_model)

def read_notification():
	with open(SETTINGS_FILENAME, "r") as file:
		settings = json.load(file)
		if 'notification' in settings:
			return settings['notification']
		else:
			return []



# ===========================================================

# Sounds
SOUND_START = "start.wav"
SOUND_COMPLETED = "completed.wav"

# OpenAI key
def read_api_key(file_path):
	with open(SETTINGS_FILENAME, "r") as file:
		return json.load(file)['OPENAI_API_KEY']

api_key = read_api_key(SETTINGS_FILENAME)

# Initialize the OpenAI API client
openai.api_key = api_key

def read_json_file(file_path):
	with open(file_path, 'r', encoding="utf-8") as file:
		data = json.load(file)
	return data

def chat_with_gpt(file_name, data, clipboardContents):
	# Seeks the file name
	fn = os.path.join(os.path.dirname(__file__), "prompts/" + str(file_name))
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
	mergedPrompt = mergedPrompt.replace('§', clipboardContents)

	# Create a dataset using GPT
	selected_model = read_model()
	if selected_model == NO_MODEL:
		selected_model = jsonFile["gptModel"]

	# Print prompt name
	print("")
	print('"' + '\033[1m' + colored(jsonFile["promptName"], "yellow") + '\033[0m' + '" using model "' + selected_model + '". Prompt:')
	print(mergedPrompt)

	response = openai.ChatCompletion.create(model=selected_model,
											messages=[{"role": "system", "content": mergedSystemMessage},
											{"role": "user", "content": mergedPrompt}])

	ret = response["choices"][0]["message"]["content"]
	print("")
	print(colored('\033[1m' + "Answer" + '\033[0m', "green")  + ":")
	print(ret)
	print("")
	print("=============================================")
	print("")
	return ret


def play_sound(file_name):
	fn = os.path.join(os.path.dirname(__file__), file_name)
	wave_obj = sa.WaveObject.from_wave_file(fn)
	play_obj = wave_obj.play()
	play_obj.volume = 0.5  # Set volume to half the maximum
	play_obj.wait_done()  # Wait for the sound to finish playing


#####################################################################################
#                         Listbox prompts order using history						#
#####################################################################################
"""
Updates the history file by placing a specific filename at the top.

Args:
    filename (str): The name of the file to be placed at the top of the history.
    path_to_history (str): The file path to the history file.
"""
def history_put_on_top(filename, path_to_history):
    with open(path_to_history, 'r') as file:
        lines = file.readlines()

    lines = [line for line in lines if line.strip("\n") != filename]
    lines.insert(0, filename + "\n")

    with open(path_to_history, 'w') as file:
        file.writelines(lines)
	

'''
Returns the prompts sorted by the history and fixes the history file (purge inexistent files in history, add new files which were not present)
'''
def get_sorted_history(prompts_dictionary, path_to_history):
	
	with open(path_to_history, 'r') as file:
		history_filenames = file.readlines()
		history_filenames = [x.replace("\n", "") for x in history_filenames]


	files_in_folder = list(prompts_dictionary.values())

	# purging all the elements in history_filenames which are not present in files_in_folder
	history_filenames = [filename for filename in history_filenames if filename in files_in_folder]

	# Taking all the elements in files_in_folder and adding them to the bottom of history_filenames
	for filename in files_in_folder:
		if filename not in history_filenames:
			history_filenames.append(filename)
	
	# Replace the old history
	with open(path_to_history, 'w') as file:
		for name in history_filenames:
			file.write(name + "\n")

	# Generates the sorted prompts list from sorted file list
	sorted_promptnames = []
	for filename in history_filenames:
		sorted_promptnames.append(find_key(prompts_dictionary, filename))

	return sorted_promptnames

def find_key(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

#####################################################################################
#                               Citation fixer                                      #
#####################################################################################
"""
Fix LaTeX citations in a given output text rewritten by ChatGPT by substituting them with the correct
labels. The code is run only if some citations in the original text are not present in the output text.

**Arguments:**
- `input_text` (str): The input text containing LaTeX citations.
- `output_text` (str): The output text from ChatGPT where the citations need to be fixed.

**Returns:**
- `ret` (str): The text with replaced citations.
"""
def fix_latex_citations(input_text, output_text):
	citations = get_citations(input_text)
	citations_output = get_citations(output_text)
	ret = output_text
	if set(citations) != set(citations_output):
		ret = substitute_citations(output_text, citations)
	return ret


"""
Extracts citation labels from an input text.

Args:
	input_text (str): The input text from which to extract citation labels.

Returns:
	list: A list of citation labels found in the input text.
"""
def get_citations(input_text):
	labels_to_match = ["cite", "citep", "citet"]
	matches = []
	for label in labels_to_match:
		label_regex = re.compile(r'(\\' + rf'{label}' + r'(?:\[[^\]]*\])?(?:\[[^\]]*\])?\{[^{}]+\})')
		label_match = label_regex.findall(input_text)
		matches = matches + label_match
		print(f"{label} matches:", label_match)

	return matches

"""
Substitute citations in the output text with the correct input labels using ChatGPT.

Args:
	output_text (str): The output text containing citations to be substituted.
	citations (list): A list of LaTeX citation labels to be used for substitution.

Returns:
	str: The fixed text with the substituted citations.
"""
def substitute_citations(output_text, citations):
	#FIXME: check to make sure that a model is selected in the settings
	selected_model = read_model()
	message_when_fixing_citations = """
	I will give a text as an input and a set of LaTeX citation labels such as `\cite{<label>}`,`\citet{<label1>,<label2>}`. Please substitute the references that you find in the input text with the correct LaTeX citation labels. Do not touch anything else.
	"""

	prompt_to_fix_citations = f"Input labels: {citations}\n\nInput text: {output_text}"

	print("\n")
	print(colored('\033[1m' + "Citations" + '\033[0m', "blue")  + ":")
	print(citations)
	print("\n")

	print(colored('\033[1m' + "Raw output" + '\033[0m', "red")  + ":")
	print(output_text)
	print("\n")

	response = openai.ChatCompletion.create(model=selected_model,
											messages=[{"role": "system", "content": message_when_fixing_citations},
											{"role": "user", "content": prompt_to_fix_citations}], temperature=0.15)

	ret = response["choices"][0]["message"]["content"]
	print(colored('\033[1m' + "Fixed text" + '\033[0m', "green")  + ":")
	print(ret)
	print("\n")

	return ret