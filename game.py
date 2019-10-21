import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

from game_creation import *

class Game(object):
    def __init__(self, size, rows):
        self.size = size
        self.rows = rows
        self.kobras = {}
        self.snacks = {}

    def drawGrid(self, size, rows, surface):
        sizeBtwn = size // rows

        x = 0
        y = 0
        for l in range(rows):
            x = x + sizeBtwn
            y = y + sizeBtwn

            pygame.draw.line(surface, (255,255,255), (x,0),(x,size))
            pygame.draw.line(surface, (255,255,255), (0,y),(size,y))


    def redrawWindow(self, surface):
        surface.fill((0,0,0))

        for s in self.kobras.values():
            s.draw(surface, self.size, self.rows)
        for snack in self.snacks.values():
            snack.draw(surface, self.size, self.rows)
        self.drawGrid(self.size,self.rows, surface)
        pygame.display.update()


    def message_box(self,subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        try:
            root.destroy()
        except:
            pass

    def passScene(self, moves):
        for Id, kobra in self.kobras.items():
            if kobra.alive:
                if Id in moves:
                    self.kobras[Id].move(self.rows, moves[Id])
                else:
                    self.kobras[Id].move(self.rows)

        self.delSnack()
        self.KobraKollision()

    def randomPos(self):
        positions = [cube.pos for kobra in self.kobras.values() for cube in kobra.body]
        for pos in self.snacks:
            positions.append(pos)

        while True:
            x = random.randrange(self.rows)
            y = random.randrange(self.rows)
            if (x,y) in positions:
                continue
            else:
                break

        return (x,y)

    # Checking for all kobras
    def KobraKollision(self):
        occupied = {}
        for kobra in self.kobras.values():
            if kobra.alive:
                for cube in kobra.body:
                    try:
                        occupied[cube.pos] += 2
                    except:
                        occupied[cube.pos] = 1

        for Id, kobra in self.kobras.items():
            if kobra.alive:
                if occupied[kobra.head.pos] > 1:
                    self.KobraKill(Id)

        del occupied

    def delSnack(self):
        pos = None
        for kobra in self.kobras.values():
            if kobra.alive:
                if kobra.head.pos in self.snacks:
                    kobra.addCube()
                    del self.snacks[kobra.head.pos]

    def KobraKill(self, Id):
        kill = self.kobras[Id]
        for cube in kill.body:
            self.addSnack(cube.pos)
        kill.die()

    def addKobra(self, Id):
        count = 0
        while True:
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            for kobra in self.kobras.values():
                if color == kobra.color:
                    count += 1
            if count == 0:
                break

        pos = self.randomPos()
        self.kobras[Id] = Snake(color, pos, (0,1))

    def addSnack(self, pos):
        self.snacks[pos] = Snack(pos)

    def main(self):
        global s, snack
        win = pygame.display.set_mode((self.size, self.size))
        s = Snake((255,0,255), (5,5), (0,1))
        snack = Snack(self.rows, s)
        flag = True

        clock = pygame.time.Clock()

        while flag:
            pygame.time.delay(DELAY)
            clock.tick(TICK)
            s.move(self.rows)
            if s.body[0].pos == snack.pos:
                s.addCube()
                snack = Snack(self.rows, s)

            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                    print('Score: ', s.score)
                    self.message_box('You Lost!', 'Play again...')
                    s.reset((10,10))
                    break

            self.redrawWindow(win)

        pass
