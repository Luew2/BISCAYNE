import pygame
import os
import time
from elevenlabs_interface import audio_dir
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

# Set the root directory of the project
project_root_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.join(project_root_dir, '..')  # Move up one directory to get the project root

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080

# Colors
WHITE = (255, 255, 255)

# Create screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image Bopper")
clock = pygame.time.Clock()

def get_latest_image(filename_prefix):
    character_dir = os.path.join(project_root_dir, 'character')
    files = [f for f in os.listdir(character_dir) if f.startswith(filename_prefix)]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(character_dir, x)), reverse=True)
    if files:
        return os.path.join(character_dir, files[0])
    return None

character_path = get_latest_image('character_without_mouth')
mouth_path = get_latest_image('mouth_same_dim')

if character_path and mouth_path:
    character = pygame.image.load(character_path)
    mouth = pygame.image.load(mouth_path)
else:
    print("Error: Could not find the required images.")
    exit()

character_rect = character.get_rect(center=(WIDTH/2, HEIGHT/2))
mouth_rect = mouth.get_rect(center=(WIDTH/2, HEIGHT/2))

# Variables for vertical movement
speed = 20  # Increased speed for more rapid movement
moving_up = True
max_movement = 5

def get_audio_segments():
    audio_path = os.path.join(audio_dir, "temp_audio.wav")
    audio = AudioSegment.from_mp3(audio_path)
    # Adjusted parameters for more precise detection
    return detect_nonsilent(audio, min_silence_len=50, silence_thresh=-30)


def is_sound_playing(current_time, segments):
    return any(start <= current_time <= end for start, end in segments)

def main():
    global moving_up
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
        screen.blit(character, character_rect.topleft)
        screen.blit(mouth, mouth_rect.topleft)

        pygame.display.flip()
        clock.tick(60)
        time.sleep(0.01)

    pygame.quit()

if __name__ == "__main__":
    print(audio_dir)
    main()
