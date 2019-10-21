#Snake Tutorial Python

import math
import pygame
import tkinter as tk
from tkinter import messagebox

from cube import Cube
from snake import Snake
from snack import Snack

delay = 50
tick = 10
rows = 10
size = 500

def drawGrid(size, rows, surface):
    sizeBtwn = size // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,size))
        pygame.draw.line(surface, (255,255,255), (0,y),(size,y))


def redrawWindow(surface):
    global s, snack
    surface.fill((0,0,0))
    s.draw(surface, size, rows)
    snack.draw(surface, size, rows)
    drawGrid(size,rows, surface)
    pygame.display.update()


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global s, snack
    win = pygame.display.set_mode((size, size))
    s = Snake((255,0,255), (5,5))
    snack = Snack(rows, s)
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(delay)
        clock.tick(tick)
        s.move(rows)
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = Snack(rows, s)

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10,10))
                break

        redrawWindow(win)

    pass

main()
