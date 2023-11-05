import openai
import os
import re
from dotenv import load_dotenv
from elevenlabs_interface import speak
import time
import subprocess
import json
import random
import yt_dlp
import mpv
import vlc
import signal
import subprocess
import threading


# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API Key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Set the root directory of the project
project_root_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.join(project_root_dir, '..')  # Move up one directory to get the project root
audio_dir = os.path.join(project_root_dir, 'audio')  # Path to the 'audio' directory

functions_description = [
    {
        "name": "play_random_song",
        "description": "Plays a song as a bard, use this to intimidate your opponents!",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

# Global variable to monitor song playback termination
terminate_song = False

def play_random_song(playlist_url="https://www.youtube.com/playlist?list=PLNpnsfpDYQxQMptivYWl4tCtSKWt9RSCB"):
    global terminate_song

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'outtmpl': 'temp_song.%(ext)s',
        'format': 'bestaudio/best'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        if 'entries' in result:
            for attempt in range(10):  # 10 attempts
                random_video = random.choice(result['entries'])
                video_url = random_video['url']
                print("Attempt:", attempt + 1)
                print("Playing:", video_url)
                
                try:
                    # First, download the audio
                    ydl.download([video_url])

                    # Determine the extension of the downloaded file
                    downloaded_file = next((f for f in os.listdir() if f.startswith("temp_song.")), None)
                    if not downloaded_file:
                        print("Downloaded file not found.")
                        return

                    # Now play it using mpv
                    mpv_process = subprocess.Popen(['mpv', '--no-video', downloaded_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                    out, err = mpv_process.communicate()
                    if out:
                        print("MPV Output:", out.decode())
                    if err:
                        print("MPV Error:", err.decode())

                    while True:
                        if terminate_song:
                            mpv_process.terminate()
                            terminate_song = False
                            return
                        if mpv_process.poll() is not None:
                            break
                        time.sleep(0.5)
                except Exception as e:
                    print(f"Error on attempt {attempt + 1}: {str(e)}")
                    continue
                break  # Exit the loop if the command succeeds
            else:
                print("All attempts failed.")



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
        messages=messages,
        functions=functions_description,
        function_call="auto"
    )
    return response

def handle_response(response, character):
    # Regular expression to find all actions
    actions = re.findall(r'\*(.*?)\*', response)

    # Split the response into segments based on actions
    segments = re.split(r'\*.*?\*', response)

    # Iterate over the segments and actions in order
    for i, segment in enumerate(segments):
        # Play dialogue segment
        if segment.strip():
            speak(segment.strip(), voice=character["voice"])
        
        # Play action segment if there's an action left
        if i < len(actions):
            action = actions[i]
            speak(action.strip(), voice=character["voice"])

def run_conversation(character):
    print("BISCAYNE Interactive Terminal")
    print("Type 'exit' to quit.")

    # Convert the character dictionary into a descriptive string
    character_description = f"""
    You are Joe biden playing dnd, your character name is: {character['name']}, a level {character['level']} {character['race']} {character['class']}. 
    You have {character['hp']} HP and {character['mana']} mana. Your inventory includes: {', '.join(character['inventory'])}.
    
    {character['ai_system_message']}
    """

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
                messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

                print(f"{character['name']} {response['choices'][0]['message']['content']}\n") 
                
                print(response)
                # Handle the response for TTS
                if response['choices'][0]['message']['content'] is not None: 
                    print("here 1")
                    handle_response(response['choices'][0]['message']['content'], character) 

                if response['choices'][0]['message'].get('function_call'):  
                    print("here 2")
                    function_name = response['choices'][0]['message']['function_call']['name']
                    if function_name == "play_random_song":
                        if response['choices'][0]['message']['content'] is not None: 
                            time.sleep(10)
                        play_random_song()

            # Clean up audio files after processing the entire speech
            cleanup_audio_files()

        # Add a delay to check for file changes periodically
        time.sleep(.5)


if __name__ == "__main__":
    play_random_song()