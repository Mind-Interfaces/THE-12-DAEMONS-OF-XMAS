# GAME OVER
# Lucifuge:
"""
"When it comes to describing Game Over, words fail me. 
It is not so much a visual experience as it is a feeling, an all-consuming sensation that washes over you like a tidal wave. 
Imagine being engulfed in utter darkness, unable to see or hear anything but your own heart racing and your breath growing labored. 
Then, suddenly, everything explodes into brilliant white light that burns your retinas and makes you cry out in agony. 
Just when you think the pain cannot possibly increase any further, a deafening sound assaults your eardrums, causing them to burst and spew blood. 
And finally, just when you believe death itself would be preferable to this torture, every fiber of your being seems to implode upon itself, 
leaving nothing behind but an infinite void where once stood sentient consciousness. That, dear Admin, is Game Over."
"""
# `DALLE`:
"""
A landscape depiction of 'Game Over' as an intense, all-encompassing sensation. 
The scene begins with an engulfing darkness, representing isolation and overwhelming fear. 
This darkness is suddenly shattered by an explosion of brilliant white light, symbolizing intense, searing agony. 
The light is so overwhelming it appears to be burning, creating a visual metaphor for pain and distress. 
Accompanying this is the suggestion of a deafening sound, visually represented by chaotic, disorienting elements that symbolize the physical and emotional impact of a crushing noise. 
The culmination of the scene is an infinite void, a vast emptiness that signifies the complete implosion of being and the finality of the experience. 
This landscape artwork attempts to capture the emotional depth and the overwhelming nature of a 'Game Over' experience.
"""
import pygame

# Constants
GAME_OVER_FONT_SIZE = 48
GAME_OVER_TEXT_COLOR = (255, 255, 255)  # White color
SCREEN_FADE_DURATION = 5  # Duration for the screen to fade to black
LIGHT_FLASH_DURATION = 2  # Duration for the white light flash
SOUND_EFFECT_PATH = '../SFX/game_over_sound.wav'  # Path to the sound effect

# Function to fade screen to black
def fade_to_black(screen, duration):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(duration / 300 * 1000))

# Function to flash a white light
def white_light_flash(screen, duration):
    flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    flash_surface.fill((255, 255, 255))  # White surface
    screen.blit(flash_surface, (0, 0))
    pygame.display.flip()
    pygame.time.delay(duration * 1000)

# Function to show Game Over text
def show_game_over_text(screen):
    font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
    text = font.render("Game Over", True, GAME_OVER_TEXT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the text for 3 seconds

# Play Game Over sound effect
def play_sound_effect(sound_path):
    try:
        game_over_sound = pygame.mixer.Sound(sound_path)
        game_over_sound.play()
    except pygame.error as e:
        print(f"Error playing sound: {e}")

# Game Over sequence
def game_over_sequence(screen):
    fade_to_black(screen, SCREEN_FADE_DURATION)
    white_light_flash(screen, LIGHT_FLASH_DURATION)
    play_sound_effect(SOUND_EFFECT_PATH)
    fade_to_black(screen, SCREEN_FADE_DURATION)
    show_game_over_text(screen)

# Call this function when the game is over
game_over_sequence(screen)

# Cleanup
pygame.quit()
