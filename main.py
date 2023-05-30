import pygame
import sys
import random
import time
import numpy as np
import os
from enums import Direction
from interactive import PacMan
from interactive import Clyde, Blinky, Inky, Pinky
import tkinter as tk



# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW_LIGHT = (255, 255, 102)
YELLOW = (255, 255, 0)
GREY = (211, 211, 211)
ORANGE = (255, 69, 0)
PINK = (255, 105, 180)





class Game:
    def __init__(self, path):
        pygame.init()

        self.path=path

        #glowne stale
        self.FPS = 60
        self.nX = 20 
        self.nY = 25 

        #dane dot okna i jego rozmiaru
        self.screen_width = 800
        self.screen_height = 700
        self.minWidth = 500
        self.minHeight = 700

        #okno
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Pac-Man")
        self.showTargets = False

        self.calculateScreen()

        #ogolne wymiary siatki w pixelach
        self.width = self.unit*self.nX
        self.height = self.unit*self.nY

        #przesuniecia by siatka byla na srodku
        self.dx = (self.screen_width-self.width)/2
        self.dy = (self.screen_height-self.height)/2

        #zmienne do przechowywania danych gry
        self.activeGame = True
        self.cherryExist = False
        self.cherryStartTime = time.time()

        #gracz
        self.playerMoveTime = 20
        self.startDinnerTime = None
        self.dinnerBonus = 200

        #duszki
        self.ghostRespawnArea = []

        #duszki ktore zabily 
        self.killers=[]

        #pobieram dane i je przypisuje do odpowiednich zmiennych
        self.boardTab = np.zeros((self.nX, self.nY))
        self.loadData(path)

        #tworze graf w postaci listy sasiedztwa
        self.tunels = []
        self.graph = None
        self.makeGraph()

        self.findPathForGhosts()

        #umiejscowanie duszkow
        self.ghosts = []
        self.placeGhosts()

        #laduje obrazki
        self.loadImages()
        
        #skaluje obrazki
        self.scaleImages()

        # zegar
        self.counter = 1
        self.clock = pygame.time.Clock()
        self.startTime = time.time()

        #pause
        self.pause=False

        #mysz
        self.mouse_is_pressed = False


    def makeGraph(self):
        self.respawnOutput = []
        self.tunels = []
        self.graph = [[[] for j in range(self.nY)] for i in range(self.nX)]
        for i in range(self.nX):
            for j in range(self.nY):
                #jezeli jest tam podloga po ktorej moge chodzic - to dodaje do grafu
                if self.boardTab[i][j] != 1 and self.boardTab[i][j] != 5 and self.boardTab[i][j] != 0:
                    #lewo
                    if self.boardTab[i-1][j] != 1 and self.boardTab[i-1][j] != 0:
                        self.graph[i][j].append((i-1,j))
                    #prawo
                    if self.boardTab[i+1][j] != 1 and self.boardTab[i+1][j] != 0: 
                        self.graph[i][j].append((i+1,j))
                    #gora
                    if self.boardTab[i][j-1] != 1 and self.boardTab[i][j-1] != 0:
                        self.graph[i][j].append((i,j-1))
                    #dol
                    if self.boardTab[i][j+1] != 1 and self.boardTab[i][j+1] != 0:
                        self.graph[i][j].append((i,j+1))
                #obsluga tuneli
                elif self.boardTab[i][j] == 5:
                    self.tunels.append((i, j))
                    if i == 0:
                        #prawo
                        if self.boardTab[i+1][j] != 1 and self.boardTab[i+1][j] != 0: 
                            self.graph[i][j].append((i+1,j))
                        #gora
                        if self.boardTab[i][j-1] != 1 and self.boardTab[i][j-1] != 0:
                            self.graph[i][j].append((i,j-1))
                        #dol
                        if self.boardTab[i][j+1] != 1 and self.boardTab[i][j+1] != 0:
                            self.graph[i][j].append((i,j+1))
                    elif i == self.nX-1:
                        #lewo
                        if self.boardTab[i-1][j] != 1 and self.boardTab[i-1][j] != 0:
                            self.graph[i][j].append((i-1,j))
                        #gora
                        if self.boardTab[i][j-1] != 1 and self.boardTab[i][j-1] != 0:
                            self.graph[i][j].append((i,j-1))
                        #dol
                        if self.boardTab[i][j+1] != 1 and self.boardTab[i][j+1] != 0:
                            self.graph[i][j].append((i,j+1))
                    elif j == 0:
                        #lewo
                        if self.boardTab[i-1][j] != 1 and self.boardTab[i-1][j] != 0:
                            self.graph[i][j].append((i-1,j))
                        #prawo
                        if self.boardTab[i+1][j] != 1 and self.boardTab[i+1][j] != 0: 
                            self.graph[i][j].append((i+1,j))
                        #dol
                        if self.boardTab[i][j+1] != 1 and self.boardTab[i][j+1] != 0:
                            self.graph[i][j].append((i,j+1))
                    elif j == self.nY-1:
                        #lewo
                        if self.boardTab[i-1][j] != 1 and self.boardTab[i-1][j] != 0:
                            self.graph[i][j].append((i-1,j))
                        #prawo
                        if self.boardTab[i+1][j] != 1 and self.boardTab[i+1][j] != 0: 
                            self.graph[i][j].append((i+1,j))
                        #gora
                        if self.boardTab[i][j-1] != 1 and self.boardTab[i][j-1] != 0:
                            self.graph[i][j].append((i,j-1))
                #obsluga respawnu duszkow
                elif self.boardTab[i][j] == 0:
                    #zagniezdzony if dodaje dana pozycje do listy wyjsc z respawnu
                    #lewo
                    if self.boardTab[i-1][j] != 1:
                        self.graph[i][j].append((i-1,j))
                        if self.boardTab[i-1][j] != 0:
                            self.respawnOutput.append((i-1, j))
                    #prawo
                    if self.boardTab[i+1][j] != 1: 
                        self.graph[i][j].append((i+1,j))
                        if self.boardTab[i+1][j] != 0:
                            self.respawnOutput.append((i+1, j))
                    #gora
                    if self.boardTab[i][j-1] != 1:
                        self.graph[i][j].append((i,j-1))
                        if self.boardTab[i][j-1] != 0:
                            self.respawnOutput.append((i, j-1))
                    #dol
                    if self.boardTab[i][j+1] != 1:
                        self.graph[i][j].append((i,j+1))
                        if self.boardTab[i][j+1] != 0:
                            self.respawnOutput.append((i, j+1))

    def findPathForGhosts(self):
        for startPosition in self.ghostRespawnArea:
            pass

    def loadData(self, path):
        self.dotScore = 0
        hp = 0
        if len(path)!=0:
            #pobieram dane z pliku
            with open(path, 'rb') as f:
                #zbieranie statystyk
                stats = np.load(f)
                self.difficulty = (int)(stats[0])
                self.cherryTime = (int)(stats[1])
                hp = (int)(stats[2])
                self.hpTab = [PacMan(1,1,1,1,1) for i in range(hp)]
                self.dinnerDuration = (int)(stats[4])
                self.tunelTime = stats[5]
                self.ghostsTunelTime = stats[6]

                #zbieranie planszy
                for i in range(self.nX):
                    for j in range(self.nY):
                        self.boardTab[i][j] = np.load(f)[0]
                        if self.boardTab[i][j] == 2:
                            self.dotScore += 10
                        if self.boardTab[i][j] == 3:
                            self.dotScore += 40
            #przeksztalcam dane do uzytecznej formy
            for i in range(self.nX):
                for j in range(self.nY):
                    #jesli trafie na cos interesujacego, to przypisuje to do opowiedniej zmiennej i zmieniam to na podloge
                    #respawn duszkow
                    if self.boardTab[i][j] == 6:
                        self.ghostRespawnArea.append((i,j))
                        self.boardTab[i][j] = 0
                    #Pac-Man
                    elif self.boardTab[i][j] == 4:
                        self.player = PacMan(i,j, self.playerMoveTime, self.tunelTime, hp)
                        self.pacX = i
                        self.pacY = j
                        self.boardTab[i][j] = 2
                        self.dotScore += 10
    
    def calculateScreen(self):
        #pobieram rozmiary okna
        self.screen_width, self.screen_height = self.screen.get_size()

        #wyznaczam nowa dlugosc jednostki        
        self.unit = min(self.screen_height/(8+self.nY), self.screen_width/(4+self.nX))

        #ustalam czcionke
        self.font = pygame.font.Font('freesansbold.ttf', int(1.5*self.unit))

        #ogolne wymiary siatki w pixelach
        self.width = self.unit*self.nX
        self.height = self.unit*self.nY

        #przesuniecia by siatka byla na srodku
        self.dx = (self.screen_width-self.width)/2
        self.dy = (self.screen_height-self.height)/2

    def loadImages(self):
        #obrazki pacmana i duszkow
        self.player.loadImages() 
        for ghost in self.ghosts:
            ghost.loadImages()

        #obrazki hp
        for pac in self.hpTab:
            pac.loadImages()
            pac.direction = Direction.EAST

        #wisienka 
        self.cherryImg = pygame.image.load('./graphics/pngFiles/bonusItems/cherries.png')

        #kropki
        self.dotImg = pygame.image.load('./graphics/pngFiles/bonusItems/dot.png')
        self.bigDotImg = pygame.image.load('./graphics/pngFiles/bonusItems/bigDot.png')

        #czworka
        self.nesw = pygame.image.load('./graphics/pngFiles/walls/czworka.png')

        #trojki
        self.nwe = pygame.image.load('./graphics/pngFiles/walls/trojka1.png')
        self.ens = pygame.image.load('./graphics/pngFiles/walls/trojka2.png')
        self.swe = pygame.image.load('./graphics/pngFiles/walls/trojka3.png')
        self.wns = pygame.image.load('./graphics/pngFiles/walls/trojka4.png')

        #proste - piony i poziomy
        self.ns = pygame.image.load('./graphics/pngFiles/walls/pion.png')
        self.we = pygame.image.load('./graphics/pngFiles/walls/poziom.png')

        #zakrety - narozniki
        self.ne = pygame.image.load('./graphics/pngFiles/walls/naroznik1.png')
        self.se = pygame.image.load('./graphics/pngFiles/walls/naroznik2.png')
        self.sw = pygame.image.load('./graphics/pngFiles/walls/naroznik3.png')
        self.nw = pygame.image.load('./graphics/pngFiles/walls/naroznik4.png')

        #koncowki
        self.endN = pygame.image.load('./graphics/pngFiles/walls/koncowka1.png')
        self.endE = pygame.image.load('./graphics/pngFiles/walls/koncowka2.png')
        self.endS = pygame.image.load('./graphics/pngFiles/walls/koncowka3.png')
        self.endW = pygame.image.load('./graphics/pngFiles/walls/koncowka4.png')

        #rondo
        self.roundabout = pygame.image.load('./graphics/pngFiles/walls/rondo.png')

    def scaleImages(self):
        #obrazki pacmana i duszkow
        self.player.scaleImages(self.unit) 
        for ghost in self.ghosts:
            ghost.scaleImages(self.unit)

        #obrazki hp
        for pac in self.hpTab:
            pac.scaleImages(self.unit*2)
            pac.direction = Direction.EAST

        #wisienka 
        self.cherryImg = pygame.transform.scale(self.cherryImg, (self.unit, self.unit))

        #kropki
        self.dotImg = pygame.transform.scale(self.dotImg, (self.unit, self.unit))
        self.bigDotImg = pygame.transform.scale(self.bigDotImg, (self.unit, self.unit))

        #czworka
        self.nesw = pygame.transform.scale(self.nesw, (self.unit, self.unit))

        #trojki
        self.nwe = pygame.transform.scale(self.nwe, (self.unit, self.unit))
        self.ens = pygame.transform.scale(self.ens, (self.unit, self.unit))
        self.swe = pygame.transform.scale(self.swe, (self.unit, self.unit))
        self.wns = pygame.transform.scale(self.wns, (self.unit, self.unit))

        #proste - piony i poziomy
        self.ns = pygame.transform.scale(self.ns, (self.unit, self.unit))
        self.we = pygame.transform.scale(self.we, (self.unit, self.unit))

        #zakrety - narozniki
        self.ne = pygame.transform.scale(self.ne, (self.unit, self.unit))
        self.se = pygame.transform.scale(self.se, (self.unit, self.unit))
        self.sw = pygame.transform.scale(self.sw, (self.unit, self.unit))
        self.nw = pygame.transform.scale(self.nw, (self.unit, self.unit))

        #koncowki
        self.endN = pygame.transform.scale(self.endN, (self.unit, self.unit))
        self.endE = pygame.transform.scale(self.endE, (self.unit, self.unit))
        self.endS = pygame.transform.scale(self.endS, (self.unit, self.unit))
        self.endW = pygame.transform.scale(self.endW, (self.unit, self.unit))

        #rondo
        self.roundabout = pygame.transform.scale(self.roundabout, (self.unit, self.unit))

    def drawWall(self, x, y):
        #lista zawierajaca kierunki rozbudowy muru
        directionsTab = [False, False, False, False]
        #polnoc
        if y > 0 and self.boardTab[x][y-1] == 1:
            directionsTab[0] = True
        #wschod
        if x < self.nX-1 and self.boardTab[x+1][y] == 1:
            directionsTab[1] = True
        #poludnie
        if y < self.nY-1 and self.boardTab[x][y+1] == 1:
            directionsTab[2] = True
        #zachod
        if x > 0 and self.boardTab[x-1][y] == 1:
            directionsTab[3] = True

        #czworka
        if False not in directionsTab:
            self.screen.blit(self.nesw, (self.dx+x*self.unit,self.dy+y*self.unit))
        #trojki
        elif directionsTab[3] and directionsTab[0] and directionsTab[1]:
            self.screen.blit(self.nwe, (self.dx+x*self.unit,self.dy+y*self.unit))
        elif directionsTab[0] and directionsTab[1] and directionsTab[2]:
            self.screen.blit(self.ens, (self.dx+x*self.unit,self.dy+y*self.unit))
        elif directionsTab[1] and directionsTab[2] and directionsTab[3]:
            self.screen.blit(self.swe, (self.dx+x*self.unit,self.dy+y*self.unit))
        elif directionsTab[2] and directionsTab[3] and directionsTab[0]:
            self.screen.blit(self.wns, (self.dx+x*self.unit,self.dy+y*self.unit))
        #pion
        elif directionsTab[0] and directionsTab[2]:
            self.screen.blit(self.ns, (self.dx+x*self.unit,self.dy+y*self.unit))
        #poziom
        elif directionsTab[1] and directionsTab[3]:
            self.screen.blit(self.we, (self.dx+x*self.unit,self.dy+y*self.unit))
        #narozniki
        elif directionsTab[0] and directionsTab[1]:
            self.screen.blit(self.ne, (self.dx+x*self.unit,self.dy+y*self.unit))
        elif directionsTab[1] and directionsTab[2]:
            self.screen.blit(self.se, (self.dx+x*self.unit,self.dy+y*self.unit))
        elif directionsTab[2] and directionsTab[3]:
            self.screen.blit(self.sw, (self.dx+x*self.unit,self.dy+y*self.unit))
        elif directionsTab[3] and directionsTab[0]:
            self.screen.blit(self.nw, (self.dx+x*self.unit,self.dy+y*self.unit))
        #koncowki
        elif directionsTab[2]:
            self.screen.blit(self.endN, (self.dx+x*self.unit,self.dy+y*self.unit))
        elif directionsTab[3]:
            self.screen.blit(self.endE, (self.dx+x*self.unit,self.dy+y*self.unit))
        elif directionsTab[0]:
            self.screen.blit(self.endS, (self.dx+x*self.unit,self.dy+y*self.unit))
        elif directionsTab[1]:
            self.screen.blit(self.endW, (self.dx+x*self.unit,self.dy+y*self.unit))
        #jak nie ma sasiadow to rondo
        else:
            self.screen.blit(self.roundabout, (self.dx+x*self.unit,self.dy+y*self.unit))
            
    def draw(self):
        #wypelnianie ekranu kolorem
        self.screen.fill(BLACK)

        #rysowanie planszy
        for x in range(self.nX):
            for y in range(self.nY):
                #floor without dot or tunnel or ghost respawn area
                if self.boardTab[x][y] == 0:
                    pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.unit,self.dy+y*self.unit,self.unit,self.unit))
                #wall
                if self.boardTab[x][y] == 1:
                    self.drawWall(x, y)
                #floor with dot
                if self.boardTab[x][y] == 2:
                    self.screen.blit(self.dotImg, (self.dx+x*self.unit,self.dy+y*self.unit))
                #big dot
                if self.boardTab[x][y] == 3:
                    self.screen.blit(self.bigDotImg, (self.dx+x*self.unit,self.dy+y*self.unit))
                #cherry
                if self.boardTab[x][y] == 6:
                    self.screen.blit(self.cherryImg, (self.dx+x*self.unit,self.dy+y*self.unit))
                
        
        #rysowanie duszkow
        #sprawdzam czy moge jesc duszki
        canBeEaten = False
        if self.startDinnerTime != None and time.time() - self.startDinnerTime < self.dinnerDuration:
            canBeEaten = True
        for ghost in self.ghosts:
            if not ghost.eaten:
                self.screen.blit(ghost.getImage(canBeEaten), (self.dx+ghost.xNormalized*self.unit, self.dy+ghost.yNormalized*self.unit))

        #rysowanie Pac-Mana
        self.screen.blit(self.player.getImage(), (self.dx+self.player.xNormalized*self.unit, self.dy+self.player.yNormalized*self.unit))


        #przeslony na tunele
        x, y = self.tunels[0]
        pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.unit,self.dy+y*self.unit,self.unit+1,self.unit+1))
        x, y = self.tunels[1]
        pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.unit,self.dy+y*self.unit,self.unit+1,self.unit+1))
        #przeslony pionowe (boki)
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.dx, self.screen_height))
        pygame.draw.rect(self.screen, BLACK, (self.dx+self.nX*self.unit, 0, self.dx, self.screen_height))
        #przeslony poziome (gora-dol)
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.screen_width, self.dy))
        pygame.draw.rect(self.screen, BLACK, (0, self.dy+self.nY*self.unit, self.screen_width, self.dy))

        #targety
        if self.showTargets and not canBeEaten:
            #nie rysuje targetow gdy moga byc jedzone, bo wtedy po prostu duszki poruszaja sie losowo
            for ghost in self.ghosts:
                pygame.draw.circle(self.screen, ghost.color, (self.dx+ghost.targetX*self.unit+self.unit/2, self.dy+ghost.targetY*self.unit+self.unit/2), self.unit/4)


        #INTERFEJS
        #hp
        hpSize = 2*self.unit
        dx = self.player.hp * hpSize / 2
        for i in range(self.player.hp):
            x = self.screen_width/2 - dx + i*hpSize
            y = self.screen_height - 2*hpSize
            self.screen.blit(self.hpTab[i].getImage(), (x,y))
        
        #score
        score = self.player.dotScore + self.player.otherScore
        scoreText = self.font.render("Score: "+str(score), True, YELLOW_LIGHT)
        textRect = scoreText.get_rect()
        textRect.center = (self.screen_width/2, self.unit*2)
        self.screen.blit(scoreText, textRect)


        #dodawanie przycisku pause
        pygame.draw.rect(self.screen,YELLOW,((self.screen_width-130),30,100,30),0,10)
        pygame.draw.rect(self.screen,BLACK,((self.screen_width-130),30,100,30),1,10)
        
        font1=pygame.font.Font('freesansbold.ttf', 20)

        save=font1.render('PAUSE', True, BLACK, YELLOW)
        self.screen.blit(save,((self.screen_width-110), 35))



    def checkWinOrDefeat(self):
        #przegrana
        if self.player.hp <= 0:
            self.activeGame = False

            #tworze okno
            root2 = tk.Tk()
            root2.configure(border=1, highlightbackground="yellow", highlightthickness=10, relief="sunken", background="black")

            #rozmiary
            window_width = 200
            window_height = 100

            root2.title("Game results")

            screen_width = root2.winfo_screenwidth()
            screen_height = root2.winfo_screenheight()

            centerX = int(screen_width/2 - window_width/2)
            centerY = int(screen_height/2 - window_height/2)

            root2.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')

            tk.Button(root2, text='You lost', command=root2.destroy, relief="flat", background="black", foreground="yellow").place(x=45, y=20)

        #wygrana
        if self.player.dotScore == self.dotScore:
            self.activeGame = False
            #tworze okno
            root2 = tk.Tk()
            root2.configure(border=1, highlightbackground="yellow", highlightthickness=10, relief="sunken", background="black")
            #rozmiary
            window_width = 200
            window_height = 100

            root2.title("End of game")

            screen_width = root2.winfo_screenwidth()
            screen_height = root2.winfo_screenheight()

            centerX = int(screen_width/2 - window_width/2)
            centerY = int(screen_height/2 - window_height/2)

            root2.geometry(f'{window_width}x{window_height}+{centerX}+{centerY}')

            tk.Button(root2, text='You win!', command=root2.destroy, relief="flat", background="black", foreground="yellow").place(x=45, y=20)

    def ghostsAI(self, ghost, canBeEaten):
        #zbieram dane o polozeniu duszka
        xp = ghost.x
        yp = ghost.y

        #sprawdzam czy nie jestem w tunelu
        if self.boardTab[xp][yp] == 5:
            return

        #szukam targetow i ew zmiany modow
        ghost.setTarget(self.player, self.ghosts, self.nX, self.nY)
        
        #jesli jestem w respawnie to musze z niego wyjsc, wiec zmieniam target
        if (xp, yp) in self.ghostRespawnArea:
            output = random.choice(self.respawnOutput)
            ghost.targetX = output[0]
            ghost.targetY = output[1]

        #tworze liste kierunkow w które moge sie ruszyc
        directions = []
        neighbours = self.graph[xp][yp]
        if (xp, yp-1) in neighbours and ghost.direction != Direction.SOUTH:
            directions.append(Direction.NORTH)
        if (xp, yp+1) in neighbours and ghost.direction != Direction.NORTH:
            directions.append(Direction.SOUTH)
        if (xp+1, yp) in neighbours and ghost.direction != Direction.WEST:
            directions.append(Direction.EAST)
        if (xp-1, yp) in neighbours and ghost.direction != Direction.EAST:
            directions.append(Direction.WEST)

        #jesli zbior kierunkow jest pusty to dodaje kierunek z ktorego przyszedlem
        if len(directions) == 0:
            if ghost.direction == Direction.NORTH:
                directions.append(Direction.SOUTH)
            elif ghost.direction == Direction.EAST:
                directions.append(Direction.WEST)
            elif ghost.direction == Direction.SOUTH:
                directions.append(Direction.NORTH)
            elif ghost.direction == Direction.WEST:
                directions.append(Direction.EAST)


        #gdy moga byc zjedzone
        if canBeEaten:
            #losuje kierunek na dalszy ruch
            ghost.direction = random.choice(directions)

        #gdy to one moga zabic
        else:
            #szukam kierunku, ktory da mi najmniejsza odlegosc od targetu
            minD = float('inf')
            bestDirection = None
            for direction in directions:
                dx, dy = 0, 0
                if direction == Direction.NORTH:
                    dx = ghost.x - ghost.targetX
                    dy = ghost.y-1 - ghost.targetY
                elif direction == Direction.EAST:
                    dx = ghost.x+1 - ghost.targetX
                    dy = ghost.y - ghost.targetY
                elif direction == Direction.SOUTH:
                    dx = ghost.x - ghost.targetX
                    dy = ghost.y+1 - ghost.targetY
                elif direction == Direction.WEST:
                    dx = ghost.x-1 - ghost.targetX
                    dy = ghost.y - ghost.targetY
                #jesli ten kierunek jest lepszy od poprzednich to to zapisuje
                d = dx*dx + dy*dy
                if d < minD:
                    minD = d
                    bestDirection = direction

            #ustawiam kierunek na najlepszy z mozliwych
            ghost.direction = bestDirection

    def moveAll(self):
        #POZWOLENIE NA JEDZENIE I EWENTUALNE SPOWALNIANIE DUSZKOW
        canBeEaten = False
        slowDelta = 2 #powinno byc calkowite, jak nie jest to nie ma plynnosci
        ghostMoveTime = self.playerMoveTime
        if self.startDinnerTime != None and time.time() - self.startDinnerTime < self.dinnerDuration:
            canBeEaten = True
            #spowalniam
            ghostMoveTime *= slowDelta
        elif self.startDinnerTime != None:
            #czekam na duchy zeby przejscie bylo plynne
            ghostMoveTime *= slowDelta
            if self.counter % ghostMoveTime < 2:
                ghostMoveTime /= slowDelta
                self.counter = 0
                self.startDinnerTime = None
                #respawnuje wszystkie zjedzone w tym czasie duszki
                self.placeGhosts()
        else:
            self.startDinnerTime = None

        #ZDERZENIA 
        for ghost in self.ghosts:
            dx = abs(self.player.xNormalized - ghost.xNormalized)
            dy = abs(self.player.yNormalized - ghost.yNormalized)
            #ta 0.3 to margines bledu, ktory sb sam wymyslilem, dla ktorego to w miare dzialalo
            if not ghost.eaten and dx < 0.3 and dy < 0.3:
                if canBeEaten:
                    ghost.eaten = True
                    self.player.otherScore += self.dinnerBonus
                    self.dinnerBonus *= 2
                else:
                    self.player.hp -= 1
                    self.killers.append(ghost.type)
                    self.player.backToPosition(self.pacX, self.pacY)
        

        #ZMIANY KIERUNKU RUCHU
        turnBack = False
        #Pac-Man
        if self.counter % self.playerMoveTime == 0:
            #potwierdzam poprzednia zmiane pozycji
            self.player.confirmPosition(self.tunels, self.nX, self.nY)

            #pobieram dane do zmiennych lokalnych by latwiej sie ich uzywalo
            xp = self.player.x
            yp = self.player.y

            #zjadam to co mam na drodze
            #male kropki
            if self.boardTab[xp][yp] == 2:
                self.player.dotScore += 10
                self.boardTab[xp][yp] = 0
            #duze kropki
            if self.boardTab[xp][yp] == 3:
                self.player.dotScore += 40
                self.boardTab[xp][yp] = 0
                #jak zjem duza kropke to moge zjadac duszki
                if self.startDinnerTime == None:
                    self.counter = 0
                self.startDinnerTime = time.time()
                self.dinnerBonus = 200
                #obrot duszkow o 180 (tylko jezeli przed zjedzeniem nie byly zdatne do spozycia)
                turnBack = True
            #wisienki
            if self.boardTab[xp][yp] == 6:
                self.player.otherScore += 100
                self.boardTab[xp][yp] = 0
                self.cherryExist = False
                self.cherryStartTime = time.time()

            
            #pobieram sasiadow aktualnego pola na ktorym jest pac-man
            neighbours = self.graph[xp][yp]

            #zmiana kierunku
            if self.player.nextDirection == Direction.NORTH and (xp, yp-1) in neighbours:
                self.player.direction = self.player.nextDirection
            elif self.player.nextDirection == Direction.SOUTH and (xp, yp+1) in neighbours:
                self.player.direction = self.player.nextDirection
            elif self.player.nextDirection == Direction.EAST and (xp+1, yp) in neighbours:
                self.player.direction = self.player.nextDirection
            elif self.player.nextDirection == Direction.WEST and (xp-1, yp) in neighbours:
                self.player.direction = self.player.nextDirection
            #jesli nie ma podanego nowego kierunku to sprawdzam czy nadal moge isc tam gdzie ide
            elif self.player.direction == Direction.NORTH and (xp, yp-1) not in neighbours:
                #sprawdzam czy jestem czy nie w tunelu
                if yp != 0:
                    self.player.direction = None
            elif self.player.direction == Direction.SOUTH and (xp, yp+1) not in neighbours:
                #sprawdzam czy jestem czy nie w tunelu
                if yp != self.nY-1:
                    self.player.direction = None
            elif self.player.direction == Direction.EAST and (xp+1, yp) not in neighbours:
                #sprawdzam czy jestem czy nie w tunelu
                if xp != self.nX-1:
                    self.player.direction = None
            elif self.player.direction == Direction.WEST and (xp-1, yp) not in neighbours:
                #sprawdzam czy jestem czy nie w tunelu
                if xp != 0:
                    self.player.direction = None

            #sprawdzam koniec gry
            self.checkWinOrDefeat()

            #tworze ew wisienki
            self.cherryService()


        #Duszki
        if self.counter % ghostMoveTime == 0:
            for ghost in self.ghosts:
                #potwierdzam poprzednia zmiane pozycji
                ghost.confirmPosition(self.tunels, self.nX, self.nY)
                #ewentualny obrot
                if turnBack:
                    if ghost.direction == Direction.NORTH:
                        ghost.direction = Direction.SOUTH
                    elif ghost.direction == Direction.EAST:
                        ghost.direction = Direction.WEST
                    elif ghost.direction == Direction.SOUTH:
                        ghost.direction = Direction.NORTH
                    elif ghost.direction == Direction.WEST:
                        ghost.direction = Direction.EAST
                #ustawiam kazdemu duszkowi kolejny kierunek
                self.ghostsAI(ghost, canBeEaten)

        
        
                

            
        #RUCH
        #Pac-Man
        self.player.move()
        #Duszki
        for ghost in self.ghosts:
            ghost.move(ghostMoveTime)

    def cherryService(self):
        #tworze wisienke tylko jesli jeszcze jej nie ma i gracz zjadl juz co najmniej 1/4 wszytskich kropek
        if not self.cherryExist and self.player.dotScore > self.dotScore/4:
            if time.time() - self.cherryStartTime >= self.cherryTime:
                while True:
                    x = random.randint(1,self.nX-2)
                    y = random.randint(1,self.nY-2)
                    if self.boardTab[x][y] == 0 and (x,y) not in self.ghostRespawnArea:
                        self.boardTab[x][y] = 6
                        self.cherryExist = True
                        break

    def placeGhosts(self):
        #jesli nie ma jeszcze duszkow
        if len(self.ghosts) == 0:
            pos = random.choice(self.ghostRespawnArea)
            self.ghosts.append(Clyde(pos[0], pos[1], self.playerMoveTime, self.ghostsTunelTime))

            pos = random.choice(self.ghostRespawnArea)
            self.ghosts.append(Inky(pos[0], pos[1], self.playerMoveTime, self.ghostsTunelTime))

            pos = random.choice(self.ghostRespawnArea)
            self.ghosts.append(Blinky(pos[0], pos[1], self.playerMoveTime, self.ghostsTunelTime))

            pos = random.choice(self.ghostRespawnArea)
            self.ghosts.append(Pinky(pos[0], pos[1], self.playerMoveTime, self.ghostsTunelTime))
        #jesli sa duszki to po prostu ozywiam te ktore sa zjedzone
        else:
            for ghost in self.ghosts:
                if ghost.eaten:
                    pos = random.choice(self.ghostRespawnArea)
                    ghost.respawn(pos[0], pos[1])
        

    def run(self):
        while self.activeGame:
            #ruszanie
            self.moveAll()

            #rysowanie
            self.draw()

            #odswiezanie okna
            pygame.display.update()

            #obsluga licznika
            self.counter += 1
            if self.counter >= 1000:
                self.counter = 0

            #kontroluje FPS
            self.clock.tick(self.FPS)


            #przechwytywanie zdarzen
            for event in pygame.event.get():
                #zamykanie okna
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # sys.exit()
                    self.activeGame = False
                    

                #zmiana rozmiaru okna - koniecznosc przeliczenia niektorych zmiennych
                elif event.type == pygame.WINDOWEXPOSED:
                    self.calculateScreen()
                    #skaluje obrazki
                    self.scaleImages()

                #keydowny
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #LPM
                    if event.button == 1:
                        self.mouse_is_pressed = True
                #keyupy
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_is_pressed = False

                if event.type == pygame.KEYDOWN:
                    #sterowanie Pac-Manem
                    if event.key == pygame.K_w:
                        self.player.nextDirection = Direction.NORTH
                    if event.key == pygame.K_d:
                        self.player.nextDirection = Direction.EAST
                    if event.key == pygame.K_s:
                        self.player.nextDirection = Direction.SOUTH
                    if event.key == pygame.K_a:
                        self.player.nextDirection = Direction.WEST
                    #targety
                    if event.key == pygame.K_t:
                        self.showTargets = not self.showTargets

                #przyciski
                self.mousePos = pygame.mouse.get_pos()
                x=(int)(self.mousePos[0]-(self.screen_width-130))
                y=(int)(self.mousePos[1]-30)
                
                if self.mouse_is_pressed and x>0 and x<100 and y>0 and y<30:
                    self.pause= not self.pause

            while self.pause:
                self.mouse_is_pressed=False
                #przyciski
                self.mousePos = pygame.mouse.get_pos()
                x=(int)(self.mousePos[0]-(self.screen_width-130))
                y=(int)(self.mousePos[1]-30)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                    #LPM
                        if event.button == 1:
                            self.mouse_is_pressed = True
                if self.mouse_is_pressed and x>0 and x<100 and y>0 and y<30:
                    self.pause= not self.pause


        self.endTime = time.time()
            
            
        #statystyki
        stats = np.array([])
        # with open("./mapStats.npy", 'wb') as f:
        #     np.save(f, stats)
        numGames=0
        with open("./mapStats.npy", 'rb') as f:
            #zbieranie statystyk
            stats = np.load(f)
            newStats = []
            for stat in stats:
                newStats.append(list(stat))
            stats = newStats
        with open("./mapStats.npy", 'wb') as f:
            #zbieram nazwe aktualnej planszy
            currMapName = os.path.basename(self.path)
            #jezeli juz gralem na tej mapie to inkrementuje licznik
            exist = False
            for stat in stats:
                numGames+=int(stat[1])
                if stat[0] == currMapName:
                    stat[1] = int(stat[1])+1
                    exist = True
                    break
            #jesli nie to dodaje mape do listy
            if not exist:
                stats.append([currMapName, 1])
            
            stats = np.array(stats)
            
            #zapis 
            np.save(f, stats)
            f.close()


        #statystyki ogolne - czas gry itp

        generalStats=np.array([])
        # with open("./generalStats.npy", 'wb') as f:
        #     np.save(f, generalStats)


        with open("./generalStats.npy", 'rb') as f:
        #zbieranie statystyk
            generalStats = np.load(f)
            newGeneralStats = list(generalStats)
            generalStats = newGeneralStats
            

        with open("./generalStats.npy", 'wb') as f:

            if(len(generalStats)==0):
                generalStats.append((self.endTime-self.startTime))
                generalStats.append(1)
                generalStats.append(self.player.dotScore)
                generalStats.append(0)
                generalStats.append(0)
                generalStats.append(0)
                generalStats.append(0)
                for name in self.killers:
                    if name == "Clyde":
                        generalStats[3]=int(generalStats[3])+1
                    if name == "Blinky":
                        generalStats[4]=int(generalStats[4])+1
                    if name == "Inky":
                        generalStats[5]=int(generalStats[5])+1
                    if name == "Pinky":
                        generalStats[6]=int(generalStats[6])+1

            else:
            #zwiekszam czas gry 
                generalStats[0]+=(self.endTime-self.startTime)
                generalStats[2]=(generalStats[2]*int(generalStats[1])+self.player.dotScore)/(int(generalStats[1])+1)
                generalStats[1]=int(generalStats[1])+1
                for name in self.killers:
                    if name == "Clyde":
                        generalStats[3]=int(generalStats[3])+1
                    if name == "Blinky":
                        generalStats[4]=int(generalStats[4])+1
                    if name == "Inky":
                        generalStats[5]=int(generalStats[5])+1
                    if name == "Pinky":
                        generalStats[6]=int(generalStats[6])+1

            generalStats = np.array(generalStats)
            
            #zapis 
            np.save(f, generalStats)
            f.close()

        
        #wyjscie z okna
        pygame.quit()
            

            
            
            

# game = Game("./maps/correct.npy")
# game.run()
