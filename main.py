import pygame
import sys
import numpy as np

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW_LIGHT = (255, 255, 102)
YELLOW = (255, 255, 0)
GREY = (211,211,211)
ORANGE =(255,69,0)


class Game:
    def __init__(self):
        pygame.init()

        #glowne stale
        self.FPS = 60
        self.screen_width = 700
        self.screen_height = 600

        self.nX = 20 
        self.nY = 25 

        self.border = 20



        #oknoself.
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        pygame.display.set_caption("Pac-Man")

        # zegar
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.screen.fill(WHITE)

            #przechwytywanie zdarzen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #keydowny
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #LPM
                    if event.button == 1:
                        self.mouse_is_pressed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        pass
            
            #odswiezanie okna
            pygame.display.update()
            #kontroluje FPS
            self.clock.tick(self.FPS)




