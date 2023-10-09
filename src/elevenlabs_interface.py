import subprocess
import time
import requests
from dotenv import load_dotenv
from pydub import AudioSegment
import os

# At the top of the elevenlabs_interface script
global audio_dir

# Load environment variables from .env file
load_dotenv()

# Initialize Elven Labs API Key from environment variable
ELVENLABS_API_KEY = os.environ.get("ELVENLABS_API_KEY")

BASE_URL = "https://api.elevenlabs.io/v1"
CHUNK_SIZE = 1024

# Set the root directory of the project
project_root_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.join(project_root_dir, '..')  # Move up one directory to get the project root
project_root_dir = os.path.normpath(project_root_dir)  # Normalize the path
audio_dir = os.path.join(project_root_dir, 'audio')  # Path to the 'audio' directory

def text_to_speech_stream(text, voice_id):
    url = f"{BASE_URL}/text-to-speech/{voice_id}/stream"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=headers, stream=True)
    return response

def save_audio_segment(response):
    audio_data = b""
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            audio_data += chunk
    
    # Generate a unique filename for each audio segment
    segment_filename = os.path.join(audio_dir, f"segment_{int(time.time())}.mp3")
    with open(segment_filename, "wb") as segment_file:
        segment_file.write(audio_data)
    
    # Load the new segment
    new_segment = AudioSegment.from_mp3(segment_filename)
    
    # Check if temp_audio.mp3 exists in the 'audio' directory, if it does, concatenate the new segment to it
    temp_audio_path = os.path.join(audio_dir, "temp_audio.mp3")
    if os.path.exists(temp_audio_path):
        existing_audio = AudioSegment.from_mp3(temp_audio_path)
        combined_audio = existing_audio + new_segment
    else:
        combined_audio = new_segment
    
    # Save the concatenated audio in the 'audio' directory
    combined_audio.export(temp_audio_path, format="mp3")

def speak(text, voice="jsCqWAovK2LkecY7zXl4"):
    response = text_to_speech_stream(text, voice)
    save_audio_segment(response)

# Example usage
if __name__ == "__main__":
    speak("Hello from the world of Dungeons and Dragons!")
