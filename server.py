import pygame
import tkinter as tk

from kobra_kombat_game.game import Game

import socket
import time

from aux_server import manageInput, manageGameLogic, manageOutput
from global_var import *

def main():
    pygame.init()

    clock = pygame.time.Clock() # clock
    d = {}

    board = Game(SIZE,ROWS)
    port = 12347

    checkpoint_500ms = time.time()

    read_list = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(0)
        s.bind(('', port))
        s.listen(5)
        read_list.append(s)


        while True:
            pygame.time.delay(DELAY) # pausa em milisegundos
            clock.tick(TICK) # sincronizacao
            new_players, lost_connections, moves, socks_ok, d = manageInput(read_list, s, d)
            board, checkpoint_500ms = manageGameLogic(board, new_players, lost_connections, moves, checkpoint_500ms)
            manageOutput(socks_ok, board)

            if len(read_list) == 1:
                break

main()
