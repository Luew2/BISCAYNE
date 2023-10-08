import subprocess
import io
import requests
from dotenv import load_dotenv
import pydub
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Elven Labs API Key from environment variable
ELVENLABS_API_KEY = os.environ.get("ELVENLABS_API_KEY")

BASE_URL = "https://api.elevenlabs.io/v1"
CHUNK_SIZE = 1024

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

def save_and_play_audio(response):
    audio_data = b""
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            audio_data += chunk
    
    # Save audio data to a temporary file
    with open("temp_audio.mp3", "wb") as temp_audio_file:
        temp_audio_file.write(audio_data)
    
    # Use ffmpeg to play the temporary audio file and redirect stderr to /dev/null
    subprocess.run(["ffmpeg", "-i", "temp_audio.mp3", "-af", "volume=2", "-y", "-hide_banner", "-loglevel", "error", "-nostdin", "-f", "alsa", "default"], stderr=subprocess.DEVNULL)

def speak(text, voice="jsCqWAovK2LkecY7zXl4"):
    response = text_to_speech_stream(text, voice)
    save_and_play_audio(response)

# Example usage
if __name__ == "__main__":
    speak("Hello from the world of Dungeons and Dragons!")
