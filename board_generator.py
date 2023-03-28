import pygame
import sys
import numpy as np


pygame.init()



# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW_LIGHT = (255, 255, 102)
YELLOW = (255, 255, 0)


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
mouse_is_pressed = False
boardTab=np.zeros((nX,nY))


#lista budowy
buildTab = [False,  #rubber 
            False,  #wall
            False,  #floor
            False,  #big dot
            False,  #Pac-Man
            False   #tunnel
            ]  

counters = [0 for el in buildTab]


#funkcja ustawiajaca wszytskie wskazniki budowy na False, poza jednym wskazanym w argumencie
def makeThemAllFalse(ind):
    for i in range(len(buildTab)):
        if i != ind:
            buildTab[i] = False


def draw_board():

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
            #wall
            if boardTab[x][y] == 1:
                pygame.draw.rect(screen,BLUE,(dx+x*border,dy+y*border,border,border))
            #floor
            if boardTab[x][y] == 2:
                pygame.draw.rect(screen, BLACK, (dx+x*border,dy+y*border,border,border))
                pygame.draw.circle(screen, YELLOW_LIGHT, (dx+x*border+border/2, dy+y*border+border/2), border/6)
            #big dot
            if boardTab[x][y] == 3:
                pygame.draw.rect(screen, BLACK, (dx+x*border,dy+y*border,border,border))
                pygame.draw.circle(screen, YELLOW_LIGHT, (dx+x*border+border/2, dy+y*border+border/2), border/4)
            #Pac-Man
            if boardTab[x][y] == 4:
                pygame.draw.rect(screen, BLACK, (dx+x*border,dy+y*border,border,border))
                pygame.draw.circle(screen, YELLOW, (dx+x*border+border/2, dy+y*border+border/2), border/3)
            #tunnel
            if boardTab[x][y] == 5:
                pygame.draw.rect(screen, BLACK, (dx+x*border,dy+y*border,border,border))
                pygame.draw.rect(screen, RED, (dx+x*border+border/4,dy+y*border+border/4,border/2,border/2))



def build():
    #pobieranie miejsca indeksu w tab myszki
    i=(int)(mousePos[0]-dx)//border
    j=(int)(mousePos[1]-dy)//border

    #jesli kursor jest poza polem, to wychodze z funkcji
    if i < 0 or j < 0 or i >= nX or j >= nY:
        return
    
    #buduje tylko jesli myszka jest wcisniete
    if mouse_is_pressed:
        #przechodze po wszystkich mozliwosciach bycia wcisnietym
        for ind in range(len(buildTab)):
            #jesli jest cos wcisniete to to buduje
            if buildTab[ind]:
                #jesli nie jestem gumka a dame pole to sciana to wychodze
                if boardTab[i][j] == 1 and ind != 0: return

                #jesli chce postawic pacmana albo tunel to sprawdzam czy jeszcze moge je wgl wstawic i jak nie to wychodze
                if (ind==4 and counters[4]>0) or (ind==5 and counters[5]>1): return

                #jesli chce postawic tunel to musi byc na brzegach, jak nie to wychodze
                if ind==5 and i != 0 and i != nX-1 and j != 0 and j != nY-1: return

                #jesli nie ma podlogi a chce polozyc: duza kropke, pacmana, duszka, to wychodze
                if boardTab[i][j] != 2 and (ind==3 or ind==4): return    


                #jesli cos tam jest to zmniejszam counter czegos co nadpisuje
                if(int(boardTab[i][j]) != 0):
                    counters[int(boardTab[i][j])] -= 1
                    
                #jesli wszystko ok to wstawiam to co mam wstawic i zwiekszam licznik
                boardTab[i][j] = ind
                counters[ind] += 1

                #wychodze z petli no bo raczej juz reszta jest False
                return



#glowna petla
while True:

    #pobieranie pozycji myszki
    mousePos = pygame.mouse.get_pos()

    #rysowanie 
    draw_board()

    #budowanie
    build()
 

    #przechwytywanie zdarzen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #keydowny
        if event.type == pygame.MOUSEBUTTONDOWN:
            #LPM
            if event.button == 1:
                mouse_is_pressed = True

        if event.type == pygame.KEYDOWN:
            #rubber
            if event.key == pygame.K_x:
                makeThemAllFalse(0)
                buildTab[0] = not buildTab[0]
            #wall
            if event.key == pygame.K_w:
                makeThemAllFalse(1)
                buildTab[1] = not buildTab[1]
            #floor
            if event.key == pygame.K_q:
                makeThemAllFalse(2)
                buildTab[2] = not buildTab[2]
            #big dot
            if event.key == pygame.K_e:
                makeThemAllFalse(3)
                buildTab[3] = not buildTab[3]
            #Pac-Man
            if event.key == pygame.K_p:
                makeThemAllFalse(4)
                buildTab[4] = not buildTab[4]
            #tunnel
            if event.key == pygame.K_r:
                makeThemAllFalse(5)
                buildTab[5] = not buildTab[5]
            
        

        #keyupy
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_is_pressed = False
        


    #odswiezanie okna
    pygame.display.update()
    #kontroluje FPS
    clock.tick(FPS)
