# VecchioGPT
 _System-wide GPT prompts on your clipboard! Ghe provo però vecchio bel casino vero? Sisi, si_

VecchioGPT is a Python application that allows users to apply custom GPT prompts using text from the system clipboard.

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

- Run gui.py:

```bash
python3 gui.py
```

- Use the arrow keys to select the prompt to run on the text in the system clipboard.

- The generated GPT response will be automatically copied to the clipboard.

Dependencies

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
