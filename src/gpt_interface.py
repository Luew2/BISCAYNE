import openai
import os
import re
from dotenv import load_dotenv
from elevenlabs_interface import speak
import time
import subprocess

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API Key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set the root directory of the project
project_root_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.join(project_root_dir, '..')  # Move up one directory to get the project root
audio_dir = os.path.join(project_root_dir, 'audio')  # Path to the 'audio' directory

character = {
        "name": "Joe",
        "class": "Wizard",
        "race": "Human",
        "level": 1,
        "hp": 10,
        "mana": 15,
        "inventory": ["wand", "spellbook"]
        }

def cleanup_audio_files():
    # Convert MP3 to WAV using ffmpeg and suppress output
    subprocess.run(["ffmpeg", "-y", "-i", os.path.join(audio_dir, "temp_audio.mp3"), os.path.join(audio_dir, "temp_audio.wav")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Delete all segment files and the main MP3 file
    for file in os.listdir(audio_dir):
        if file.startswith("segment_") and file.endswith(".mp3"):
            os.remove(os.path.join(audio_dir, file))
    if os.path.exists(os.path.join(audio_dir, "temp_audio.mp3")):
        os.remove(os.path.join(audio_dir, "temp_audio.mp3"))

def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return response['choices'][0]['message']['content']

def handle_response(response):
    # Regular expression to find all actions
    actions = re.findall(r'\*(.*?)\*', response)

    # Split the response into segments based on actions
    segments = re.split(r'\*.*?\*', response)

    # Iterate over the segments and actions in order
    for i, segment in enumerate(segments):
        # Play dialogue segment
        if segment.strip():
            speak(segment.strip(), voice="igoSWis3wMrLrHIeQnWA")
        
        # Play action segment if there's an action left
        if i < len(actions):
            action = actions[i]
            speak(action.strip(), voice="V34fyfeMxZJthpVEAsg4")

def run_conversation():
    print("BISCAYNE Interactive Terminal")
    print("Type 'exit' to quit.")

    # Convert the character dictionary into a descriptive string
    character_description = f"""
    You are Joe biden playing dnd, your character name is: {character['name']}, a level {character['level']} {character['race']} {character['class']}. 
    You have {character['hp']} HP and {character['mana']} mana. Your inventory includes: {', '.join(character['inventory'])}.
    
    The dungeon master is named Toby, you will be asking him questions and telling him what you roll.
    Speak as your chracters voice when role playing, but also feel free to speak as yourself, Joe Biden,
    when you are talking to the DM. Toby actually exists as a person, dont respond as him, only respond as yourself and wait for further
    instructions of what happened as a result of your actions, keep your responses short.
    """
    # When responding to combat or action scenarios:
    # - Enclose actions in asterisks (*). For example: "*{character['name']} casts a Fireball spell at the enemy*".
    # - Remember, every action or narration that is not directly dialogue, you MUST enclose in asterisks.
    # - For dialogue, speak as {character['name']}. For example: "Feel the heat of my magic!"
    # - Avoid providing additional context or rolling dice in your response. The user will handle the outcomes and let you know
    # what happens next turn.
    # - If told that you are in a fight and initiative has been rolled, it is a standard DND fight, you get 1 action, 30FT movement, and 1 bonus action.
    # Narrate every choice you make.

    # The narrator never uses I voice, so anything in * doesnt use I voice

    # Also extra important: You are Joe Biden Playing this DND character named Joe, and the narrator for your actions is Obama, act like Joe biden and Obama,
    # sometimes throw in things that is out of DND character but akin to Joe Biden the President or Obama the former president.
    # 

    messages = [
        {"role": "system", "content": character_description}
    ]
 # Check for changes in the transcribed_text.txt file
    last_modified = None

    while True:
        # Check if transcribed_text.txt has been modified
        current_modified = os.path.getmtime("transcribed_text.txt")
        if current_modified != last_modified:
            # File has been modified, read its contents
            last_modified = current_modified

            with open("transcribed_text.txt", "r") as text_file:
                user_input = text_file.read().strip()

                if user_input.lower() == "exit":
                    break

                messages.append({"role": "user", "content": user_input})
                response = get_response(messages)
                messages.append({"role": "assistant", "content": response})
                print(f"{character['name']} {response}\n")

                # Handle the response for TTS
                handle_response(response)

            # Clean up audio files after processing the entire speech
            cleanup_audio_files()

        # Add a delay to check for file changes periodically
        time.sleep(.5)

if __name__ == "__main__":
    run_conversation()
