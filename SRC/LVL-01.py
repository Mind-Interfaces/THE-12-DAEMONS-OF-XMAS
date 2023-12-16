# Anamelech Mini Game .. Exploding Christmas Trees
# 🏗️ Exploration of themes related to surprise and the challenge of balancing greed with charity.

import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Anammelech's Journey")

# Load images
player_image = pygame.image.load('anammelech_sprite.png')
tree_image = pygame.image.load('christmas_tree.png')
background_image = pygame.image.load('winter_forest.png')

# Game variables
player_position = [width//2, height//2]
tree_positions = [[random.randrange(width), random.randrange(height)] for _ in range(10)]
score = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_position[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_position[0] += 5
    if keys[pygame.K_UP]:
        player_position[1] -= 5
    if keys[pygame.K_DOWN]:
        player_position[1] += 5

    # Check for setting trees on fire
    for tree_position in tree_positions:
        if (player_position[0] in range(tree_position[0] - 10, tree_position[0] + 10) and 
            player_position[1] in range(tree_position[1] - 10, tree_position[1] + 10)):
            tree_positions.remove(tree_position)
            score += 1

    # Draw everything
    screen.blit(background_image, (0, 0))
    for tree_position in tree_positions:
        screen.blit(tree_image, tree_position)
    screen.blit(player_image, player_position)
    pygame.display.flip()

pygame.quit()

