import pygame
import sys
import random
import time
import numpy as np
from enums import Direction
from interactive import PacMan
from interactive import Clyde, Blinky, Inky, Pinky

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



class Game:
    def __init__(self, path):
        pygame.init()

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
        self.ghostRespawnArea = []

        #gracz
        self.playerMoveTime = 20
        self.startDinnerTime = None
        self.dinnerBonus = 200

        #pobieram dane i je przypisuje do odpowiednich zmiennych
        self.boardTab = np.zeros((self.nX, self.nY))
        self.loadData(path)

        #umiejscowanie duszkow
        self.placeGhosts()

        #laduje obrazki
        self.loadImages()
        
        #tworze graf w postaci listy sasiedztwa
        self.tunels = []
        self.graph = None
        self.makeGraph()

        # zegar
        self.counter = 1
        self.clock = pygame.time.Clock()

    def makeGraph(self):
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

    def loadData(self, path):
        self.dotScore = 0
        hp = 0
        if len(path)!=0:
            #pobieram dane z pliku
            with open(path, 'rb') as f:
                #zbieranie statystyk
                stats = np.load(f)
                self.difficulty = stats[0]
                self.cherryTime = stats[1]
                hp = stats[2]
                self.hpTab = [PacMan(1,1,1,1,1) for i in range(hp)]
                self.dinnerDuration = stats[4]
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
                        self.player = PacMan(i,j, self.playerMoveTime, 0.5, hp)
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
        self.player.loadImages(self.unit) 
        for ghost in self.ghosts:
            ghost.loadImages(self.unit)

        #obrazki hp
        for pac in self.hpTab:
            pac.loadImages(self.unit*2)
            pac.direction = Direction.EAST

        #wisienka 
        self.cherryImg = pygame.image.load('./graphics/pngFiles/bonusItems/cherries.png')
        self.cherryImg = pygame.transform.scale(self.cherryImg, (self.unit, self.unit))

        #kropki
        self.dotImg = pygame.image.load('./graphics/pngFiles/bonusItems/dot.png')
        self.dotImg = pygame.transform.scale(self.dotImg, (self.unit, self.unit))

        self.bigDotImg = pygame.image.load('./graphics/pngFiles/bonusItems/bigDot.png')
        self.bigDotImg = pygame.transform.scale(self.bigDotImg, (self.unit, self.unit))

        #czworka
        self.nesw = pygame.image.load('./graphics/pngFiles/walls/czworka.png')
        self.nesw = pygame.transform.scale(self.nesw, (self.unit, self.unit))

        #trojki
        self.nwe = pygame.image.load('./graphics/pngFiles/walls/trojka1.png')
        self.nwe = pygame.transform.scale(self.nwe, (self.unit, self.unit))

        self.ens = pygame.image.load('./graphics/pngFiles/walls/trojka2.png')
        self.ens = pygame.transform.scale(self.ens, (self.unit, self.unit))

        self.swe = pygame.image.load('./graphics/pngFiles/walls/trojka3.png')
        self.swe = pygame.transform.scale(self.swe, (self.unit, self.unit))

        self.wns = pygame.image.load('./graphics/pngFiles/walls/trojka4.png')
        self.wns = pygame.transform.scale(self.wns, (self.unit, self.unit))

        #proste - piony i poziomy
        self.ns = pygame.image.load('./graphics/pngFiles/walls/pion.png')
        self.ns = pygame.transform.scale(self.ns, (self.unit, self.unit))

        self.we = pygame.image.load('./graphics/pngFiles/walls/poziom.png')
        self.we = pygame.transform.scale(self.we, (self.unit, self.unit))

        #zakrety - narozniki
        self.ne = pygame.image.load('./graphics/pngFiles/walls/naroznik1.png')
        self.ne = pygame.transform.scale(self.ne, (self.unit, self.unit))

        self.se = pygame.image.load('./graphics/pngFiles/walls/naroznik2.png')
        self.se = pygame.transform.scale(self.se, (self.unit, self.unit))

        self.sw = pygame.image.load('./graphics/pngFiles/walls/naroznik3.png')
        self.sw = pygame.transform.scale(self.sw, (self.unit, self.unit))

        self.nw = pygame.image.load('./graphics/pngFiles/walls/naroznik4.png')
        self.nw = pygame.transform.scale(self.nw, (self.unit, self.unit))

        #koncowki
        self.endN = pygame.image.load('./graphics/pngFiles/walls/koncowka1.png')
        self.endN = pygame.transform.scale(self.endN, (self.unit, self.unit))

        self.endE = pygame.image.load('./graphics/pngFiles/walls/koncowka2.png')
        self.endE = pygame.transform.scale(self.endE, (self.unit, self.unit))

        self.endS = pygame.image.load('./graphics/pngFiles/walls/koncowka3.png')
        self.endS = pygame.transform.scale(self.endS, (self.unit, self.unit))

        self.endW = pygame.image.load('./graphics/pngFiles/walls/koncowka4.png')
        self.endW = pygame.transform.scale(self.endW, (self.unit, self.unit))

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
        for ghost in self.ghosts:
            if not ghost.eaten:
                self.screen.blit(ghost.getImage(), (self.dx+ghost.xNormalized*self.unit, self.dy+ghost.yNormalized*self.unit))

        #rysowanie Pac-Mana
        self.screen.blit(self.player.getImage(), (self.dx+self.player.xNormalized*self.unit, self.dy+self.player.yNormalized*self.unit))


        #przeslony na tunele
        x, y = self.tunels[0]
        pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.unit,self.dy+y*self.unit,self.unit,self.unit))
        x, y = self.tunels[1]
        pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.unit,self.dy+y*self.unit,self.unit,self.unit))
        #przeslony pionowe (boki)
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.dx, self.screen_height))
        pygame.draw.rect(self.screen, BLACK, (self.dx+self.nX*self.unit, 0, self.dx, self.screen_height))
        #przeslony poziome (gora-dol)
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.screen_width, self.dy))
        pygame.draw.rect(self.screen, BLACK, (0, self.dy+self.nY*self.unit, self.screen_width, self.dy))

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

    def checkWinOrDefeat(self):
        #przegrana
        if self.player.hp <= 0:
            self.activeGame = False
        #wygrana
        if self.player.dotScore == self.dotScore:
            self.activeGame = False

    def moveAll(self):
        #ZMIANY KIERUNKU RUCHU
        #Pac-Man
        if self.counter % self.playerMoveTime == 0:
            #potwierdzam poprzednia zmiane pozycji
            self.player.confirmPosition(self.tunels)

            
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
                self.startDinnerTime = time.time()
                self.dinnerBonus = 200
            #wisienki
            if self.boardTab[xp][yp] == 6:
                self.player.otherScore += 100
                self.boardTab[xp][yp] = 0
                self.cherryExist = False
                self.cherryStartTime = time.time()

            #sprawdzam czy moge jesc duszki
            canBeEaten = False
            if self.startDinnerTime != None and time.time() - self.startDinnerTime < self.dinnerDuration:
                canBeEaten = True
            else:
                self.startDinnerTime = None
            
            #sprawdzam czy wszedlem na duszka
            for ghost in self.ghosts:
                if ghost.x == self.player.x and ghost.y == self.player.y:
                    #jesli moge jesc to zjadam jesli nie to trace hp
                    if canBeEaten:
                        ghost.eaten = True
                        self.player.otherScore += self.dinnerBonus
                        self.dinnerBonus *= 2
                    else:
                        self.player.hp -= 1
                        break


            #sprawdzam koniec gry
            self.checkWinOrDefeat()

            #tworze ew wisienki
            self.cherryService()

            
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
            

        #RUCH
        #Pac-Man
        self.player.move()

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


    #metoda robocza
    def placeGhosts(self):
        self.ghosts=[]
        while True:
            x = random.randint(1,self.nX-2)
            y = random.randint(1,self.nY-2)
            if self.boardTab[x][y] == 2:
                self.ghosts.append(Clyde(x,y,self.playerMoveTime,0.8))
                break
        
        while True:
            x = random.randint(1,self.nX-2)
            y = random.randint(1,self.nY-2)
            if self.boardTab[x][y] == 2:
                self.ghosts.append(Blinky(x,y,self.playerMoveTime,0.8))
                break
        
        while True:
            x = random.randint(1,self.nX-2)
            y = random.randint(1,self.nY-2)
            if self.boardTab[x][y] == 2:
                self.ghosts.append(Inky(x,y,self.playerMoveTime,0.8))
                break

        while True:
            x = random.randint(1,self.nX-2)
            y = random.randint(1,self.nY-2)
            if self.boardTab[x][y] == 2:
                self.ghosts.append(Pinky(x,y,self.playerMoveTime,0.8))
                break


    def run(self):
        while self.activeGame:
            #ruszanie
            self.moveAll()

            #rysowanie
            self.draw()

            #przechwytywanie zdarzen
            for event in pygame.event.get():
                #zamykanie okna
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #zmiana rozmiaru okna - koniecznosc przeliczenia niektorych zmiennych
                elif event.type == pygame.WINDOWEXPOSED:
                    self.calculateScreen()
                    self.loadImages()

                #keydowny
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #LPM
                    if event.button == 1:
                        self.mouse_is_pressed = True

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

            
            #odswiezanie okna
            pygame.display.update()

            #obsluga licznika
            self.counter += 1
            if self.counter >= 1000:
                self.counter = 0

            #kontroluje FPS
            self.clock.tick(self.FPS)



# game = Game("./maps/first.npy")
# game.run()
