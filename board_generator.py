import pygame
import sys
import numpy as np


pygame.init()



# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE =(0,0, 255)
 

#glowne stale
FPS = 60
screen_width = 700
screen_height = 600

nX = 20
nY = 25

border = 20

#ogolne wymiary siatki w pixelach
width = border*nX
height = border*nY

#przesuniecia by siatka byla na srodku
dx = (screen_width-width)/2
dy = (screen_height-height)/2


#okno
screen = pygame.display.set_mode((screen_width, screen_height))
 
pygame.display.set_caption("Pac-Man board generator")

# zegar
clock = pygame.time.Clock()


#glowne zmienne
mousePos = pygame.mouse.get_pos()

boardTab=np.zeros((nX,nY))


#zmienne do budowy
buildWall=False





def draw_grid():

    #wypelnianie ekranu kolorem
    screen.fill(WHITE)

    #zaznaczanie kwadracika
    if(mousePos[0]>=dx and mousePos[1]>=dy and mousePos[0]<width+dx and mousePos[1]<height+dy):
        xk=(mousePos[0])-(mousePos[0]-dx)%border
        yk=(mousePos[1])-(mousePos[1]-dy)%border
        pygame.draw.rect(screen, GREEN, (xk, yk, border, border))

    #rysowanie siatki
    for x in range(nX+1):
        for y in range(nY+1):
            pygame.draw.line(screen, BLACK, (dx+x*border, dy), (dx+x*border, dy+height), 1)
            pygame.draw.line(screen, BLACK, (dx, dy+y*border), (dx+width, dy+y*border), 1)

    #rysowanie planszy
    for x in range(nX):
        for y in range(nY):
            if boardTab[x][y] == 1:
                pygame.draw.rect(screen,BLUE,(dx+x*border,dy+y*border,border,border))

def build():
    #pobieranie miejsca indeksu w tab myszki
    i=(int)(mousePos[0]-dx)//nX
    j=(int)(mousePos[1]-dy)//nY
    #buduje mur
    if buildWall:
        boardTab[i][j] = 1

#glowna petla
while True:

    #pobieranie pozycji myszki
    mousePos = pygame.mouse.get_pos()


    #rysowanie siatki
    draw_grid()
    #budowanie
    build()
 

    #przechwytywanie zdarzen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                buildWall = not buildWall
            
        


    #odswiezanie okna
    pygame.display.update()
    #kontroluje FPS
    clock.tick(FPS)
