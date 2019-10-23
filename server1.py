# cenario 1

# IMPORTS {{{
import pygame
import tkinter as tk

from kobra_kombat_game.game import Game

import socket
import time
import threading

from aux_server import manageInput, manageGameLogic, manageOutput
from global_var import *
# }}}

def thread_func(PORT, dur):# {{{
    read_list = []
    clock = pygame.time.Clock() # clock
    checkpoint_500ms = time.time()
    d = {}
    game = Game(SIZE,ROWS)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(0)
        s.bind(('', PORT))
        s.listen(5)
        read_list.append(s)
        while True:
            clock.tick(TICK) # sincronizacao

            t = time.time()
            new_players, lost_connections, moves, socks_ok, d = manageInput(read_list, s, d)
            dur['io_time'] += time.time() - t

            t = time.time()
            game, checkpoint_500ms = manageGameLogic(game, new_players, lost_connections, moves, checkpoint_500ms)
            dur['game_logic_time'] += time.time() - t

            t = time.time()
            manageOutput(socks_ok, game)
            dur['io_time'] += time.time() - t

            if(len(read_list) == 1):
                break
# }}}

def main():# {{{
    PORT = 12346

    dur = {
        'io_time': 0,
        'game_logic_time': 0
    }

    t = threading.Thread(target=thread_func, args=(PORT, dur))
    t.start()
    t.join()

    print(dur)
# }}}

main()
