import socket
import os


class clientData():

    
    HOST = '127.0.0.1'
    PORT = None

    PL_HP = 0
    PL_MAX_HP = 0
    PL_DAM = 0
    PL_MISSILES = 0
    PL_REPAIRKITS = 0

    def client_connect(HOST, PORT):

        CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CLIENT.connect((HOST, PORT))

        while True:

            data = CLIENT.recv(1024)
            
            print(data.decode())

            if data:
                input('> ')
                CLIENT.close()
                break
