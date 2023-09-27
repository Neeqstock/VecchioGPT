import openai
import pyperclip
import os
import platform
import simpleaudio as sa
from pynput import keyboard

# Funzioni del cazzo di pynput porcoddio
def on_press(key):
    print(f'{key} pressed')

def on_release(key):
    print(f'{key} release')
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


def chat_with_gpt(prompt):
    # Define the system message
    system_msg = 'You are a helpful assistant.'

    # Create a dataset using GPT
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                            {"role": "user", "content": prompt}])

    return response["choices"][0]["message"]["content"]


# OpenAI key
api_key = "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"
# Initialize the OpenAI API client
openai.api_key = api_key

        
def play_completion_sound():
    wave_obj = sa.WaveObject.from_wave_file('completed.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait for the sound to finish playing



def main():
    
    while True:
        input("Press Enter to read from clipboard...")
        user_input = pyperclip.paste()                          # Get string from clipboard

        if user_input.lower() == 'exit':
            break

        response = chat_with_gpt(f"You: {user_input}\nAI:")     # Run ChatGPT
        print(response)
        pyperclip.copy(response)                                # Save output to clipboard
        play_completion_sound()


if __name__ == "__main__":
    main()




