import os
import io
import requests
from dotenv import load_dotenv
import pydub
from pydub.playback import play

# Load environment variables from .env file
load_dotenv()

# Initialize Elven Labs API Key from environment variable
ELVENLABS_API_KEY = os.environ.get("ELVENLABS_API_KEY")

BASE_URL = "https://api.elevenlabs.io/v1"
CHUNK_SIZE = 1024

def text_to_speech_stream(text, voice_id="jsCqWAovK2LkecY7zXl4"):
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
    audio = pydub.AudioSegment.from_mp3(io.BytesIO(audio_data))
    play(audio)

def speak(text, voice):
    response = text_to_speech_stream(text, voice)
    save_and_play_audio(response)

# Example usage
if __name__ == "__main__":
    speak("Hello from the world of Dungeons and Dragons!")
