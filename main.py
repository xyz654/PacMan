import pygame
import sys
import numpy as np
from enums import Direction
from player import PacMan

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
    def __init__(self, path):
        pygame.init()

        #glowne stale
        self.FPS = 60
        self.nX = 20 
        self.nY = 25 

        #dane dot okna i jego rozmiaru
        self.screen_width = 700
        self.screen_height = 600

        self.border = 20

        #ogolne wymiary siatki w pixelach
        self.width = self.border*self.nX
        self.height = self.border*self.nY

        #przesuniecia by siatka byla na srodku
        self.dx = (self.screen_width-self.width)/2
        self.dy = (self.screen_height-self.height)/2

        #zmienne do przechowywania danych gry
        self.ghostRespawnArea = []
        self.difficulty = 1
        self.cherryTime = 1
        self.hp = 1
        self.boostTime = 1

        #gracz
        self.playerMoveTime = 20
        self.player = None

        #pobieram dane i je przypisuje do odpowiednich zmiennych
        self.boardTab = np.zeros((self.nX, self.nY))
        self.loadData(path)

        #tworze graf w postaci listy sasiedztwa
        self.tunels = []
        self.graph = None
        self.makeGraph()

        #okno
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Pac-Man")

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
        if len(path)!=0:
            #pobieram dane z pliku
            with open(path, 'rb') as f:
                #zbieranie statystyk
                stats = np.load(f)
                self.difficulty = stats[0]
                self.cherryTime = stats[1]
                self.hp = stats[2]
                self.boostTime = stats[4]
                #zbieranie planszy
                for i in range(self.nX):
                    for j in range(self.nY):
                        self.boardTab[i][j] = np.load(f)[0]
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
                        self.player = PacMan(i,j, self.playerMoveTime)
                        self.boardTab[i][j] = 2
    
    def calculateScreen(self):
        #pobieram rozmiary okna
        self.screen_width, self.screen_height = self.screen.get_size()

        self.border = 20

        #ogolne wymiary siatki w pixelach
        self.width = self.border*self.nX
        self.height = self.border*self.nY

        #przesuniecia by siatka byla na srodku
        self.dx = (self.screen_width-self.width)/2
        self.dy = (self.screen_height-self.height)/2

    def draw(self):
        #wypelnianie ekranu kolorem
        self.screen.fill(BLACK)

        #rysowanie planszy
        for x in range(self.nX):
            for y in range(self.nY):
                #floor without dot or tunnel or ghost respawn area
                if self.boardTab[x][y] == 0:
                    pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
                #wall
                if self.boardTab[x][y] == 1:
                    pygame.draw.rect(self.screen,BLUE,(self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
                #floor with dot
                if self.boardTab[x][y] == 2:
                    pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
                    pygame.draw.circle(self.screen, YELLOW_LIGHT, (self.dx+x*self.border+self.border/2, self.dy+y*self.border+self.border/2), self.border/6)
                #big dot
                if self.boardTab[x][y] == 3:
                    pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
                    pygame.draw.circle(self.screen, YELLOW_LIGHT, (self.dx+x*self.border+self.border/2, self.dy+y*self.border+self.border/2), self.border/4)
        
        #rysowanie Pac-Mana
        pygame.draw.circle(self.screen, YELLOW, (self.dx+self.player.xNormalized*self.border+self.border/2, self.dy+self.player.yNormalized*self.border+self.border/2), self.border/3)



        #przeslony na tunele
        x, y = self.tunels[0]
        pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
        x, y = self.tunels[1]
        pygame.draw.rect(self.screen, BLACK, (self.dx+x*self.border,self.dy+y*self.border,self.border,self.border))
        #przeslony pionowe (boki)
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.dx, self.screen_height))
        pygame.draw.rect(self.screen, BLACK, (self.dx+self.nX*self.border, 0, self.dx, self.screen_height))
        #przeslony poziome (gora-dol)
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.screen_width, self.dy))
        pygame.draw.rect(self.screen, BLACK, (0, self.dy+self.nY*self.border, self.screen_width, self.dy))

    def moveAll(self):
        #ZMIANY KIERUNKU RUCHU
        #Pac-Man
        if self.counter % self.playerMoveTime == 0:
            #potwierdzam poprzednia zmiane pozycji
            self.player.confirmPosition(self.tunels)

            #pobieram dane do zmiennych lokalnych by latwiej sie ich uzywalo
            xp = self.player.x
            yp = self.player.y
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


    def run(self):
        while True:
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




game = Game("./first.npy")
game.run()