# THE 12 DAEMONS OF XMAS
import pygame
import sys
import os

# Add the SRC directory to the system path
src_dir = os.path.join(os.path.dirname(__file__), 'SRC')
sys.path.append(src_dir)

import INTRO
import CORE

# Now you can import the level modules
import LVL-01
import LVL-02
import LVL-03
import LVL-04

# Import other levels as needed
import OUTRO
import DEBUG

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    
    levels = [INTRO, CORE, LVL-01, CORE, LVL-02, CORE, LVL-03, CORE, LVL-04, OUTRO, DEBUG]  # List of levels
    current_level = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if current_level < len(levels):
            level_complete = levels[current_level].run_level(screen)
            if level_complete:
                current_level += 1
        else:
            # All levels complete, or show end game screen
            break

        pygame.display.flip()

if __name__ == '__main__':
    main()
