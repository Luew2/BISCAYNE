# BISCAYNE: DND AI Assistant

`BISCAYNE` is a Python-based tool designed to bring an AI character to life in your DND campaign. Dive into a seamless integration of human and AI storytelling in the world of tabletop role-playing.

## Features

- **AI Character Integration**: Introduce an AI-driven character into your DND game. Describe the ongoing events, and BISCAYNE will craft responses, actions, and dialogues for its character.
  
- **Voice-to-Text Input**: Use a push-to-talk mechanism to narrate the game's events. BISCAYNE will listen, understand, and react accordingly.

- **Elven Labs Audio**: Experience immersive audio responses generated through Elven Labs, enhancing the storytelling experience.

- **Dynamic Role-playing**: Roll for the AI, play out its turn, and then relay back the outcomes. BISCAYNE will adapt and evolve its strategies based on the game's progression.

## Setup

1. **Clone the Repository**:
```bash
git clone https://github.com/yourusername/BISCAYNE.git
```

2. **Character Image**:
Place a character image titled `character.png` in the `character` folder. This will be used to represent the AI character visually.

3. **Run Character Creator**:
Before starting the main program, navigate to the `src` directory and execute:
```bash
python char_creator.py
```
This will process the character image for use in the main program.

4. **Install Dependencies**:
Navigate to the project directory and run:
```bash
pip install -r requirements.txt
```

5. **API Keys**:
Store your GPT-4 and Elven Labs API keys in a `.env` file. You can use `example.env` as a template. Simply copy its contents and replace the placeholders with your actual API keys.

6. **Character Profiles**:
Update `characters/character_profiles.json` with the AI character's backstory and traits.

7. **Run BISCAYNE**:
Navigate to the `src` directory and execute:
```bash
python main.py
```

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