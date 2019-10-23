# cenario 2

import pygame
import tkinter as tk

from kobra_kombat_game.game import Game

import socket
import time
import threading

from aux_server import manageInput, manageGameLogic, manageOutput
from global_var import *

fila = []
flag = True

dur = {
    'i_time': 0,
    'o_time': 0,
    'g_time': 0
}



def thread_func(read_list, s, d):
    global flag
    while True:

        t = time.time()
        new_players, lost_connections, moves, socks_ok, d = manageInput(read_list, s, d)
        dur['i_time'] += time.time() - t

        fila.append((new_players, lost_connections, moves, socks_ok, d))

        if len(read_list) == 1:
            flag = False
            break


def main():
    global flag
    clock = pygame.time.Clock() # clock

    d = {}

    game = Game(SIZE, ROWS)
    PORT = 12347

    checkpoint_500ms = time.time()

    read_list = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(0)
        s.bind(('', PORT))
        s.listen(5)
        read_list.append(s)

        t = threading.Thread(target=thread_func, args=(read_list, s, d))
        t.start()

        while flag:
            # pygame.time.delay(DELAY) # pausa em milisegundos
            clock.tick(TICK) # sincronizacao
            while len(fila) != 0:
                new_players, lost_connections, moves, socks_ok, d = fila[0]
                fila.pop(0)

                t = time.time()
                game, checkpoint_500ms = manageGameLogic(game, new_players, lost_connections, moves, checkpoint_500ms)
                dur['g_time'] += time.time() - t

                t = time.time()
                manageOutput(socks_ok, game)
                dur['o_time'] += time.time() - t
        print(dur)


main()
