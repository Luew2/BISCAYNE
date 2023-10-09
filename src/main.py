import threading
import queue
from voice_to_text import start_recording, stop_recording
from gpt_interface import run_conversation
from char_video import main as char_video_main

exit_program = False

def set_exit_flag():
    global exit_program
    exit_program = True

def audio_thread_function(input_queue):
    recording = False
    while not exit_program:
        try:
            user_input = input_queue.get(timeout=1)  # 1-second timeout
            if user_input == "":
                if recording:
                    stop_recording()
                    recording = False
                else:
                    start_recording()
                    recording = True
        except queue.Empty:
            continue

if __name__ == "__main__":
    input_queue = queue.Queue()

    # Create threads
    audio_thread = threading.Thread(target=audio_thread_function, args=(input_queue,))
    chat_thread = threading.Thread(target=run_conversation)
    char_video_thread = threading.Thread(target=char_video_main)

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
