# Import the pygame library and initialise the game engine
import pygame
from sceneswitch import Sceneswitch

pygame.init()

sceneSwitcher = Sceneswitch()


# -------- Main Program (Homescreen is playing) Loop -----------

sceneSwitcher.switchscenes()

# -------- Main Program (Game is playing) Loop -----------


# Once we have exited the main program loop we can stop the game engine:
pygame.quit()