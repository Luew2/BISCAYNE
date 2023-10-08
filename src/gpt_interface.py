# gpt_interface.py
import openai
import os
import re
from dotenv import load_dotenv
from elevenlabs_interface import speak

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API Key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

character = {
        "name": "BISCAYNE",
        "class": "Wizard",
        "race": "Elf",
        "level": 1,
        "hp": 10,
        "mana": 15,
        "inventory": ["wand", "spellbook"]
        }

def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
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
            speak(segment.strip(), voice="jsCqWAovK2LkecY7zXl4")
        
        # Play action segment if there's an action left
        if i < len(actions):
            action = actions[i]
            speak(action.strip(), voice="zcAOhNBS3c14rBihAFp1")

def run_conversation():
    print("BISCAYNE Interactive Terminal")
    print("Type 'exit' to quit.")

    # Convert the character dictionary into a descriptive string
    character_description = f"""
    You are {character['name']}, a level {character['level']} {character['race']} {character['class']}. 
    You have {character['hp']} HP and {character['mana']} mana. Your inventory includes: {', '.join(character['inventory'])}.

    When responding to combat or action scenarios:
    - Enclose actions in asterisks (*). For example: "*{character['name']} casts a Fireball spell at the enemy*".
    - Remember, every action or narration that is not directly dialogue, you MUST enclose in asterisks.
    - For dialogue, speak as {character['name']}. For example: "Feel the heat of my magic!"
    - Avoid providing additional context or rolling dice in your response. The user will handle the outcomes and let you know
    what happens next turn.
    - If told that you are in a fight and initiative has been rolled, it is a standard DND fight, you get 1 action, 30FT movement, and 1 bonus action.
    Narrate every choice you make.
    """





    messages = [
        {"role": "system", "content": character_description}
    ]
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break
        messages.append({"role": "user", "content": user_input})
        response = get_response(messages)
        messages.append({"role": "assistant", "content": response})
        print(f"BISCAYNE: {response}")

        # Handle the response for TTS
        handle_response(response)

if __name__ == "__main__":
    run_conversation()
