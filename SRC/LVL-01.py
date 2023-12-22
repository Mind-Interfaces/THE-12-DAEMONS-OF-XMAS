# Anamelech Mini Game .. Exploding Christmas Trees
# 🏗️ Exploration of themes related to surprise and the challenge of balancing greed with charity.
# 🏗️ Anamelech tests humanity's ability to balance greed and generosity through surprises.
# 🚧 Anamelech's test revolves around the balance between greed and generosity. 
# 🚧 It underscores the perennial struggle of human beings to strike an equilibrium between self-interest and benevolence, a test that transcends time.
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
import math
import time

# Initialize Pygame and Set Up Display
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Anamelech's Journey")

# Load images with error handling
def load_image(image_path):
    try:
        return pygame.image.load(image_path)
    except pygame.error as e:
        show_debug_message(f"Error loading image {image_path}: {e}")
        return None

# Load sound effects with error handling
def load_sound(sound_path):
    try:
        return pygame.mixer.Sound(sound_path)
    except pygame.error as e:
        show_debug_message(f"Error loading sound {sound_path}: {e}")
        return None

# Display debug message on the screen
def show_debug_message(message):
    debug_daemon_image = pygame.image.load('../IMG/DEBUG/debug_daemon.png')
    screen.blit(debug_daemon_image, (50, 50))
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (100, 150))
    pygame.display.flip()
    time.sleep(5)

# Load images and sound
player_image = load_image('../IMG/BOSS/anamelech_sprite.png')
tree_image = load_image('../IMG/TREE/christmas_tree.png')
background_image = load_image('../IMG/BACKGROUND/winter_forest.png')
santa_image = load_image('../IMG/NPC/santa_sprite.png')
explosion_sound = load_sound('../BGM/SFX/explosion_sound.wav')  # For tree ignition / TODO STUD

# Game Variables
player_position = [width // 2, height // 2]
tree_positions = [[random.randrange(width), random.randrange(height)] for _ in range(10)]
santa_position = [random.randrange(width), random.randrange(height)]
santa_speed = 2
santa_direction = random.choice([(santa_speed, 0), (-santa_speed, 0), (0, santa_speed), (0, -santa_speed)])
score = 0
start_time = time.time()

# Font for displaying text
font = pygame.font.Font(None, 36)

# Movement and collision functions
def move_santa():
    global santa_position, santa_direction
    santa_position[0] += santa_direction[0]
    santa_position[1] += santa_direction[1]
    if random.random() < 0.01:
        santa_direction = random.choice([(santa_speed, 0), (-santa_speed, 0), (0, santa_speed), (0, -santa_speed)])

def check_collision(player_pos, other_pos, distance=20):
    return math.hypot(player_pos[0] - other_pos[0], player_pos[1] - other_pos[1]) < distance

def draw_text(text, position):
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, position)

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

    # Santa movement
    move_santa()

    # Check for setting trees on fire
    for tree_position in tree_positions[:]:
        if check_collision(player_position, tree_position):
            tree_positions.remove(tree_position)
            score += 1
            explosion_sound.play()  # Play explosion sound on tree ignition

    # Collision with Santa Claus
    if check_collision(player_position, santa_position):
        show_debug_message("Caught by Santa! Game Over.")
        running = False

    # Draw everything
    screen.blit(background_image, (0, 0))
    for tree_position in tree_positions:
        screen.blit(tree_image, tree_position)
    screen.blit(santa_image, santa_position)
    screen.blit(player_image, player_position)

    # Display score and time
    elapsed_time = int(time.time() - start_time)
    draw_text(f"Score: {score}", (10, 10))
    draw_text(f"Time: {elapsed_time}", (10, 40))

    pygame.display.flip()

pygame.quit()
