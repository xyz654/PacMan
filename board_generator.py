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
GREY = (211,211,211)


#glowne stale
FPS = 60
screen_width = 700
screen_height = 600

nX = 20 #4
nY = 25 #5

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
#graf poruszania sie pac-mana - reprezentacja macierzowa 
graf=np.zeros((nX*nY, nX*nY))

#lista budowy
buildTab = [False,  #rubber 
            False,  #wall
            False,  #floor
            False,  #big dot
            False,  #Pac-Man
            False   #tunnel
            ]  

counters = [0 for el in buildTab]

#wsp tunelu 
t1=np.zeros(2)
t2=np.zeros(2)


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

    #rysowanie legendy
    font = pygame.font.Font('freesansbold.ttf', 20)
    font1=pygame.font.Font('freesansbold.ttf', 10)
    text = font.render('Legend', True, BLACK, WHITE)
    wall=font1.render('to set wall press: W', True, BLACK, WHITE)
    pacman=font1.render('to set pacman press: P', True, BLACK, WHITE)
    rubber=font1.render('to get rubber press: X', True, BLACK, WHITE)
    floor=font1.render('to set floor press: Q', True, BLACK, WHITE)
    tunel=font1.render('to set tunel press: R', True, BLACK, WHITE)
    bigdot=font1.render('to set BigDot press: E', True, BLACK, WHITE)

    textRect = text.get_rect()
    textRect.center = (dx//2, dy)
    screen.blit(text, textRect)
    screen.blit(wall,(dx//8, 1.5*dy))
    screen.blit(pacman,(dx//8, 2*dy))
    screen.blit(rubber,(dx//8,2.5*dy))
    screen.blit(floor,(dx//8, 3*dy))
    screen.blit(tunel,(dx//8, 3.5*dy))
    screen.blit(bigdot,(dx//8, 4*dy))


    #dodawanie przycisku zapisz
    pygame.draw.rect(screen,GREY,((width+dx+20),height+dy-40,100,30),0,10)
    pygame.draw.rect(screen,BLACK,((width+dx+20),height+dy-40,100,30),1,10)

    save=font1.render('SAVE', True, BLACK, GREY)
    screen.blit(save,((width+dx+60), height+dy-30))

    i=(int)(mousePos[0]-width-dx-20)
    j=(int)(mousePos[1]-(height+dy-40))

    if mouse_is_pressed and i>0 and i<100 and j>0 and j<30:
        #zapisz
        print("zapisz")
        f = open("graf.txt",mode='w')
        for i in range(len(graf[0])):

            f.write(str(graf[i]))
            f.write("\n")
        f.close()


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

                #jesli chce postawic tunel to musi byc na brzegach ale nie w rogu!, jak nie to wychodze
                if ind==5 and i != 0 and i != nX-1 and j != 0 and j != nY-1: return

                 #jesli chce postawic tunel to nie moze byc w rogu!, jak nie to wychodze

                if ind==5 and ((i==0 and j==0) or (i==0 and j==nY-1) or (i==nX-1 and j==0) or (i==nX-1 and j==nY-1)): return

                #jesli nie ma podlogi a chce polozyc: duza kropke, pacmana, duszka, to wychodze
                if boardTab[i][j] != 2 and (ind==3 or ind==4): return    


                #jesli cos tam jest to zmniejszam counter czegos co nadpisuje
                if(int(boardTab[i][j]) != 0):
                    counters[int(boardTab[i][j])] -= 1

                if ind==0: #jesli jestem gumka trzeba sprawdzic co chce zmazac - czy tunel
                    if boardTab[i][j]==5:
                        if counters[5]==0: #byl tylko jeden
                            t1[0]=0
                            t1[1]=0
                        else: #byly dwa - trzeba sie dowiedziec ktory usuwam
                            if t1[0]==i and t1[1]==j: #chce usunac t1
                                #przepisuje dane do t1 i usuwam t2
                                t1[0]=t2[0]
                                t1[1]=t2[1]
                                t2[0]=0
                                t2[1]=0
                            else: #chce usunac t2
                                t2[0]=0
                                t2[1]=0
                            
                            #usuwam polaczenie miedzy tunelami, bo zostaje tylko jeden
                            graf[(int)(t1[1]*nX+t1[0])][(int)(t2[1]*nX+t2[0])]=0
                            graf[(int)(t2[1]*nX+t2[0])][(int)(t1[1]*nX+t1[0])]=0

                    if boardTab[i][j]==2: #chce zmazac podloge - trzeba usunac polaczenia w grafie
                        if boardTab[i-1][j]==2: #lewo
                            graf[j*nX+i][j*nX+i-1]=0
                            graf[j*nX+i-1][j*nX+i]=0
                        if boardTab[i+1][j]==2: #prawo
                            graf[j*nX+i][j*nX+i+1]=0
                            graf[j*nX+i+1][j*nX+i]=0
                        if boardTab[i][j-1]==2: #gora
                            graf[j*nX+i][(j-1)*nX+i]=0
                            graf[(j-1)*nX+i][j*nX+i]=0
                        if boardTab[i][j+1]==2: #dol
                            graf[j*nX+i][(j+1)*nX+i]=0
                            graf[(j+1)*nX+i][j*nX+i]=0
                    
                #jesli wszystko ok to wstawiam to co mam wstawic i zwiekszam licznik
                boardTab[i][j] = ind
                counters[ind] += 1
                if ind==5: #jesli to byl tunel, to zapisuje jego wsp
                    if t1[1]==0 and t1[0]==0:
                        t1[0]=i
                        t1[1]=j
                    else:
                        t2[0]=i
                        t2[1]=j

                

                if ind==2: #zbudowano podloge
                    #sprawdzam co jest naokolo (gora,dol,prawo,lewo) i jesli tez podloga to dodaje do macierzy
                    if boardTab[i-1][j]==2: #lewo
                        graf[j*nX+i][j*nX+i-1]=1
                        graf[j*nX+i-1][j*nX+i]=1
                    if boardTab[i+1][j]==2: #prawo
                        graf[j*nX+i][j*nX+i+1]=1
                        graf[j*nX+i+1][j*nX+i]=1
                    if boardTab[i][j-1]==2: #gora
                        graf[j*nX+i][(j-1)*nX+i]=1
                        graf[(j-1)*nX+i][j*nX+i]=1
                    if boardTab[i][j+1]==2: #dol
                        graf[j*nX+i][(j+1)*nX+i]=1
                        graf[(j+1)*nX+i][j*nX+i]=1

                if ind==5 and counters[5]==2: #zbudowano tunel i juz jakis jest na mapie
                   
                    graf[(int)(t1[1]*nX+t1[0])][(int)(t2[1]*nX+t2[0])]=1
                    graf[(int)(t2[1]*nX+t2[0])][(int)(t1[1]*nX+t1[0])]=1



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
