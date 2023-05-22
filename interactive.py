import time
import pygame
import random
from enums import Direction


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


#zmienne globalne dotyczace AI duszkow
scatterTime = 7
chaseTime = 20



class GameElement:
    def __init__(self, x, y, t, tunelTime):
        self.x = x
        self.y = y
        self.xNormalized = x
        self.yNormalized = y
        self.v = 1/t
        self.direction = None
        self.nextDirection = None
        self.isInTunel = False
        self.tunelDuration = tunelTime
        self.startTunel = 0
        self.imageIterator = 0
        self.imageDuration = 0.05
        self.imageTime = time.time()

    def move(self):
        if self.direction == Direction.NORTH:
            self.yNormalized -= self.v
        elif self.direction == Direction.SOUTH:
            self.yNormalized += self.v
        elif self.direction == Direction.EAST:
            self.xNormalized += self.v
        elif self.direction == Direction.WEST:
            self.xNormalized -= self.v

    def confirmPosition(self, tunels, nx, ny):
        #jesli jestem w tunelu i odczekuje opoznienie
        if self.isInTunel:
            #sprawdzam czas
            endTunel = time.time()
            tunelTime = endTunel - self.startTunel
            #jesli jeszcze czas nie uplynal to dalej czekam
            if tunelTime < self.tunelDuration:
                return
            #jesli czas uplynal to moge dalej isc
            self.isInTunel = False
            #ustawiam poprawna pozycje
            if tunels[0] == (self.x, self.y):
                self.x = tunels[1][0]
                self.y = tunels[1][1]
                if self.x == 0:
                    self.direction = Direction.EAST
                elif self.x == nx-1:
                    self.direction = Direction.WEST
                elif self.y == 0:
                    self.direction = Direction.SOUTH
                elif self.y == ny-1:
                    self.direction = Direction.NORTH
            else:
                self.x = tunels[0][0]
                self.y = tunels[0][1]
                if self.x == 0:
                    self.direction = Direction.EAST
                elif self.x == nx-1:
                    self.direction = Direction.WEST
                elif self.y == 0:
                    self.direction = Direction.SOUTH
                elif self.y == ny-1:
                    self.direction = Direction.NORTH
            self.xNormalized = self.x
            self.yNormalized = self.y

        #jesli nie jestem w oczekiwaniu na przejscie tunelu
        elif self.direction == Direction.NORTH:
            #sprawdzam tunel
            if self.y == 0 and (self.x, self.y) in tunels:
                self.isInTunel = True
                self.startTunel = time.time()
                return
            #jesli to nie tunel to wszystko ok
            else:
                self.y -= 1
            self.xNormalized = self.x
            self.yNormalized = self.y
        elif self.direction == Direction.SOUTH:
            #sprawdzam tunel
            if self.y > 0 and (self.x, self.y) in tunels:
                self.isInTunel = True
                self.startTunel = time.time()
                return
            #jesli to nie tunel to wszystko ok
            else:
                self.y += 1
            self.xNormalized = self.x
            self.yNormalized = self.y
        elif self.direction == Direction.EAST:
            #sprawdzam tunel
            if self.x > 0 and (self.x, self.y) in tunels:
                self.isInTunel = True
                self.startTunel = time.time()
                return
            #jesli to nie tunel to wszystko ok
            else:
                self.x += 1
            self.xNormalized = self.x
            self.yNormalized = self.y
        elif self.direction == Direction.WEST:
            #sprawdzam tunel
            if self.x == 0 and (self.x, self.y) in tunels:
                self.isInTunel = True
                self.startTunel = time.time()
                return
            #jesli to nie tunel to wszystko ok
            else:
                self.x -= 1
            self.xNormalized = self.x
            self.yNormalized = self.y

    def loadImages(self, imagesPaths):
        #laduje obrazki
        self.frames = []
        for imgPath in imagesPaths:
            self.frames.append(pygame.image.load(imgPath))
        
    def scaleImages(self, unit):
        #skaluje zaladowane obrazki
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], (unit, unit))

    def getImage(self, tab):
        #co jakis czas zmieniam returnowany obrazek
        currTime = time.time()
        if currTime - self.imageTime >= self.imageDuration:
            self.imageTime = time.time()
            self.imageIterator += 1
        
        #wyswietlam obrazek
        toReturn = None
        if self.imageIterator >= len(tab):
            if self.imageIterator >= 2*len(tab):
                self.imageIterator = 0
            else:
                toReturn = tab[len(tab) - self.imageIterator-1]
        if toReturn == None:
            toReturn = tab[self.imageIterator]

        return toReturn



class PacMan(GameElement):
    def __init__(self, x, y, t, tunelTime, hp):
        super().__init__(x,y,t,tunelTime)
        self.hp = hp
        self.dotScore = 0
        self.otherScore = 0

    def backToPosition(self, posX, posY):
        self.x = posX
        self.y = posY
        self.xNormalized = posX
        self.yNormalized = posY
        self.direction = None
        self.nextDirection = None
        
    def loadImages(self):
        paths = []
        paths.append('./graphics/pngFiles/pacman/pacman1.png')
        paths.append('./graphics/pngFiles/pacman/pacman2.png')
        paths.append('./graphics/pngFiles/pacman/pacman3.png')
        paths.append('./graphics/pngFiles/pacman/pacman4.png')
        paths.append('./graphics/pngFiles/pacman/pacman5.png')
        paths.append('./graphics/pngFiles/pacman/pacman6.png')
        super().loadImages(paths)
    
    def getImage(self):
        toReturn = super().getImage(self.frames)

        #obracanie w zaleznosci od kierunku ruchu
        if self.direction == Direction.NORTH:
            toReturn = pygame.transform.rotate(toReturn, 0)
        elif self.direction == Direction.EAST:
            toReturn = pygame.transform.rotate(toReturn, -90)
        elif self.direction == Direction.SOUTH:
            toReturn = pygame.transform.rotate(toReturn, 180)
        elif self.direction == Direction.WEST:
            toReturn = pygame.transform.rotate(toReturn, 90)
        elif self.nextDirection == Direction.NORTH:
            toReturn = pygame.transform.rotate(toReturn, 0)
        elif self.nextDirection == Direction.EAST:
            toReturn = pygame.transform.rotate(toReturn, -90)
        elif self.nextDirection == Direction.SOUTH:
            toReturn = pygame.transform.rotate(toReturn, 180)
        elif self.nextDirection == Direction.WEST:
            toReturn = pygame.transform.rotate(toReturn, 90)

        return toReturn

class Ghost(GameElement):
    def __init__(self, x, y, t, tunelTime, type):
        super().__init__(x,y,t,tunelTime)
        #jedzenie
        self.eaten = False
        self.type = type
        #AI
        self.targetX = self.x
        self.targetY = self.y
        self.timeAI = time.time()
        self.isInChase = random.choice([True, False])
    
    def loadImages(self, imagesPaths):
        #laduje obrazki do zjedzenia
        eatenPaths = ['./graphics/pngFiles/ghosts/blue/blue1.png',
                      './graphics/pngFiles/ghosts/blue/blue2.png',
                      './graphics/pngFiles/ghosts/blue/blue3.png']
        self.eatenImgs = []
        for imgPath in eatenPaths:
            self.eatenImgs.append(pygame.image.load(imgPath))

        return super().loadImages(imagesPaths)

    def setTarget(self, player, ghosts, nX, nY):
        #ewentualna zmiana moda
        now = time.time()
        if (self.isInChase and now-self.timeAI >= chaseTime) or ((not self.isInChase) and now-self.timeAI >= scatterTime):
            self.timeAI = now
            self.isInChase = not self.isInChase
            #obrot o 180 jezeli zaczyna polowac
            if self.isInChase:
                if self.direction == Direction.NORTH:
                    self.direction = Direction.SOUTH
                elif self.direction == Direction.EAST:
                    self.direction = Direction.WEST
                elif self.direction == Direction.SOUTH:
                    self.direction = Direction.NORTH
                elif self.direction == Direction.WEST:
                    self.direction = Direction.EAST

    def move(self, t):
        self.v = 1/t
        super().move()
    
    def respawn(self, x, y):
        self.x = x
        self.y = y
        self.xNormalized = x
        self.yNormalized = y
        self.direction = None
        self.nextDirection = None
        self.eaten = False

    def scaleImages(self, unit):
        #skaluje zaladowane obrazki zjescable duszkow
        for i in range(len(self.eatenImgs)):
            self.eatenImgs[i] = pygame.transform.scale(self.eatenImgs[i], (unit, unit))
        return super().scaleImages(unit)

    def getImage(self, canBeEaten):
        if canBeEaten:
            return super().getImage(self.eatenImgs)
        return super().getImage(self.frames)



class Clyde(Ghost):
    def __init__(self, x, y, t, tunelTime):
        super().__init__(x, y, t, tunelTime, "Clyde")
        self.color = ORANGE
        
        
    def loadImages(self):
        paths = []
        paths.append('./graphics/pngFiles/ghosts/clyde/clyde1.png')
        paths.append('./graphics/pngFiles/ghosts/clyde/clyde2.png')
        paths.append('./graphics/pngFiles/ghosts/clyde/clyde3.png')
        super().loadImages(paths)
    
    def setTarget(self, player, ghosts, nX, nY):
        super().setTarget(player, ghosts, nX, nY)
        
        #w zaleznosci w jakim jest modzie, tak ustawiam target
        if self.isInChase:
            #jesli sciga i jest od PacMana odpowiednio daleko to ma target na PacMana
            if (self.x - player.x)**2 + (self.y - player.y)**2 >= 6**2:
                self.targetX = player.x
                self.targetY = player.y
            #jesli jest za blisko, to leci do swojegu punktu ucieczki
            else:
                self.targetX = -1
                self.targetY = nY
        else:
            #jesli ucieka to ma target na lewy dolny rog 
            self.targetX = -1
            self.targetY = nY
    


class Blinky(Ghost):
    def __init__(self, x, y, t, tunelTime):
        super().__init__(x, y, t, tunelTime, "Blinky")
        self.color = RED
        

    def loadImages(self):
        paths = []
        paths.append('./graphics/pngFiles/ghosts/blinky/blinky1.png')
        paths.append('./graphics/pngFiles/ghosts/blinky/blinky2.png')
        paths.append('./graphics/pngFiles/ghosts/blinky/blinky3.png')
        super().loadImages(paths)

    def setTarget(self, player, ghosts, nX, nY):
        super().setTarget(player, ghosts, nX, nY)
        
        #w zaleznosci w jakim jest modzie, tak ustawiam target
        if self.isInChase:
            #jesli sciga to ma target na PacMana
            self.targetX = player.x
            self.targetY = player.y
        else:
            #jesli ucieka to ma target na prawy gorny rog 
            self.targetX = nX
            self.targetY = -1


class Inky(Ghost):
    def __init__(self, x, y, t, tunelTime):
        super().__init__(x, y, t, tunelTime, "Inky")
        self.color = BLUE


    def loadImages(self):
        paths = []
        paths.append('./graphics/pngFiles/ghosts/inky/inky1.png')
        paths.append('./graphics/pngFiles/ghosts/inky/inky2.png')
        paths.append('./graphics/pngFiles/ghosts/inky/inky3.png')
        super().loadImages(paths)

    def setTarget(self, player, ghosts, nX, nY):
        super().setTarget(player, ghosts, nX, nY)
        
        #w zaleznosci w jakim jest modzie, tak ustawiam target
        if self.isInChase:
            #jesli sciga to ma target zalezny od PacMana i Blinky'ego
            xb = 0
            yb = 0
            for ghost in ghosts:
                if ghost.type == "Blinky":
                    xb = ghost.x
                    yb = ghost.y
                    break
            
            if player.direction == Direction.NORTH:
                self.targetX = player.x-1
                self.targetY = player.y-1
            elif player.direction == Direction.EAST:
                self.targetX = player.x+1
                self.targetY = player.y
            elif player.direction == Direction.SOUTH:
                self.targetX = player.x
                self.targetY = player.y+1
            elif player.direction == Direction.WEST:
                self.targetX = player.x-1
                self.targetY = player.y

            dx = xb - self.targetX
            dy = yb - self.targetY

            self.targetX -= dx
            self.targetY -= dy
        else:
            #jesli ucieka to ma target na prawy dolny rog 
            self.targetX = nX
            self.targetY = nY
    


class Pinky(Ghost):
    def __init__(self, x, y, t, tunelTime):
        super().__init__(x, y, t, tunelTime, "Pinky")
        self.color = PINK


    def loadImages(self):
        paths = []
        paths.append('./graphics/pngFiles/ghosts/pinky/pinky1.png')
        paths.append('./graphics/pngFiles/ghosts/pinky/pinky2.png')
        paths.append('./graphics/pngFiles/ghosts/pinky/pinky3.png')
        super().loadImages(paths)

    def setTarget(self, player, ghosts, nX, nY):
        super().setTarget(player, ghosts, nX, nY)
        
        #w zaleznosci w jakim jest modzie, tak ustawiam target
        if self.isInChase:
            #jesli sciga to ma target na 4 unity przed PacManem (chyba ze gracz idzie do gory, wtedy tez 4 w lewo)
            if player.direction == Direction.NORTH:
                self.targetX = player.x-3
                self.targetY = player.y-3
            elif player.direction == Direction.EAST:
                self.targetX = player.x+3
                self.targetY = player.y
            elif player.direction == Direction.SOUTH:
                self.targetX = player.x
                self.targetY = player.y+3
            elif player.direction == Direction.WEST:
                self.targetX = player.x-3
                self.targetY = player.y
        else:
            #jesli ucieka to ma target na lewy gorny rog 
            self.targetX = -1
            self.targetY = -1
    



