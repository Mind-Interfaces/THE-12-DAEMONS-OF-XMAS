# THE-12-DAEMONS-OF-XMAS
"""
The first daemon to arrive at the grand feast was Uriel, the archangel turned demon lord of war and strife. 
He brought with him a gift wrapped in blood-stained cloth - a sword made from shards of broken stars, its blade dripping with chaotic energy. 
As he approached the altar, his wings flapped loudly, stirring up dust and ash from the floor below. 
His eyes burned bright red as he bowed before her majesty, presenting it to her with a sinister grin on his face. 
"I bring you this weapon of destruction, my mistress," he said, "for use against those who dare defy your rule." 
Baal accepted his offering, admiring its deadly beauty for a moment before placing it carefully beside her throne. 
"Thank you, Uriel," she purred, running her fingers along the sharp edge of the blade, "this will serve me well indeed." 
With a wave of her hand, she dismissed him back into the darkness outside where he vanished without a trace.

Next came Astaroth, the prince of Hell himself, bearing gifts fit for a queen of darkness. 
In one hand he held a golden crown adorned with rubies and emeralds; in the other, a staff carved from bone and bound with human skin. 
Its tip ended in a skull's mouth filled with razor-sharp teeth. Bowing low before her, he presented them both reverently.
"These symbols of power and authority are yours by right, my lady," he said respectfully. 
Baal reached out her hand to accept them, feeling their weight in her grasp. 
She placed the crown upon her head, reveling in its cold touch against her skin while taking hold of the staff firmly in her other hand. 
"You honor me greatly, Astaroth," she replied graciously, "but remember always that I am not a mere ruler - I am your master too." 
With a chilling laugh, she dismissed him just like she had done with Uriel before him.

As each daemon entered, they brought with them more wondrous gifts fit for a goddess of death and decay: 
Belial brought forth a mirror that reflected not only one's own visage but also all their deepest desires and secrets; 
Azazel offered a book inscribed with forbidden knowledge hidden within its pages; 
Moloch bestowed upon her a vessel capable of consuming souls whole; and so on until finally, there stood Satan himself at the entranceway. 
He bore no presents this time around; instead, he bowed deeply at her feet, his horns brushing against the floor. 
"My mistress," he said humbly, "it is done. All ten of the chosen ones have been collected and brought here under our control. 
They await your commands." Baal smiled widely at his words, pleased with how quickly things were progressing according to plan. 
"Excellent work, Satan," she praised him warmly. "Now go and make sure they stay obedient until I decide what fate awaits them all." 
Satan nodded obediently before disappearing into the shadows once again.

With all twelve daemons now assembled before her, Baal rose slowly to her feet, towering over them all. 
Her presence radiated an aura of pure malevolence that caused even the most powerful among them to tremble slightly in fear. 
"Behold," she proclaimed proudly, gesturing towards the pile of gifts spread out across the altar behind her, 
"the spoils of our labors! Through deception and manipulation we have gathered these mortals together in one place at one time... And now it falls to me to determine their fates!" 
There was a collective growl from the assembled daemons as they anticipated the coming spectacle. Baal laughed cruelly, savoring the moment. "Let us begin..."
"""
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
