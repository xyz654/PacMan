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

        #ogolne wymiary siatki w pixelach
        self.width = self.border*self.nX
        self.height = self.border*self.nY

        #przesuniecia by siatka byla na srodku
        self.dx = (self.screen_width-self.width)/2
        self.dy = (self.screen_height-self.height)/2

        #zmienne do przechowywania danych gry
        self.ghostRespawnArea = []


        #pobieram dane i je przypisuje do odpowiednich zmiennych
        self.boardTab = np.zeros((self.nX, self.nY))
        self.loadData("./first.npy")

        #okno
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pac-Man")

        # zegar
        self.clock = pygame.time.Clock()




    def loadData(self, path):
        if len(path)!=0:
            #pobieram dane z pliku
            with open(path, 'rb') as f:
                stats = np.load(f)
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
                        self.boardTab[i][j] = 2
    

    def draw(self):
        #wypelnianie ekranu kolorem
        self.screen.fill(WHITE)

        #rysowanie planszy
        for x in range(self.nX):
            for y in range(self.nY):
                #floor without dot or tunnel or ghost respawn area
                if self.boardTab[x][y] == 0 or self.boardTab[x][y] == 5:
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
                

    def run(self):
        while True:
            self.draw()

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




game = Game()
game.run()