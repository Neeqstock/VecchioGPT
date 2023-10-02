# VecchioGPT
 _System-wide GPT prompts on your clipboard! Ghe provo però vecchio bel casino vero? Sisi, si_

VecchioGPT is a Python application that allows users to apply custom GPT prompts to the text stored in the system clipboard.

## Features
- Clipboard Integration: Easily generate prompts using text copied to the system clipboard.
- Workflow Efficiency: Use a designated hotkey to call VecchioGPT, and the user-defined prompt is executed, with the output conveniently pasted into the clipboard.
- Interactive GUI: A cross-platform graphical user interface provides a user-friendly way to select and customize prompts.

## Installation

Clone the repository:
```bash
git clone https://github.com/Neeqstock/VecchioGPT.git
cd VecchioGPT
```

Install dependencies using pip:

```bash
pip3 install sv-ttk fuzzywuzzy pyperclip pillow termcolor simpleaudio openai pynput
```

## Usage

- Ensure the required dependencies are installed.
- Create a file named `openai_key.txt` containing your OpenAI key, e.g.
    
```bash
OPENAI_API_KEY=<your-OpenAI-key>
```

### Method 1: single launch

- Run gui.py:

```bash
python3 gui.py
```

- Use the arrow keys to select the prompt to run on the text in the system clipboard.

- The generated GPT response will be automatically copied to the clipboard.

### Method 2: background daemon

- Run daemon.py (you can reduce to icon the script)
- Select some text, and press CTRL+C to put it into clipboard
- Press any of the defined keyboard shortcuts

**Shortcuts:**
CTRL+SHIFT+(0-9): run any of the custom prompts associated to numeral keys
CTRL+SHIFT+*: open the prompt selection GUI
CTRL+SHIFT+-: change the model in use, between gpt-3.5-turbo, gpt-4, or prompt_default. This one means the model suggested in the custom prompt file will be used.

### Making new prompts

Custom prompts are file stored inside the _prompts_ folder. You will find a collection of custom prompts inside the _Awesome-VecchioGPT_ folder, which you can simply move in the prompts folder.
New prompts are easy to make: just copy any prompt file and edit the fields. Those are:
- **promptName**: name of the prompt which will be shown in the GUI;
- **language**: type of programming or markup language involved. Specify "Text" if the prompt works on plain text;
- **description**: a detailed description of the effect of the prompt;
- **author**: your nickname x)
- **systemMessage**: the system message that will be sent as part of the prompt. Required, and often used to give specific instructions and informations to the model.
- **gptModel**: suggested GPT model to be used with this prompt;
- **temperature**: form 0.1 to 1.0, define how much "creative" will the answer be. 0.1 is the creativity extreme, while 1.0 means every answer will be the same, provided the same prompt contents;
- **prompt**: the effective prompt that will be passed to the GPT model. Use "§" character to specify where the clipboard contents will be merged inside the prompt: it will be substituted with the contents of the clipboard.

Files named _(0-9).json_ must be present in the _prompts_ folder, and refer to the prompts that will be called using the CTRL+SHIFT+(0-9) keyboard shortcut combination, using the background daemon.

## Dependencies

- sv-ttk
- fuzzywuzzy
- pyperclip
- PIL (Pillow)
- termcolor
- simpleaudio
- openai
- pynput

Note: The listed dependencies are not exhaustive; make sure you have a Python environment with the necessary built-in modules.


Feel free to contribute by forking the repository and creating pull requests. Bug reports and feature requests are welcome!
