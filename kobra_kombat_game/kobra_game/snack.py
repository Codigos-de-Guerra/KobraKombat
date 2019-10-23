import pygame
from .cube import Cube

# hehe to usando herença
class Snack(Cube):# {{{

    def __init__(self, pos):# {{{
        self.pos = pos
        Cube.__init__(self,self.pos,(0,255,0), (0, 0))# }}}
# }}}
