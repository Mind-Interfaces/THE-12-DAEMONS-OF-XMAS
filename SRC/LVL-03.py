# Baal Mini Game .. 
# 🏗️ Examination of trust, and the struggle between lust and chastity.
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

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Baal's Labyrinth of Desires")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
RED = (255, 0, 0)

# Maze settings
maze_rows = 10
maze_columns = 10
cell_size = 50
maze = [[0 for _ in range(maze_columns)] for _ in range(maze_rows)]  # 0 represents open path

# Player settings
player_pos = [0, 0]  # Starting at top-left corner
player_color = WHITE
player_size = cell_size - 10

# Font setup
font = pygame.font.Font(None, 36)

# Sample questions (expand this with real questions)
questions = [
    {"text": "Question 1: ...", "correct_option": "A", "options": ["A", "B", "C"]},
    {"text": "Question 2: ...", "correct_option": "B", "options": ["A", "B", "C"]},
    {"text": "Question 3: ...", "correct_option": "C", "options": ["A", "B", "C"]}
]

# Game variables
current_question = None
score = 0
baal_hint_active = False
difficulty_level = 1  # Increase this when Baal's hint is used

def generate_maze():
    """Generate a simple maze."""
    for row in range(maze_rows):
        for col in range(maze_columns):
            if random.choice([True, False]):
                maze[row][col] = 1  # Set wall

def draw_maze():
    """Draw the maze on the screen."""
    for row in range(maze_rows):
        for col in range(maze_columns):
            color = GREY if maze[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col*cell_size, row*cell_size, cell_size, cell_size))

def draw_player():
    """Draw the player on the screen."""
    pygame.draw.rect(screen, player_color, 
                     (player_pos[0]*cell_size + 5, player_pos[1]*cell_size + 5, player_size, player_size))

def move_player(key):
    """Move the player based on key input."""
    new_pos = list(player_pos)
    if key == pygame.K_UP:
        new_pos[1] -= 1
    elif key == pygame.K_DOWN:
        new_pos[1] += 1
    elif key == pygame.K_LEFT:
        new_pos[0] -= 1
    elif key == pygame.K_RIGHT:
        new_pos[0] += 1

    # Check for wall collisions
    if 0 <= new_pos[0] < maze_columns and 0 <= new_pos[1] < maze_rows and maze[new_pos[1]][new_pos[0]] == 0:
        player_pos[:] = new_pos

def check_question():
    """Check if the player has encountered a question."""
    global current_question, score
    if player_pos == [maze_columns - 1, maze_rows - 1]:  # Example end position
        current_question = random.choice(questions)
        present_question(current_question)

def present_question(question):
    """Display a question and handle player input for the answer."""
    global score, baal_hint_active
    # TODO: Display the question and options on screen
    # Example: draw_text(question["text"], (100, 100))
    # Handle player input for options and check answer
    # Example: if player's answer == question["correct_option"]: score += 1

def draw_text(text, position):
    """Draw text on the screen."""
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, position)

def draw_score():
    """Draw the current score."""
    draw_text(f"Score: {score}", (10, 10))

# Generate the maze
generate_maze()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            move_player(event.key)

    # Game logic
    check_question()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the maze, player, and score
    draw_maze()
    draw_player()
    draw_score()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
