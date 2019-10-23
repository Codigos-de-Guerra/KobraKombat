from random import randint, randrange
import pygame
import tkinter as tk

from .kobra_game import *

class Game(object):

    def __init__(self, size, rows):# {{{
        self.size = size
        self.rows = rows
        self.kobras = {}
        self.snacks = {}# }}}

    def addKobra(self, Id):# {{{
        count = 0
        while True:
            color = (randint(0,255), randint(0,255), randint(0,255))
            for kobra in self.kobras.values():
                if color == kobra.color:
                    count += 1
            if count == 0:
                break

        pos = self.randomPos()
        self.kobras[Id] = Kobra(color, pos, (0,1))# }}}

    def KobraKill(self, Id):# {{{
        kill = self.kobras[Id]
        for cube in kill.body:
            self.addSnack(cube.pos)
        kill.die()# }}}

    def addSnack(self, pos=None):# {{{
        if pos == None:
            pos = self.randomPos()
        self.snacks[pos] = Snack(pos)# }}}

    def delSnack(self):# {{{
        pos = None
        for kobra in self.kobras.values():
            if kobra.alive:
                if kobra.head.pos in self.snacks:
                    kobra.addCube()
                    del self.snacks[kobra.head.pos]# }}}

    def getScores(self):# {{{
        scores = []
        for IdUser, kobra in self.kobras.items():
            if kobra.alive:
                scores.append((kobra.score, IdUser))

        scores.sort(reverse=True)

        return scores# }}}

    # Checking for all kobras
    def KobraKollision(self):# {{{
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

        del occupied# }}}

    def newScene(self, moves):# {{{
        for Id, kobra in self.kobras.items():
            if kobra.alive:
                if Id in moves:
                    self.kobras[Id].move(self.rows, moves[Id])
                else:
                    self.kobras[Id].move(self.rows)

        self.delSnack()
        self.KobraKollision()# }}}

    def message_box(self,subject, content):# {{{
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        tk.messagebox.showinfo(subject, content)
        try:
            root.destroy()
        except:
            pass# }}}

    def randomPos(self):# {{{
        positions = [cube.pos for kobra in self.kobras.values() for cube in kobra.body]
        for pos in self.snacks:
            positions.append(pos)

        while True:
            x = randrange(self.rows)
            y = randrange(self.rows)
            if (x,y) in positions:
                continue
            else:
                break

        return (x,y)# }}}

    def drawGrid(self, surface):# {{{
        sizeBtwn = self.size // self.rows

        x = 0
        y = 0
        for l in range(self.rows):
            x = x + sizeBtwn
            y = y + sizeBtwn

            pygame.draw.line(surface, (255,255,255), (x,0),(x,self.size))
            pygame.draw.line(surface, (255,255,255), (0,y),(self.size,y))# }}}

    def drawEndGame(self, surface, Id):# {{{
        bigbigFont = pygame.font.SysFont('comicsansms', 52)

        goText = bigbigFont.render('WASTED', True, (255,255,255), (0,0,0))
        scoreText = bigbigFont.render('YOUR SCORE: {}'.format(self.kobras[Id].score), True, (255,255,255), (0,0,0))

        goTextRect = goText.get_rect()
        scoreTextRect = scoreText.get_rect()

        goTextRect.center = (self.size//2, self.size//2)
        scoreTextRect.center = (self.size//2, self.size//2 + goTextRect.height)

        surface.blit(goText, goTextRect)
        surface.blit(scoreText, scoreTextRect)# }}}

    def redrawWindow(self, surface, Id):# {{{
        surface.fill((0,0,0))
        self.drawGrid(surface)
        self.drawInfo(surface, Id)

        for s in self.kobras.values():
            s.draw(surface, self.size, self.rows)
        for snack in self.snacks.values():
            snack.draw(surface, self.size, self.rows)

        if not self.kobras[Id].alive:
            self.drawEndGame(surface, Id)

        pygame.display.update()# }}}

    def drawInfo(self, surface, Id):# {{{
        bigFont = pygame.font.SysFont('comicsansms', 32)
        normalFont = pygame.font.SysFont('comicsansms', 22)
        smallFont = pygame.font.SysFont('comicsansms', 18)

        idText = normalFont.render('Your ID is: {}'.format(Id), True, (255,255,255), (0,0,0))
        titleText = bigFont.render('ScoreBoard', True, (255,255,255), (0,0,0))

        titleTextRect = titleText.get_rect()
        idTextRect = idText.get_rect()

        titleTextRect.topleft = (self.size + 15, 15)
        idTextRect.topleft = (self.size + 15, titleTextRect.height + 15)

        surface.blit(titleText, titleTextRect)
        surface.blit(idText, idTextRect)

        scores = self.getScores()
        # scores = [1,2,3]

        lastHeight = titleTextRect.height + idTextRect.height + 15
        for score in scores:
            scoreText = smallFont.render("{}: {}".format(score[1], score[0]), True, (255,255,255), (0,0,0))
            scoreTextRect = scoreText.get_rect()
            scoreTextRect.topleft = (self.size + 15, lastHeight + 10)
            lastHeight = scoreTextRect.height + lastHeight
            surface.blit(scoreText, scoreTextRect)# }}}

