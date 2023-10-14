import pygame
import os
import time
import json
from elevenlabs_interface import audio_dir
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from voice_to_text import start_recording, stop_recording

# Set the root directory of the project
project_root_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.join(project_root_dir, '..')  # Move up one directory to get the project root

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Recording Button Attributes
RECORDING_BUTTON_RADIUS = 20
RECORDING_BUTTON_POS = (WIDTH // 2, HEIGHT - RECORDING_BUTTON_RADIUS - 30)  # 30 pixels offset from the bottom

# Create screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Character")
clock = pygame.time.Clock()

# Variables for vertical movement
speed = 20  # Increased speed for more rapid movement
moving_up = True
max_movement = 5
is_recording = False

def draw_recording_indicator():
    color = RED if is_recording else (200, 200, 200)  # Light gray if not recording, red if recording
    pygame.draw.circle(screen, color, RECORDING_BUTTON_POS, RECORDING_BUTTON_RADIUS)

def get_image(character_dir, filename):
    image_path = os.path.join(character_dir, filename)
    if os.path.isfile(image_path):
        return image_path
    return None

def load_character_images(character_json_path):
    global character, mouth, without_mouth, mouth_rect
    with open(character_json_path, "r") as json_file:
        character_data = json.load(json_file)

    character_dir = os.path.join(project_root_dir, 'character')
    character_path = get_image(character_dir, character_data["image"])
    mouth_path = get_image(character_dir, character_data["mouth"])
    without_mouth_path = get_image(character_dir, character_data["without_mouth"])

    if character_path and mouth_path and without_mouth_path:
        character = pygame.image.load(character_path)
        mouth = pygame.image.load(mouth_path)
        without_mouth = pygame.image.load(without_mouth_path)
        mouth_rect = mouth.get_rect(center=(WIDTH/2, HEIGHT/2))  # Initialize mouth_rect
    else:
        print("Error: Could not find the required images.")
        exit()

    return character, mouth, without_mouth

def get_audio_segments():
    audio_path = os.path.join(audio_dir, "temp_audio.wav")
    audio = AudioSegment.from_mp3(audio_path)
    # Adjusted parameters for more precise detection
    return detect_nonsilent(audio, min_silence_len=50, silence_thresh=-30)

def is_sound_playing(current_time, segments):
    return any(start <= current_time <= end for start, end in segments)

def main(character, mouth, without_mouth):
    global moving_up
    global is_recording

    character_rect = character.get_rect(center=(WIDTH/2, HEIGHT/2))
    mouth_rect = mouth.get_rect(center=(WIDTH/2, HEIGHT/2))

    audio_path = os.path.join(audio_dir, "temp_audio.wav")
    last_mod_time = os.path.getmtime(audio_path)
    running = True
    base_y = mouth_rect.y
    segments = get_audio_segments()
    audio_started = False  # New variable to check if audio has started

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse button was pressed
                mouse_pos = pygame.mouse.get_pos()
                distance_to_button = ((mouse_pos[0] - RECORDING_BUTTON_POS[0])**2 + (mouse_pos[1] - RECORDING_BUTTON_POS[1])**2)**0.5
                if distance_to_button <= RECORDING_BUTTON_RADIUS:  # Mouse clicked inside the button
                    is_recording = not is_recording  # Toggle the recording state
                    if is_recording:
                        start_recording()
                    else:
                        stop_recording()
        current_mod_time = os.path.getmtime(audio_path)
        if current_mod_time != last_mod_time:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            last_mod_time = current_mod_time
            segments = get_audio_segments()
            audio_started = True  # Set to True once audio starts playing

        current_time = pygame.mixer.music.get_pos()
        sound_playing = is_sound_playing(current_time, segments)

        if sound_playing:
            moving_up = False
        else:
            moving_up = True

        # Only update mouth position if audio has started playing
        if audio_started:
            if moving_up and mouth_rect.y < base_y + max_movement:
                mouth_rect.y += speed
            elif not moving_up and mouth_rect.y > base_y:
                mouth_rect.y -= speed

        # Reset mouth position if audio is complete
        if not pygame.mixer.music.get_busy() and mouth_rect.y != base_y:
            mouth_rect.y = base_y

        screen.fill(WHITE)
        screen.blit(without_mouth, character_rect.topleft)
        screen.blit(mouth, mouth_rect.topleft)
        draw_recording_indicator()

        pygame.display.flip()
        clock.tick(60)
        time.sleep(0.01)

    pygame.quit()