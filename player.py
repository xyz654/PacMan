import time
import pygame
from enums import Direction


class PacMan:
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

    def loadImages(self, border):
        self.frames = []
        self.frames.append(pygame.image.load('./graphics/pacman1.png'))
        self.frames.append(pygame.image.load('./graphics/pacman2.png'))
        self.frames.append(pygame.image.load('./graphics/pacman3.png'))
        self.frames.append(pygame.image.load('./graphics/pacman4.png'))
        self.frames.append(pygame.image.load('./graphics/pacman5.png'))
        self.frames.append(pygame.image.load('./graphics/pacman6.png'))

        for i in range(6):
            self.frames[i] = pygame.transform.scale(self.frames[i], (border, border))

    def getImage(self):
        #co jakis czas zmieniam returnowany obrazek
        currTime = time.time()
        if currTime - self.imageTime >= self.imageDuration:
            self.imageTime = time.time()
            self.imageIterator += 1
        
        #wyswietlam obrazek
        toReturn = None
        if self.imageIterator >= len(self.frames):
            if self.imageIterator >= 2*len(self.frames):
                self.imageIterator = 0
            else:
                toReturn = self.frames[len(self.frames) - self.imageIterator-1]
        if toReturn == None:
            toReturn = self.frames[self.imageIterator]
        
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
        