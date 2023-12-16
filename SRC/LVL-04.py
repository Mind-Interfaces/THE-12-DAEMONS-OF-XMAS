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
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lucifuge's Hide-and-Seek")

# Load images (replace with your own assets)
lilith_image = pygame.image.load('lilith_sprite.png')
mask_images = {
    'Famine': pygame.image.load('famine_mask.png'),
    'War': pygame.image.load('war_mask.png'),
    'Pestilence': pygame.image.load('pestilence_mask.png'),
    'Death': pygame.image.load('death_mask.png')
}
background_image = pygame.image.load('tower_background.png')

# Game variables
lilith_position = [width // 2, height // 2]
mask_positions = {name: [random.randrange(width), random.randrange(height)] for name in mask_images}
collected_masks = []

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
        lilith_position[0] -= 5
    if keys[pygame.K_RIGHT]:
        lilith_position[0] += 5
    if keys[pygame.K_UP]:
        lilith_position[1] -= 5
    if keys[pygame.K_DOWN]:
        lilith_position[1] += 5

    # Mask collection logic
    for name, position in mask_positions.items():
        if pygame.Rect(lilith_position[0], lilith_position[1], lilith_image.get_width(), lilith_image.get_height()).colliderect(
            pygame.Rect(position[0], position[1], mask_images[name].get_width(), mask_images[name].get_height())):
            collected_masks.append(name)
            del mask_positions[name]

    # Draw everything
    screen.blit(background_image, (0, 0))
    for name, position in mask_positions.items():
        screen.blit(mask_images[name], position)
    screen.blit(lilith_image, lilith_position)

    # Display collected masks
    draw_text(f"Masks Collected: {', '.join(collected_masks)}", (10, 10))

    pygame.display.flip()

pygame.quit()

