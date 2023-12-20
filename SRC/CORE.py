from datetime import datetime
from gradio_client import Client
from PIL import Image

import pygame
import sys
import textwrap
import threading

# Initialize Pygame and Gradio Clients
pygame.init()



# FastAPI https://f6435fb8424218dbd3.gradio.live/docs
image_client = Client("https://f6435fb8424218dbd3.gradio.live/")
# image_client = Client("https://linaqruf-animagine-xl.hf.space/")

# Gradio https://ab92da00650e4b920d.gradio.live/docs
chat_client = Client("https://ink-concert-snapshot-engage.trycloudflare.com/")
# chat_client = Client("https://osanseviero-mistral-super-fast.hf.space/")

button_states = {
    'F1': False,
    'F2': False,
    'F3': True,
    'O': False
}

# Pygame Window Configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
BG_COLOR = (30, 30, 30)
FONT = pygame.font.Font('font.ttf', 36)
FONT_COLOR = (255, 255, 255)
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Global variable for background
background = None
background_lock = threading.Lock()  # Lock for thread-safe access to background
background_ready = False  # Flag to indicate when the background is ready
background_thread = None


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {message}")


# Function to render wrapped text and calculate the total required height
def get_wrapped_text_height(text, font, max_width):
    lines = textwrap.wrap(text, width=max_width)
    text_height = 0
    for line in lines:
        text_surface = font.render(line, True, FONT_COLOR)
        text_height += text_surface.get_height() + 2  # 2 pixels for line spacing
    return text_height


# Function to draw semi-transparent background
def draw_transparent_background(surface, rect, color, alpha):
    chat_bg = pygame.Surface(rect.size, pygame.SRCALPHA)  # Use SRCALPHA to allow alpha blending
    chat_bg.fill((*color, alpha))  # Include alpha in the color tuple
    surface.blit(chat_bg, rect.topleft)  # Position it at the top-left of the rect


def generate_image(prompt):
    global background, background_ready
    # log(f"Starting image generation with prompt: {prompt} ")
    log("Sending image prompt to remote API...")
    file_path = image_client.predict(
        prompt, "Ugly, Blurry, Hazy, Low Quality",
        prompt, "Unrealistic, Underage, 2Girls",
        True, 1000000,
        1344, 768,
        1344, 768,
        1344, 768,
        10, 40,
        False, 0,
        False, False,
        api_name="/run"
    )
    # Set background_ready to False right after the API call
    background_ready = False
    log(f"API response received: {file_path}")
    try:
        with background_lock:
            image = Image.open(file_path)
            background = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
            background_ready = True
            log("Background image successfully loaded and updated.")
    except Exception as e:
        log(f"Failed to load image from path. Error: {e}")


def start_background_image_generation(prompt):
    global background_thread, background_ready
    if background_thread is not None and background_thread.is_alive():
        log("Waiting for existing background thread to finish.")
        background_thread.join()

    background_ready = False
    background_thread = threading.Thread(target=generate_image, args=(prompt,))
    background_thread.start()
    log("Started new background image generation thread.")


def chat(message):
    log("Sending text to remote API...")
    result = chat_client.predict(
        message,
        0.9,
        256,
        0.9,
        1.2,
        api_name="/chat"
    )
    log(f"API response received: {result}")
    return result


def draw_text(surface, text, position):
    text_surface = FONT.render(text, True, FONT_COLOR)
    surface.blit(text_surface, position)


def create_button(surface, keyword, rect, color, hover_color, text_color):
    global button_states, last_click_time
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    current_time = pygame.time.get_ticks()
    if rect.collidepoint(mouse):
        pygame.draw.rect(surface, hover_color, rect)  # Button hover effect
        if click[0] == 1 and current_time - last_click_time > 500:  # 500 milliseconds debounce
            log(f"Button '{keyword}' clicked")
            last_click_time = current_time
            button_states[keyword] = not button_states[keyword]
            perform_button_action(keyword)  # Perform specific action for the button
    else:
        button_color = hover_color if button_states[keyword] else color
        pygame.draw.rect(surface, button_color, rect)

    text_surf = FONT.render(keyword, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def toggle_command():
    global prompt
    was_updated = False

    if button_states['O'] and "(1girl:1.0), " not in prompt:
        prompt = "(1girl:1.0), " + prompt
        was_updated = True
    elif not button_states['O'] and "(1girl:1.0), " in prompt:
        prompt = prompt.replace("(1girl:1.0), ", "")
        was_updated = True

    if was_updated:
        log(f"Prompt updated to: {prompt}")
        start_background_image_generation(prompt)


# Define individual toggle functions for Function Keys
def toggle_F1():
    global prompt, button_state
    was_updated = False

    # Implement specific action for button F1
    if button_states['F1'] and "(Anime Style:1.0), " not in prompt:
        prompt = "(Anime Style:1.0), " + prompt
        was_updated = True
    elif not button_states['F1'] and "(Anime Style:1.0), " in prompt:
        prompt = prompt.replace("(Anime Style:1.0), ", "")
        was_updated = True

    if was_updated:
        log(f"Prompt updated to: {prompt}")
        start_background_image_generation(prompt)


def toggle_F2():
    global prompt, button_state
    was_updated = False

    # Implement specific action for button F2
    if button_states['F2'] and "(Intense Eye Contact:1.0), " not in prompt:
        prompt = "(Intense Eye Contact:1.0), " + prompt
        was_updated = True
    elif not button_states['F2'] and "(Intense Eye Contact:1.0), " in prompt:
        prompt = prompt.replace("(Intense Eye Contact:1.0), ", "")
        was_updated = True

    if was_updated:
        log(f"Prompt updated to: {prompt}")
        start_background_image_generation(prompt)


def toggle_F3():
    global prompt, button_state
    was_updated = False

    # Implement specific action for button F3 (NSFW) APPEND
    if button_states['F3'] and ", (Professional Lighting:1.0)" not in prompt:
        prompt += ", (Professional Lighting:1.0)"
        was_updated = True
    elif not button_states['F3'] and ", (Professional Lighting:1.0)" in prompt:
        prompt = prompt.replace(", (Professional Lighting:1.0)", "")
        was_updated = True

    if was_updated:
        log(f"Prompt updated to: {prompt}")
        start_background_image_generation(prompt)


def perform_button_action(keyword):
    if keyword == 'O':
        return toggle_command()
    elif keyword == 'F1':
        return toggle_F1()
    elif keyword == 'F2':
        return toggle_F2()
    elif keyword == 'F3':
        return toggle_F3()


def update_and_generate():
    global background_thread, background_ready
    if not background_ready and (background_thread is None or not background_thread.is_alive()):
        log(f"Starting new background generation with prompt: {prompt}")
        background_thread = threading.Thread(target=generate_image, args=(prompt,))
        background_thread.start()


# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CORE")
log("Game window initialized.")

# Initial prompt setup
prompt = "(Lobby:1.0), (Waiting Area:1.0), (Professional Lighting:1.0)"

# Input box and chat history
input_box = pygame.Rect(100, 650, 140, 32)
chat_history = []
user_input = ''
clock = pygame.time.Clock()

# O-Key configuration
button_color = (0, 255, 0)  # Green
hover_color = (255, 0, 0)  # Red
button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40, 100, 30)  # Button position and size

button_state = False  # False when green (normal), True when cyan (1girl added)
last_click_time = 0

# F-Key configurations
f3_color = (30, 30, 30)  # Grey
f3_rect = pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 40, 100, 30)  # Button position and size

f2_color = (30, 30, 30)  # Grey
f2_rect = pygame.Rect(SCREEN_WIDTH - 450, SCREEN_HEIGHT - 40, 100, 30)  # Button position and size

f1_color = (30, 30, 30)  # Grey
f1_rect = pygame.Rect(SCREEN_WIDTH - 600, SCREEN_HEIGHT - 40, 100, 30)  # Button position and size

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            log("Quit event detected. Exiting game loop.")
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                log("Enter key pressed. Sending chat message.")
                response = chat(user_input)
                chat_history.append("You: " + user_input)
                chat_history.append("Mistral: " + str(response))
                user_input = ''
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_F1:
                toggle_F1()
            elif event.key == pygame.K_F2:
                toggle_F2()
            elif event.key == pygame.K_F3:
                toggle_F3()
            elif event.key == pygame.K_F4:
                toggle_command()  # Assuming 'O' is assigned to F4
            else:
                user_input += event.unicode

    screen.fill(BG_COLOR)
    with background_lock:
        if background is not None:
            screen.blit(background, (-32, -24))

    # Initialize variables for chat log rendering
    chat_y_start = 50
    line_counter = 0
    max_lines = 11  # Maximum number of lines in the chat log

    # Calculate the required height for the chat log
    chat_lines = []
    for message in reversed(chat_history[-5:]):  # Start with the most recent messages
        message = message.replace("</s>", "")  # Sanitize the message
        lines = textwrap.wrap(message, width=75)
        for line in reversed(lines):
            if line_counter < max_lines:
                chat_lines.insert(0, line)  # Insert lines at the beginning to maintain order
                line_counter += 1
            else:
                break  # Stop if we reach the maximum number of lines
        if line_counter >= max_lines:
            break  # Stop if we reach the maximum number of lines

    total_required_height = line_counter * (FONT.get_linesize() + 2)

    # Draw the semi-transparent background for the chat log
    chat_bg_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, total_required_height)
    draw_transparent_background(screen, chat_bg_rect, (0, 0, 0), 128)

    # Render the chat text on top of the background
    for line in chat_lines:
        draw_text(screen, line, (60, chat_y_start))
        chat_y_start += FONT.get_linesize() + 2  # Move to the next line position

    # Input box background
    input_bg_height = FONT.get_linesize() + 10  # Add some padding
    input_bg_rect = pygame.Rect(50, SCREEN_HEIGHT - input_bg_height - 50, SCREEN_WIDTH - 100, input_bg_height)
    draw_transparent_background(screen, input_bg_rect, (0, 0, 0), 128)

    # Draw input text
    input_text_rect = pygame.Rect(60, SCREEN_HEIGHT - input_bg_height - 40, SCREEN_WIDTH - 120, input_bg_height)
    draw_text(screen, user_input, input_text_rect.topleft)

    # Draw and handle the button
    create_button(screen, "O", button_rect, button_color, hover_color, FONT_COLOR)
    create_button(screen, "F1", f1_rect, f1_color, hover_color, FONT_COLOR)
    create_button(screen, "F2", f2_rect, f2_color, hover_color, FONT_COLOR)
    create_button(screen, "F3", f3_rect, f3_color, hover_color, FONT_COLOR)

    # Regenerate the background if necessary
    update_and_generate()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
log("Connection closed. Exiting application.")
sys.exit()
