import pygame
from .cube import Cube

#TODO COMEÇAR COBRA COM TAMANHO 3
## Tanto no init quanto no reset

class Kobra(object):# {{{

    def __init__(self, color, pos, dire):# {{{
        self.color = color
        self.head = Cube(pos, self.color, dire)
        self.body = [self.head]
        self.dirnx, self.dirny = dire
        self.turns = {}
        self.alive = True
        self.score = 1# }}}

        self.addCube()
        self.addCube()

    def move(self, rows, key=None):# {{{
        if key == "l":
            self.dirnx, self.dirny = (-1, 0)

        elif key == "r":
            self.dirnx, self.dirny = (1,0)

        elif key == "u":
            self.dirnx, self.dirny = (0,-1)

        elif key == "d":
            self.dirnx, self.dirny = (0,1)

        self.turns[self.head.pos] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos

            if p in self.turns:
                turn = self.turns[p]
                if i == len(self.body)-1:
                    self.turns.pop(p)
                c.move(turn)
            else:
                c.move()

            if c.dirnx == -1 and c.pos[0] < 0: c.pos = (rows-1, c.pos[1])
            if c.dirnx == 1 and c.pos[0] > rows-1: c.pos = (0,c.pos[1])
            if c.dirny == 1 and c.pos[1] > rows-1: c.pos = (c.pos[0], 0)
            if c.dirny == -1 and c.pos[1] < 0: c.pos = (c.pos[0],rows-1)
# }}}

    def reset(self, pos):# {{{
        self.head = Cube(pos, self.color, (0,1))
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.alive = True
        self.score = 1# }}}

        self.addCube()
        self.addCube()

    def die(self):# {{{
        self.head = None
        self.body = []
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.alive = False# }}}

    def addCube(self):# {{{
        self.score += 1
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        NewPos = (tail.pos[0]-dx, tail.pos[1]-dy)
        self.body.append(Cube(NewPos, self.color, (dx, dy)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy# }}}

    def draw(self, surface, size, rows):# {{{
        for i, c in enumerate(self.body):
            c.draw(surface, size, rows, i==0)# }}}
# }}}
