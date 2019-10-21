import pygame

class Cube(object):

    def __init__(self, start, color, dire):
        self.pos = start
        self.dirnx, self.dirny = dire
        self.color = color

    def move(self, dire=None):
        if dire != None:
            self.dirnx, self.dirny = dire
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, size, rows, eyes=False):
        dis = size // rows
        i, j = self.pos

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


