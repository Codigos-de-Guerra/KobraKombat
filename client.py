import pygame
import tkinter as tk
from tkinter import simpledialog
from kobra_kombat_game import Game, LoginDialog
from global_var import *

import socket
import signal
import pickle

flag = True

def INT_handler(sig_num, arg):# {{{
    flag = False
    pygame.quit()# }}}

def conectar():# {{{
    root = tk.Tk()
    root.withdraw()
    d = LoginDialog(root, "Login")
    return (d.r1, int(d.r2)) # }}}

# reads directions when inputed
def directions(avaiable_keys):# {{{
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
            pygame.quit()

    keys = pygame.key.get_pressed()

    for key, dire in avaiable_keys.items():
        if keys[key]:
            return dire

    return None# }}}

def main():# {{{
    signal.signal(signal.SIGINT, INT_handler)
    avaiable_keys = { pygame.K_LEFT:"l",
                      pygame.K_RIGHT:"r",
                      pygame.K_UP:"u",
                      pygame.K_DOWN:"d" }

    pygame.init()
    win = pygame.display.set_mode((SIZE+150, SIZE))
    clock = pygame.time.Clock()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(conectar())

        ip, port = s.getsockname()
        conn = (ip + ":" + str(port))

        while flag:
            pygame.time.delay(DELAY)
            clock.tick(TICK)

            try:
                client_direction = directions(avaiable_keys)
            except:
                break

            if client_direction:
                s.sendall((conn + "_" + client_direction + ";").encode('ascii'))
            else:
                s.sendall((conn + "_NO" + ";").encode('ascii'))

            data = s.recv(1048576)

            try:
                Id, game = pickle.loads(data)
                game.redrawWindow(win, Id)
            except:
                print("FAIL!")


        s.sendall((conn + "_OUT" + ";").encode('ascii'))# }}}

main()
