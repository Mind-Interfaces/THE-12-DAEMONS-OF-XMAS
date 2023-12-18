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
Belial brought forth a mirror that reflected not only one's visage but also all their deepest desires and secrets; 
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
"the spoils of our labors! Through deception and manipulation, we have gathered these mortals together in one place at one time... And now it falls to me to determine their fates!" 
There was a collective growl from the assembled daemons as they anticipated the coming spectacle. Baal laughed cruelly, savoring the moment. "Let us begin..."
"""
import pygame
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
BACKGROUND_MUSIC_PATH = '../BGM/LVL-01/110-G-minor-1337.wav'
TREE_IMAGES = {
    "default": '../IMG/default_tree.png',
    "exploding": '../IMG/exploding_tree.png',
    "exploded": '../IMG/exploded_tree.png'
}
TITLE_IMAGE_PATH = '../IMG/game_title.png'
DEBUG_DAEMON_IMAGE_PATH = '../IMG/debug_daemon.png'  # Debug image

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The 12 Daemons of Xmas")

# Function to display debug daemon and message
def show_debug_message(message):
    debug_daemon_image = pygame.image.load(DEBUG_DAEMON_IMAGE_PATH)
    screen.blit(debug_daemon_image, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (100, 100))  # Adjust position as needed
    pygame.display.flip()
    time.sleep(5)

# Load assets with error handling
def load_asset(asset_path, asset_type='image'):
    try:
        if asset_type == 'image':
            return pygame.image.load(asset_path)
        elif asset_type == 'sound':
            return pygame.mixer.Sound(asset_path)
    except pygame.error as e:
        error_message = f"Error loading {asset_type}: {e}"
        print(error_message)
        show_debug_message(error_message)
        pygame.quit()
        raise SystemExit

# Load images
tree_images = {state: load_asset(path) for state, path in TREE_IMAGES.items()}
title_image = load_asset(TITLE_IMAGE_PATH)

# Load and play background music
try:
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
    pygame.mixer.music.play(-1)  # Loop the music
except pygame.error as e:
    show_debug_message(f"Error loading music: {e}")

# Game state variables
tree_state = "default"
tree_timer_start = 0
tree_explode_duration = 2

# Main game loop
running = True
intro_started = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Start intro sequence
    if not intro_started:
        tree_timer_start = time.time()
        intro_started = True

    # Tree animation logic
    time_elapsed = time.time() - tree_timer_start
    if tree_state == "default" and time_elapsed > tree_explode_duration / 2:
        tree_state = "exploding"
    elif tree_state == "exploding" and time_elapsed > tree_explode_duration:
        tree_state = "exploded"

    # Draw tree based on state
    screen.blit(tree_images[tree_state], (0, 0))

    # Show title after explosion
    if tree_state == "exploded":
        screen.blit(title_image, (0, 0))
        # Add any additional title screen logic here

    # Update display
    pygame.display.flip()

# Cleanup
pygame.quit()

