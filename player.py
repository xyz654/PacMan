import time
from enums import Direction


class PacMan:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.xNormalized = x
        self.yNormalized = y
        self.v = 1/t
        self.direction = None
        self.nextDirection = None
        self.isInTunel = False
        self.tunelDuration = 0.5
        self.startTunel = 0

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

    
