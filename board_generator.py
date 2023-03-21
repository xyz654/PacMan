import pygame
import sys


pygame.init()





# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 

#glowne stale
FPS = 60
screen_width = 700
screen_height = 600

#okno
screen = pygame.display.set_mode((screen_width, screen_height))
 
pygame.display.set_caption("Pac-Man board generator")

# zegar
clock = pygame.time.Clock()


#glowna petla
while True:
    #wypelnianie ekranu kolorem
    screen.fill(WHITE)


    #jakies rysowanie
    pygame.draw.rect(screen, RED, (100, 100, 300, 400))
 

    #przechwytywanie zdarzen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print("Move the character forwards")
            elif event.key == pygame.K_s:
                print("Move the character backwards")
            elif event.key == pygame.K_a:
                print("Move the character left")
            elif event.key == pygame.K_d:
                print("Move the character right")
        


    #odswiezanie okna
    pygame.display.update()
    #kontroluje FPS
    clock.tick(FPS)
