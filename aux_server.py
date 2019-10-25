import pickle
import select
import time

def manageInput(read_list, s, d):# {{{
    readable, writeable, error = select.select(read_list,[],[])

    new_players, lost_connections, moves, socks_ok = [], [], [], []

    for sock in readable:
        if sock is s:
            conn, info = sock.accept()
            read_list.append(conn)
            print("connection received from ", info)
            ip, port = info
            cons = (ip + ':' + str(port))
            d[cons] = len(d)
            new_players.append(d[cons])

        else:
            data = sock.recv(1048576)

            if data:
                data = data.decode('ascii').split(';')[0]
                head, body = data.split('_')
                id_user = d[head]

                if body == 'OUT':
                    lost_connections.append(id_user)
                    sock.close()
                    read_list.remove(sock)
                else:
                    move = body
                    moves.append((id_user, move))
                    socks_ok.append((id_user, sock))

            else:
                sock.close()
                read_list.remove(sock)

    return new_players, lost_connections, moves, socks_ok, d# }}}

def manageGameLogic(game, new_players, lost_connections, moves, checkpoint_500ms):# {{{
    for lost_con in lost_connections:
        game.KobraKill(lost_con)

    for player in new_players:
        game.addKobra(player)

    for id_user, move in moves:
        game.newScene({id_user: move})

    if time.time() - checkpoint_500ms >= 0.5:
        game.addSnack()
        checkpoint_500ms = time.time()

    return game, checkpoint_500ms# }}}

def manageOutput(socks_ok, game):# {{{
    gameEncoded = pickle.dumps(game, protocol=2)

    for id_user, sock in socks_ok:
        encoded = pickle.dumps((id_user, game), protocol=2)
        sock.send(encoded)# }}}
