# Baal Mini Game .. 
# 🏗️ Examination of trust, and the struggle between lust and chastity.
# 🏗️ Baal tempts with desire and lust, testing humanity's morality against adultery and chastity.
# 🚧 Baal's challenge concerning desire and lust delves into the complex realm of human morality, particularly concerning fidelity and chastity. 
# 🚧 This theme has been explored in countless philosophical and ethical discussions over the ages.
'''
Very well, then let us simplify it even further. 
Instead of choosing truth or dare, players simply answer multiple-choice questions about love and desire. 
Each correct answer earns them a point, while incorrect ones result in a loss. 
Throughout the game, Baal may offer subtle hints via voice prompts to nudge players towards the correct answers. 
However, accepting her assistance comes at the cost of increased difficulty in subsequent questions. 
The goal remains the same – accruing enough points before running out altogether. 
This way, even novice players can enjoy exploring the thrill of seduction within the confines of a single-player experience.
'''
import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Baal's Labyrinth of Desires")

# Colors and Assets
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
PINK = (255, 0, 255)

player_sprite = pygame.image.load('../IMG/CHAR/player_sprite.png')
wall_tile = pygame.image.load('../IMG/TILE/wall_tile.png')
background_music = pygame.mixer.Sound('../BGM/LVL-03/background_music.wav')

# Maze settings
maze_rows = 10
maze_columns = 10
cell_size = 50
maze = [[0 for _ in range(maze_columns)] for _ in range(maze_rows)]

# Player settings
player_pos = [0, 0]
player_color = WHITE
player_size = cell_size // 2

# Font and Questions
font = pygame.font.Font(None, 36)
questions = [{"text": "True or False: ...", "correct_option": "True", "options": ["True", "False"]}]
current_question = None
score = 0
game_over = False
start_time = pygame.time.get_ticks()
time_limit = 300000  # 5 minutes in milliseconds

def load_image(image_path):
    try:
        return pygame.image.load(image_path)
    except pygame.error as e:
        show_debug_message(f"Error loading image {image_path}: {e}")
        return None

def show_debug_message(message):
    debug_daemon_image = load_image('../IMG/DEBUG/debug_daemon.png')
    screen.blit(debug_daemon_image, (50, 50))
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 0, 0))
    screen.blit(text, (100, 150))
    pygame.display.flip()
    time.sleep(5)

def generate_maze():
    for row in range(maze_rows):
        for col in range(maze_columns):
            if random.choice([True, False]):
                maze[row][col] = 1

def draw_iso_tile(x, y, tile_type):
    iso_x, iso_y = (x - y) * cell_size + screen_width // 2, (x + y) * cell_size // 4
    color = GREY if tile_type == 1 else BLACK
    points = [(iso_x, iso_y), (iso_x + cell_size//2, iso_y + cell_size//4),
              (iso_x, iso_y + cell_size//2), (iso_x - cell_size//2, iso_y + cell_size//4)]
    pygame.draw.polygon(screen, color, points)

def draw_maze_iso():
    for row in range(maze_rows):
        for col in range(maze_columns):
            draw_iso_tile(col, row, maze[row][col])

def iso_to_screen(x, y):
    screen_x = (x - y) * cell_size + screen_width // 2
    screen_y = (x + y) * cell_size // 4
    return screen_x, screen_y

def draw_player_iso():
    screen_x, screen_y = iso_to_screen(player_pos[0], player_pos[1])
    pygame.draw.rect(screen, player_color, (screen_x, screen_y, player_size, player_size // 2))

def move_player_iso(key):
    dx, dy = 0, 0
    if key == pygame.K_UP:
        dy = -1
    elif key == pygame.K_DOWN:
        dy = 1
    elif key == pygame.K_LEFT:
        dx = -1
    elif key == pygame.K_RIGHT:
        dx = 1

    new_pos = [player_pos[0] + dx, player_pos[1] + dy]
    if 0 <= new_pos[0] < maze_columns and 0 <= new_pos[1] < maze_rows and maze[new_pos[1]][new_pos[0]] == 0:
        player_pos[:] = new_pos

def check_question():
    global current_question, score
    if player_pos == [maze_columns - 1, maze_rows - 1]:
        current_question = random.choice(questions)
        present_question(current_question)

def present_question(question):
    global score, game_over
    # Simple question routine (to be expanded later)
    answer = input(question["text"] + " " + "/".join(question["options"]) + ": ")
    if answer.lower() == question["correct_option"].lower():
        score += 1
    else:
        game_over = True

def draw_text(text, position):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, position)

def draw_score():
    draw_text(f"Score: {score}", (10, 10))

def check_time():
    global game_over
    if pygame.time.get_ticks() - start_time > time_limit:
        game_over = True

generate_maze()
background_music.play(-1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            move_player_iso(event.key)

    if game_over:
        show_debug_message("Game Over")
        break

    check_question()
    check_time()

    screen.fill(BLACK)
    draw_maze_iso()
    draw_player_iso()
    draw_score()

    pygame.display.flip()

pygame.quit()
sys.exit()
