import sys
import threading
import queue
import json
from voice_to_text import start_recording, stop_recording
from gpt_interface import run_conversation
from char_video import main as char_video_main, load_character_images, is_recording

# Define a global variable for the selected character JSON path
selected_character_json = None

exit_program = False

def set_exit_flag():
    global exit_program
    exit_program = True

def audio_thread_function(input_queue):
    recording = False
    global is_recording  # Access the global variable
    while not exit_program:
        try:
            user_input = input_queue.get(timeout=1)  # 1-second timeout
            if user_input == "":
                if recording:
                    stop_recording()
                    recording = False
                    is_recording = False  # Update the variable
                else:
                    start_recording()
                    recording = True
                    is_recording = True  # Update the variable
        except queue.Empty:
            continue


if __name__ == "__main__":
    # Check if a character JSON path is provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python main.py <character_json_path>")
        sys.exit(1)

    # Read the selected character JSON file and convert it to a dictionary
    with open(sys.argv[1], 'r') as f:
        character_data = json.load(f)

    # Set the selected character JSON path from the command line argument
    selected_character_json = sys.argv[1]

    input_queue = queue.Queue()

    # Load character images
    character, mouth, without_mouth = load_character_images(selected_character_json)

    # Open the file in write mode to overwrite the existing content
    with open('transcribed_text.txt', 'w') as file:
        file.write("Welcome to DND Chat GPT! Await instructions and information!")

    # Create threads
    audio_thread = threading.Thread(target=audio_thread_function, args=(input_queue,))
    chat_thread = threading.Thread(target=run_conversation, args=(character_data,))
    char_video_thread = threading.Thread(target=char_video_main, args=(character, mouth, without_mouth))

    # Set threads as daemon
    audio_thread.daemon = True
    chat_thread.daemon = True
    char_video_thread.daemon = True

    # Start threads
    audio_thread.start()
    chat_thread.start()
    char_video_thread.start()

    print("Press Enter to start/stop recording (Type 'exit' or Ctrl+C to exit)")
    try:
        while True:
            user_input = input()
            if user_input == "exit":
                set_exit_flag()
                break
            input_queue.put(user_input)
    except KeyboardInterrupt:
        set_exit_flag()
        print("Exiting...")

    # Give threads a moment to recognize the exit flag and clean up
    audio_thread.join(timeout=2)
    chat_thread.join(timeout=2)
    char_video_thread.join(timeout=2)
