import subprocess
import os
import sys
import speech_recognition as sr

# Set the root directory of the project
project_root_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.join(project_root_dir, '..')  # Move up one directory to get the project root
audio_dir = os.path.join(project_root_dir, 'audio')  # Path to the 'audio' directory

recording = False
temp_filename = os.path.join(audio_dir, "temp_audio.raw")  # Raw audio format in 'audio' directory
converted_filename = os.path.join(audio_dir, "converted_audio.wav")  # Converted WAV format in 'audio' directory

def capture_audio():
    recognizer = sr.Recognizer()
    with sr.AudioFile(converted_filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not hear your request.")
        except sr.RequestError:
            print("Sorry, the speech service is currently down; please try again later.")
        return None

def start_recording():
    global recording
    if not recording:
        print("Attempting to start recording...")
        recording = True
        # Start parec in the background
        process = subprocess.Popen(["parec", "--format=s16le", "--rate=44100", "--channels=1", temp_filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Process ID for parec: {process.pid}")

def stop_recording():
    global recording
    if recording:
        print("Attempting to stop recording...")
        recording = False
        # Kill parec process
        subprocess.run(["pkill", "parec"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Convert the raw audio to WAV format using ffmpeg
        subprocess.run(["ffmpeg", "-f", "s16le", "-ar", "44100", "-ac", "1", "-i", temp_filename, converted_filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.exists(converted_filename):
            print("Converted file exists. Transcribing...")
            transcribed_text = capture_audio()
            if transcribed_text:
                print(f"You said: {transcribed_text}")

                # Remove the existing contents of the text document, if it exists
                if os.path.exists("transcribed_text.txt"):
                    with open("transcribed_text.txt", "w") as text_file:
                        text_file.write("")

                # Save the transcribed text to the text document
                with open("transcribed_text.txt", "a") as text_file:
                    text_file.write(transcribed_text)

            os.remove(temp_filename)
            os.remove(converted_filename)
        else:
            print("Converted file does not exist.")
        subprocess.run(["pkill", "ffmpeg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    print("Press Enter to start/stop recording (Ctrl+C to exit)")
    try:
        while True:
            user_input = input()
            if user_input == "":
                if recording:
                    stop_recording()
                else:
                    start_recording()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
