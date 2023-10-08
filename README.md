# BISCAYNE: DND AI Assistant

`BISCAYNE` is a Python-based tool designed to bring an AI character to life in your DND campaign. Dive into a seamless integration of human and AI storytelling in the world of tabletop role-playing.

## Features

- **AI Character Integration**: Introduce an AI-driven character into your DND game. Describe the ongoing events, and BISCAYNE will craft responses, actions, and dialogues for its character.
  
- **Voice-to-Text Input**: Use a push-to-talk mechanism to narrate the game's events. BISCAYNE will listen, understand, and react accordingly.

- **Elven Labs Audio**: Experience immersive audio responses generated through Elven Labs, enhancing the storytelling experience.

- **Dynamic Role-playing**: Roll for the AI, play out its turn, and then relay back the outcomes. BISCAYNE will adapt and evolve its strategies based on the game's progression.

## Setup

1. **Clone the Repository**:
git clone https://github.com/yourusername/BISCAYNE.git

2. **Install Dependencies**:
Navigate to the project directory and run:
pip install -r requirements.txt

3. **API Keys**:
Store your GPT-4 and Elven Labs API keys in `config/api_keys.json`.

4. **Character Profiles**:
Update `characters/character_profiles.json` with the AI character's backstory and traits.

5. **Run BISCAYNE**:
Navigate to the `src` directory and execute:
python main.py

## Usage

1. Start the program and introduce the AI character using a system message.
2. Use the push-to-talk button to describe the ongoing events in the DND game.
3. BISCAYNE will generate a script for its character's actions and dialogues.
4. Play out the AI's turn, roll for it, and then relay back the outcomes.
5. Continue your adventure with BISCAYNE by your side!

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
