# THE-12-DAEMONS-OF-XMAS
import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The 12 Daemons of Xmas")

# Load images (replace with actual file paths)
default_tree_image = pygame.image.load('default_tree.png')  # Default tree sprite
exploding_tree_image = pygame.image.load('exploding_tree.png')  # Exploding tree sprite
exploded_tree_image = pygame.image.load('exploded_tree.png')  # Exploded tree sprite
background_image = pygame.image.load('intro_background.png')
title_image = pygame.image.load('game_title.png')

# Load sound effects (replace with actual file paths)
explosion_sound = pygame.mixer.Sound('explosion_sound.wav')

# Tree state variables
tree_state = "default"  # Can be "default", "exploding", or "exploded"
tree_timer_start = 0
tree_explode_duration = 2  # Duration for the exploding effect

# Introductory Scene Variables
intro_done = False
tree_scene_done = False
start_time = time.time()
intro_duration = 5  # seconds

# Function to draw the tree based on its current state
def draw_tree():
    if tree_state == "default":
        screen.blit(default_tree_image, (0, 0))
    elif tree_state == "exploding":
        screen.blit(exploding_tree_image, (0, 0))
    elif tree_state == "exploded":
        screen.blit(exploded_tree_image, (0, 0))

# Function to play explosion sound
def play_explosion_sound():
    explosion_sound.play()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Introductory Scenes Logic
    if not intro_done:
        screen.blit(background_image, (0, 0))
        if time.time() - start_time > intro_duration:
            intro_done = True
            tree_timer_start = time.time()  # Start timer for tree explosion
        else:
            continue  # Skip the rest of the loop

    # Christmas Tree Scene Logic
    if intro_done and not tree_scene_done:
        draw_tree()
        elapsed = time.time() - tree_timer_start
        if elapsed > tree_explode_duration:
            if tree_state != "exploded":  # Play sound only once
                play_explosion_sound()
            tree_state = "exploded"
            tree_scene_done = True
        elif elapsed > tree_explode_duration / 2 and tree_state != "exploding":
            tree_state = "exploding"

    # Display Title Screen
    if tree_scene_done:
        screen.blit(title_image, (0, 0))
        # TODO: Add any title screen interactions or animations here

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
