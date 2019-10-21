import pygame
import random
from .cube import Cube

class Snack(Cube):

    def __init__(self, pos):
        self.pos = pos
        Cube.__init__(self,self.pos,(0,255,0), (0, 0))
