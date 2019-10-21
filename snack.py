import pygame
import random
from cube import Cube

class Snack(Cube):

    def __init__(self, rows, kobra):
        pos = self.randomSnack(rows, kobra)
        Cube.__init__(self,pos, 0, 0, (0,255,0))

    def randomSnack(self, rows, kobra):
        positions = kobra.body

        while True:
            x = random.randrange(rows)
            y = random.randrange(rows)
            if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
                continue
            else:
                break

        return (x,y)
