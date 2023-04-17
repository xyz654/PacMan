import time
import pygame
from enums import Direction



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

    def confirmPosition(self, tunels):
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
            else:
                self.x = tunels[0][0]
                self.y = tunels[0][1]
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
    def __init__(self, x, y, t, tunelTime):
        super().__init__(x,y,t,tunelTime)
        self.eaten = False
    
    def loadImages(self, imagesPaths):
        #laduje obrazki do zjedzenia
        eatenPaths = ['./graphics/pngFiles/ghosts/blue/blue1.png',
                      './graphics/pngFiles/ghosts/blue/blue2.png',
                      './graphics/pngFiles/ghosts/blue/blue3.png']
        self.eatenImgs = []
        for imgPath in eatenPaths:
            self.eatenImgs.append(pygame.image.load(imgPath))

        return super().loadImages(imagesPaths)
    
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
    def loadImages(self):
        paths = []
        paths.append('./graphics/pngFiles/ghosts/clyde/clyde1.png')
        paths.append('./graphics/pngFiles/ghosts/clyde/clyde2.png')
        paths.append('./graphics/pngFiles/ghosts/clyde/clyde3.png')
        super().loadImages(paths)
    


class Blinky(Ghost):
    def loadImages(self):
        paths = []
        paths.append('./graphics/pngFiles/ghosts/blinky/blinky1.png')
        paths.append('./graphics/pngFiles/ghosts/blinky/blinky2.png')
        paths.append('./graphics/pngFiles/ghosts/blinky/blinky3.png')
        super().loadImages(paths)
    


class Inky(Ghost):
    def loadImages(self):
        paths = []
        paths.append('./graphics/pngFiles/ghosts/inky/inky1.png')
        paths.append('./graphics/pngFiles/ghosts/inky/inky2.png')
        paths.append('./graphics/pngFiles/ghosts/inky/inky3.png')
        super().loadImages(paths)
    


class Pinky(Ghost):
    def loadImages(self):
        paths = []
        paths.append('./graphics/pngFiles/ghosts/pinky/pinky1.png')
        paths.append('./graphics/pngFiles/ghosts/pinky/pinky2.png')
        paths.append('./graphics/pngFiles/ghosts/pinky/pinky3.png')
        super().loadImages(paths)
    



