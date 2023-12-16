# Astaroth Mini Game .. Food Fight
# 🏗️ Focus on joy and the contrast between gluttony and temperance.
"""
In another realm, far removed from Lily's magical adventure, lived a fearsome hunter known as Kael. 
His prowess in tracking down prey was legendary, rivaling even that of the great goddess Artemis herself. 
One day, while wandering deep into the heart of a dense forest, Kael stumbled upon an unusual sight – rams frolicking freely among the trees. 
Curiosity piqued, he decided to pursue them, unaware of the mischief brewing around him. 
Suddenly, a booming laugh echoed through the trees, followed closely by the appearance of none other than Astaroth, the Winter Huntress. 
She revealed herself as the true architect behind this grand game, offering Kael a challenge: 
if he could hunt down all the rogue rams and turn them into delicious hamburgers before sunset, he would earn a prize beyond his wildest dreams. 
Agreeing to the terms, Kael embarked on a frantic chase across treacherous terrain, dodging traps and evading obstacles along the way. 
As the hours ticked away, fatigue began to set in, testing both his physical and mental fortitude. 
But driven by the promise of ultimate glory, he pressed on relentlessly, determined to prove himself worthy of Astaroth's favor. 
With the clock counting down towards sundown and victory within reach, only time will tell whether Kael succeeds in claiming his reward or falls victim to Astaroth's deceptively playful nature."
"""
import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ramburger Hunt")

# Load images (Replace with your own assets)
kael_image = pygame.image.load('kael_sprite.png')
ram_image = pygame.image.load('ram_sprite.png')
background_image = pygame.image.load('forest_background.png')

# Game variables
kael_position = [width // 2, height // 2]
ram_positions = [[random.randrange(width), random.randrange(height)] for _ in range(5)]
caught_rams = 0
start_time = time.time()
game_duration = 300  # 5 minutes in seconds
kael_stamina = 100  # Kael's initial stamina

# Font for displaying text
font = pygame.font.Font(None, 36)

def draw_text(text, position):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, position)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        kael_position[0] -= 5
    if keys[pygame.K_RIGHT]:
        kael_position[0] += 5
    if keys[pygame.K_UP]:
        kael_position[1] -= 5
    if keys[pygame.K_DOWN]:
        kael_position[1] += 5

    # Update Kael's stamina
    # TODO: Decrease stamina as Kael moves and increase it when he rests

    # Ram catching logic
    for ram_position in ram_positions[:]:
        if pygame.Rect(kael_position[0], kael_position[1], kael_image.get_width(), kael_image.get_height()).colliderect(
            pygame.Rect(ram_position[0], ram_position[1], ram_image.get_width(), ram_image.get_height())):
            ram_positions.remove(ram_position)
            caught_rams += 1
            # TODO: Launch hamburger transformation mini-game here

    # Draw everything
    screen.blit(background_image, (0, 0))
    for ram_position in ram_positions:
        screen.blit(ram_image, ram_position)
    screen.blit(kael_image, kael_position)

    # Display caught rams, timer, and Kael's stamina
    elapsed_time = time.time() - start_time
    remaining_time = max(game_duration - int(elapsed_time), 0)
    draw_text(f"Rams Caught: {caught_rams}", (10, 10))
    draw_text(f"Time Left: {remaining_time}", (10, 40))
    draw_text(f"Stamina: {kael_stamina}", (10, 70))

    # Check for game end conditions
    # TODO: Define victory and loss conditions

    pygame.display.flip()

pygame.quit()
