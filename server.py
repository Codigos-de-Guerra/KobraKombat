# Conexao de referencia

# IMPORTS {{{
import pygame
import socket
import time
import tkinter as tk

from aux_server import manageInput, manageGameLogic, manageOutput
from global_var import *
from kobra_kombat_game.game import Game
# }}}

def main():# {{{
    pygame.init()

    clock = pygame.time.Clock() # clock
    d = {}

    game = Game(SIZE,ROWS)
    PORT = 12345

    checkpoint_500ms = time.time()

    read_list = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(0)
        s.bind(('', PORT))
        s.listen(5)
        read_list.append(s)


        while True:
            clock.tick(TICK) # sincronizacao
            new_players, lost_connections, moves, socks_ok, d = manageInput(read_list, s, d)
            game, checkpoint_500ms = manageGameLogic(game, new_players, lost_connections, moves, checkpoint_500ms)
            manageOutput(socks_ok, game)

            if len(read_list) == 1:
                break
# }}}
main()
