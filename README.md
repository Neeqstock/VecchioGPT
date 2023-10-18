<div align="center">
  <img src="https://raw.githubusercontent.com/Neeqstock/VecchioGPT/main/VecchioGPT.png" alt="VecchioGPT logo. Thanks for existing, Stable Diffusion, because I can't draw." width="150px" height="150px" />
</div>

# VecchioGPT
 _System-wide GPT prompts computed on your clipboard's contents! Ghe provo però vecchio bel casino vero? Sisi, si_

VecchioGPT is a Python application that allows users to apply custom GPT prompts to the text stored in the system clipboard. It is cross-platform and compatible with both Windows and Linux systems.

## OpenAI API

VecchioGPT runs on the OpenAI API, which means that you need to have an OpenAI account and an [OpenAI API key](https://platform.openai.com/account/api-keys). Unlike the web version of ChatGPT, which operates on a monthly subscription basis, API access is billed based on usage at affordable prices.

## Features
- Clipboard Integration: Easily generate prompts using text copied to the system clipboard.
- Workflow Efficiency: Use a designated hotkey to call VecchioGPT, and the user-defined prompt is executed, with the output conveniently pasted into the clipboard.
- Interactive GUI: A cross-platform graphical user interface provides a user-friendly way to select and customize prompts.

<div align="center">
  <img src="https://raw.githubusercontent.com/Neeqstock/VecchioGPT/main/readme_files/gui_example.png" alt="VecchioGPT GUI example" height="200px" />
</div>

## Installation

Clone the repository:
```bash
git clone https://github.com/Neeqstock/VecchioGPT.git
cd VecchioGPT
```

Install dependencies using pip:

```bash
pip3 install sv-ttk thefuzz pyperclip pillow termcolor simpleaudio openai pynput keyboard
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

- Run _daemon.py_ (you can reduce to icon the script console)
- Select some text, and press CTRL+C to put it into clipboard
- Press any of the defined keyboard shortcuts
- Two audible pings will advise you when the computation is started, and when the answer is complete and ready
- When the answer is ready, it will be automatically copied inside the clipboard. Use CTRL+V to paste it anywhere
- Prompts, input and answers will also be printed on the console

**Keyboard shortcuts:**

CTRL+SHIFT+(0-9): run any of the custom prompts associated to numeral keys

CTRL+SHIFT+*: open the prompt selection GUI

CTRL+SHIFT+-: change the model in use, between gpt-3.5-turbo, gpt-4, or prompt_default. This one means the model suggested in the custom prompt file will be used.

## [Making new custom prompts](./docs/prompts.md)

<!-- Custom prompts are files stored inside the _prompts_ folder. You will find a collection of custom prompts inside the _Awesome-VecchioGPT_ folder, which you can simply move to the prompts folder. -->
<!-- Creating new prompts is easy: just copy any prompt file and edit the fields. The fields to edit are: -->

<!-- - **promptName**: name of the prompt which will be shown in the GUI; -->
<!-- - **language**: type of programming or markup language involved. Specify "Text" if the prompt works on plain text; -->
<!-- - **description**: a detailed description of the effect of the prompt; -->
<!-- - **author**: your nickname x) -->
<!-- - **systemMessage**: the system message that will be sent as part of the prompt. Required, and often used to give specific instructions and informations to the model. -->
<!-- - **gptModel**: suggested GPT model to be used with this prompt; -->
<!-- - **temperature**: form 0.1 to 1.0, define how much "creative" will the answer be. 0.1 is the creativity extreme, while 1.0 means every answer will be the same, provided the same prompt contents; -->
<!-- - **prompt**: the effective prompt that will be passed to the GPT model. Use "§" character to specify where the clipboard contents will be merged inside the prompt: it will be substituted with the contents of the clipboard. -->

Files named _(0-9).json_ must be present in the _prompts_ folder, and refer to the prompts that will be called using the CTRL+SHIFT+(0-9) keyboard shortcut combination, using the background daemon. Those will be also accessible through the prompt picker GUI.

It's greatly advised not to create two prompts with the same _promptName_.

## Dependencies

- sv-ttk
- thefuzz
- pyperclip
- PIL (Pillow)
- termcolor
- simpleaudio
- openai
- pynput
- keyboard

Note: The listed dependencies are not exhaustive; make sure you have a Python environment with the necessary built-in modules.


Feel free to contribute by forking the repository and creating pull requests. Bug reports and feature requests are welcome!
