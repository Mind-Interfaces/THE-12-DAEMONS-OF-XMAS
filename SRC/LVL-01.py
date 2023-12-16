# Anamelech Mini Game .. Exploding Christmas Trees
# 🏗️ Exploration of themes related to surprise and the challenge of balancing greed with charity.
"""
Once upon a time, in a world where darkness still held sway over light, there lived a young girl named Lily. 
She was known far and wide for her boundless curiosity and innocent spirit, traits that often landed her in trouble despite her mother's best efforts to keep her safe. 
On one particularly stormy night, as Lily defied her mother once again by venturing outside after bedtime, she stumbled upon something truly extraordinary – a grove filled with trees unlike any she had ever seen. 
They were tall and majestic, adorned with colorful lights and sparkling ornaments, yet there was an air of menace surrounding them that made her blood run cold. 
Despite her instincts screaming at her to flee, Lily couldn't tear her eyes away from these enchanting yet ominous creatures. 
That's when Anamelech appeared before her, cloaked in shadows and shrouded in mystery. He offered Lily a deal: 
if she could successfully ignite all of the trees without being caught by Santa Claus himself, he would grant her one wish of her choosing. 
Tempted by the prospect of having anything she desired, Lily accepted his challenge without hesitation. 
And thus began a thrilling game of cat and mouse through the darkened woods, pitting Lily's wits against Santa's omniscience and Anamelech's sinister machinations. 
With each tree that fell victim to flames, Lily drew closer to fulfilling her end of the bargain. 
But as time wore on and exhaustion set in, she found herself questioning whether the price she might pay for achieving her desires would be worth the risk. 
Only time would tell if Lily would emerge victorious or succumb to the lures of corruption laid out by Anamelech, the Dark Christmas Tree Angel.
"""
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

