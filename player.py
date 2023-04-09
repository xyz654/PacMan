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

    def move(self):
        if self.direction == Direction.NORTH:
            self.yNormalized -= self.v
        elif self.direction == Direction.SOUTH:
            self.yNormalized += self.v
        elif self.direction == Direction.EAST:
            self.xNormalized += self.v
        elif self.direction == Direction.WEST:
            self.xNormalized -= self.v

    def confirmPosition(self):
        if self.direction == Direction.NORTH:
            self.y -= 1
            self.yNormalized = self.y
        elif self.direction == Direction.SOUTH:
            self.y += 1
            self.yNormalized = self.y
        elif self.direction == Direction.EAST:
            self.x += 1
            self.xNormalized = self.x
        elif self.direction == Direction.WEST:
            self.x -= 1
            self.xNormalized = self.x

    
