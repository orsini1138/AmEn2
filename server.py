import socket
import os
import time
import sys


## to change later to get automatically of local ip instead of localhost
HOST = '127.0.0.1'
## gets port from cmdline argument sent when player runs server from multiplayer_lobby_cmds
PORT = int(sys.argv[1])

BUFF_SIZE = 1024
ADDR = (HOST, PORT)

CLIENTS = {}
ADDRESSES = {}

## Run socket
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)


print('\n[*] SERVER RUNNING\n\n[*] IP: '+HOST+'\n[*] PORT: '+str(PORT)+'\n')


def accept_clients():

    total_clients = 0

    while True:
        ## List amt of clients currently
        print('[*] '+str(total_clients) + ' client(s) connected')
        SERVER.listen(2)

        client_socket, client_address = SERVER.accept()
        ADDRESSES[client_socket] = client_address

        total_clients += 1
        
        print('Connected by ', client_address)
        client_socket.sendall('> You are now connected to server'.encode())

        if total_clients == 2:
            print('[*] Connections successful, now closing')
            time.sleep(3)

            break
        



def main():
    accept_clients()

main()
SERVER.close()
