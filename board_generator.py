import pygame


pygame.init()





# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 

#glowne stale
FPS = 60
screen_width = 1000
screen_height = 700

#okno
screen = pygame.display.set_mode((screen_width, screen_height))
 
pygame.display.set_caption("Pac-Man board generator")

# zegar
clock = pygame.time.Clock()



while True:
    #wypelnianie ekranu kolorem
    screen.fill(WHITE)


    #jakies rysowanie
    pygame.draw.rect(screen, RED, (100, 200, 300, 400))
 

    #odswiezanie okna
    pygame.display.update()
    #kontroluje FPS
    clock.tick(FPS)
