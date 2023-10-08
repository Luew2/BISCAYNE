# voice_to_text.py
import speech_recognition as sr

def capture_audio():
    """
    Captures audio from the user's microphone and converts it to text.
    Returns the transcribed text.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio_data = recognizer.listen(source)
        try:
            # Convert audio to text using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not hear your request.")
        except sr.RequestError:
            print("Sorry, the speech service is currently down; please try again later.")
        return None

if __name__ == "__main__":
    transcribed_text = capture_audio()
    if transcribed_text:
        print(f"You said: {transcribed_text}")
