# Lucifuge Mini Game ...
# 🏗️ Delving into fear and the battle between sloth and diligence.
# 🏗️ Lucifuge instills fear and laziness, testing humanity's determination against sloth and diligence.
# 🚧 Lucifuge's test, which involves fear and laziness, probes into the depths of human determination and the perennial struggle against sloth. 
# 🚧 It highlights the significance of diligence in the face of fear-induced inertia.
"""
During a snow-covered winter solstice celebration. 
Guests dressed in festive attire gather outside to partake in traditional festivities such as feasting and dancing. 
Among them stands Lilith, drawn to the mysterious figure of Lucifuge Rofocale standing alone atop a tall tower overlooking the revelry below. 
Determined to unravel the enigma surrounding her, she decides to accept her invitation to play a dangerous game of hide-and-seek. 
Throughout the game, players must navigate through various rooms decorated with Yuletide cheer yet tainted by hints of darker forces at work. 
Along the way, they encounter masks representing different aspects of death – 
Famine transforming food into rot; War causing discord and chaos; Pestilence spreading disease and illness; 
and finally, Death itself waiting patiently in the shadows for its next victim. 
Collecting each mask bestows upon Lilith powerful abilities but also brings her one step closer to succumbing to their respective curses. 
Ultimately, she must face off against Lucifuge herself in a climactic dance of life and death, where the fate of not only herself but also everyone else present hangs in the balance.
"""
import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lucifuge's Hide-and-Seek")

# Load images and sounds
def load_image(image_path):
    try:
        return pygame.image.load(image_path)
    except pygame.error as e:
        show_debug_message(f"Error loading image {image_path}: {e}")
        return None

def load_sound(sound_path):
    try:
        return pygame.mixer.Sound(sound_path)
    except pygame.error as e:
        show_debug_message(f"Error loading sound {sound_path}: {e}")
        return None

# Debug Daemon for error handling
def show_debug_message(message):
    debug_daemon_image = load_image('../IMG/DEBUG/debug_daemon.png')
    screen.blit(debug_daemon_image, (50, 50))
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (100, 150))
    pygame.display.flip()
    time.sleep(5)

# Game assets
lilith_image = load_image('../IMG/CHAR/lilith_sprite.png')
mask_images = {
    'Famine': load_image('../IMG/SPRITE/famine_mask.png'),
    'War': load_image('../IMG/SPRITE/war_mask.png'),
    'Pestilence': load_image('../IMG/SPRITE/pestilence_mask.png'),
    'Death': load_image('../IMG/SPRITE/death_mask.png')
}
background_image = load_image('../IMG/BACKGROUND/tower_background.png')
background_music = load_sound('../BGM/LVL-04/background_music.wav')
mask_pickup_sound = load_sound('../BGM/SFX/mask_pickup_sound.wav')
final_showdown_music = load_sound('../BGM/SFX/final_showdown_music.wav')

# Additional Game Variables
traps = []  # Coordinates for traps
trap_image = load_image('../IMG/SRITE/trap_sprite.png')
trap_triggered_sound = load_sound('../BGM/SFX/trap_sound.wav')
score = 0

# Generate Traps
for _ in range(10):
    traps.append([random.randrange(width), random.randrange(height)])

# Trap Triggering Logic
def trigger_traps():
    global score
    for trap in traps:
        if pygame.Rect(lilith_position[0], lilith_position[1], lilith_image.get_width(), lilith_image.get_height()).colliderect(
                pygame.Rect(trap[0], trap[1], trap_image.get_width(), trap_image.get_height())):
            trap_triggered_sound.play()
            score -= 5
            traps.remove(trap)

# Player Movement Function
def move_lilith():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        lilith_position[0] -= 5
    if keys[pygame.K_RIGHT]:
        lilith_position[0] += 5
    if keys[pygame.K_UP]:
        lilith_position[1] -= 5
    if keys[pygame.K_DOWN]:
        lilith_position[1] += 5

# Mask Collection Logic
def collect_masks():
    for name, position in mask_positions.items():
        if pygame.Rect(lilith_position[0], lilith_position[1], lilith_image.get_width(), lilith_image.get_height()).colliderect(
            pygame.Rect(position[0], position[1], mask_images[name].get_width(), mask_images[name].get_height())):
            collected_masks.append(name)
            del mask_positions[name]
            mask_pickup_sound.play()

# Drawing Game Elements
def draw_game_elements():
    screen.blit(background_image, (0, 0))
    for name, position in mask_positions.items():
        screen.blit(mask_images[name], position)
    screen.blit(lilith_image, lilith_position)
    draw_text(f"Masks Collected: {', '.join(collected_masks)}", (10, 10))

# Final Showdown with Lucifuge
def final_showdown():
    final_showdown_music.play()
    global running
    while boss_health > 0 and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    create_fireball()
                move_lilith()

        move_fireballs()
        screen.fill(BLACK)
        screen.blit(lucifuge_image, lucifuge_position)
        draw_game_elements()
        draw_fireballs()
        display_score()
        pygame.display.flip()

    # Handle victory or defeat
    if boss_health <= 0:
        show_victory_screen()
    else:
        show_defeat_screen()

# Show Victory Screen Function
def show_victory_screen():
    victory_image = load_image('../IMG/BACKGROUND/victory_screen.png')
    screen.blit(victory_image, (0, 0))
    pygame.display.flip()
    time.sleep(5)  # Display for 5 seconds

# Show Defeat Screen Function
def show_defeat_screen():
    defeat_image = load_image('../IMG/BACKGROUND/defeat_screen.png')
    screen.blit(defeat_image, (0, 0))
    pygame.display.flip()
    time.sleep(5)  # Display for 5 seconds

# Main Game Loop
background_music.play(-1)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            move_lilith()

    collect_masks()
    trigger_traps()
    if len(collected_masks) == len(mask_images):
        final_showdown()

    screen.fill(BLACK)
    draw_game_elements()
    for trap in traps:
        screen.blit(trap_image, trap)
    display_score()
    pygame.display.flip()

pygame.quit()
sys.exit()
