import math
import pygame
from game import Game

SIZE = 500
ROWS = 20
DELAY = 50
TICK = 10

def directions(avaiable_keys):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        keys = pygame.key.get_pressed()

        for key in avaiable_keys:
            if keys[key]:
                return key

    return None

def main():

    avaiable_keys = [ pygame.K_LEFT,
                      pygame.K_RIGHT,
                      pygame.K_UP,
                      pygame.K_DOWN ]

    app = Game(SIZE, ROWS)
    win = pygame.display.set_mode((app.size, app.size))
    clock = pygame.time.Clock()

    app.addKobra(1)
    app.addKobra(2)
    # app.addKobra(3)
    pos = app.randomPos()
    app.addSnack(pos)

    flag = True

    while flag:
        pygame.time.delay(DELAY)
        clock.tick(TICK)

        key = directions(avaiable_keys)
        moves = {1:key, 2:key}

        app.passScene(moves)

        if len(app.snacks) < 1:
            pos = app.randomPos()
            app.addSnack(pos)

        some_alive = False

        for kobra in app.kobras.values():
            if kobra.alive:
                some_alive = True
                break

        if not some_alive:
            print("Morreu tudo")
            for Id in app.kobras:
                print("User: ", Id, "Score: ", app.kobras[Id].score)
            app.message_box("You lost!", "Play again...")

            for kobra in app.kobras.values():
                pos = app.randomPos()
                kobra.reset(pos)
        # for x in range(len(snake.body)):
        #     if snake.body[x].pos in list(map(lambda z:z.pos,snake.body[x+1:])):
        #         print("Score: ", snake.score)
        #         app.message_box("You lost!", "Play again...")
        #         snake.reset((10,10))
        #         break

        app.redrawWindow(win)

    pass


main()
