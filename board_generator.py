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

nX = 20
nY = 25


#glowne zmienne
mousePos = pygame.mouse.get_pos()

#okno
screen = pygame.display.set_mode((screen_width, screen_height))
 
pygame.display.set_caption("Pac-Man board generator")

# zegar
clock = pygame.time.Clock()


def draw_grid(border):

    #wypelnianie ekranu kolorem
    screen.fill(WHITE)

    #ogolne wymiary siatki w pixelach
    width = border*nX
    height = border*nY

    #przesuniecia by siatka byla na srodku
    dx = (screen_width-width)/2
    dy = (screen_height-height)/2

    #rysowanie siatki
    for x in range(nX+1):
        for y in range(nY+1):
            pygame.draw.line(screen, BLACK, (dx+x*border, dy), (dx+x*border, dy+height), 1)
            pygame.draw.line(screen, BLACK, (dx, dy+y*border), (dx+width, dy+y*border), 1)





#glowna petla
while True:
    
    #pobieranie pozycji myszki
    mousePos = pygame.mouse.get_pos()


    #rysowanie siatki
    draw_grid(15)
 

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
