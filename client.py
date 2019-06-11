## TODO
'''
    -
'''

import socket
import os
import time
from msvcrt import getch


class clientData():

    
    HOST = '127.0.0.1'
    PORT = None

    NAME = ''
    USERNAME = False

    PL_HP = 0
    PL_MAX_HP = 0
    PL_DAM = 0
    PL_MISSILES = 0
    PL_REPAIRKITS = 0

    RETURN_LOOT = 0

    ## Connects to server lobby and gets player name then sends to server
    def client_connect(CLIENT):

        while True:
            data = CLIENT.recv(1024) 
            print(data.decode())

            if data:
                if not clientData.USERNAME:
                    
                    username = ''
                    
                    while True:
                        input_username = input('> ')
                        if len(input_username) > 10:
                            print('>> NAME TOO LONG')
                        elif input_username == '' or input_username == ' ':
                            print('>> Write a real name jackass')
                        else:
                            username = input_username
                            break

                    clientData.NAME = username
                    CLIENT.send(username.encode())
                    print('\n[*] Waiting for 2nd player connection.\n[*] Close server terminal to disconnect safely')

                break


    ## Sends player name, stats to server for pregame load=in so server can hold the data
    def send_stats(CLIENT):
        while True:
            confirm_send = CLIENT.recv(1024)
            if confirm_send.decode() == 'stats':
                ## once the server sends confirmation that it's ready to recv, 
                ## here the player is sending a string of the stats separated by'
                ## periods so that the server can split by '.' and assign properly
                CLIENT.send((clientData.NAME+'.'+str(clientData.PL_HP) + '.'+ str(clientData.PL_MAX_HP)\
                            + '.' + str(clientData.PL_DAM) + '.' + str(clientData.PL_MISSILES) \
                            + '.' + str(clientData.PL_REPAIRKITS)).encode())
                break

    ## Main game loop to run
    def main_loop(CLIENT):
        
        while True:
            os.system('cls')
           
            map_round_start = CLIENT.recv(2048).decode()
            time.sleep(.5)
            current_turn = CLIENT.recv(2048).decode()
            

            print(map_round_start)
            print('\t'+current_turn)
            
            ## check for win condition
            if current_turn.startswith('-'):

                loot_received = CLIENT.recv(1024).decode()
                print('\n\t     >> You win +' + loot_received + 'g')

                clientData.RETURN_LOOT = int(loot_received)
                break

            

            ## print msg here saying "you won + "+gold+"gold" and gold var is
            ## from cli.recv, send at game end on victory condition, then the
            ## function here returns that to main,py and adds it
                 

            if current_turn.lower() == '> your turn':

                ## When player gives valid input, it's put into this and then sent to server
                send_option = ''

                ## Option loop
                while True:

                    ## print attackers options
                    print('\n\t[1] Laser Cannon' + \
                        f'\n\t[2] Missile ({str(clientData.PL_MISSILES)})' + \
                        f'\n\t[3] Repairkit ({str(clientData.PL_REPAIRKITS)})' + \
                        '\n\t[4] Leave')
                    
                    attacker_input = bytes.decode(getch())

                    ## laser cannon
                    if attacker_input == '1':

                        send_option = attacker_input
                        break
                    
                    ## missiles
                    elif attacker_input == '2':

                        if clientData.PL_MISSILES <= 0:
                            print('\n\t>> NO MISSILES')
                            getch()
                            os.system('cls')
                            print(map_round_start)
                            print('\t'+current_turn)

                        else:
                            send_option = attacker_input
                            clientData.PL_MISSILES -= 1
                            break

                    ## repairkits
                    elif attacker_input == '3':

                        if clientData.PL_REPAIRKITS <= 0:
                            print('\n\t>> NO REPAIRKITS')
                            getch()
                            os.system('cls')
                            print(map_round_start)
                            print('\t'+current_turn)

                        else:
                            send_option = attacker_input
                            clientData.PL_REPAIRKITS -= 1
                            break
                    
                    ## leave multiplayer battle
                    elif attacker_input == '4':

                        print('\n\t>> EXIT? 1-yes / 2-no')
                        quit_option = bytes.decode(getch())

                        if quit_option == '1':
                            send_option = attacker_input
                            break
                        else:
                            os.system('cls')
                            print(map_round_start)
                            print('\t'+current_turn)

                    ## Any invalid key
                    else:
                        os.system('cls')
                        print(map_round_start)
                        print('\t'+current_turn)
                        
                ## Send player chice to server        
                CLIENT.send(send_option.encode())

            
            damage_map = CLIENT.recv(1024).decode()
            if damage_map == 'quit':
                print('\n\t> THE SERVER HAS BEEN SHUT DOWN')
                break
            damage_report = CLIENT.recv(1024).decode()

            os.system('cls')

            print(damage_map)
            print(damage_report)

            time.sleep(2)


            ## Confirmation for turn end
            CLIENT.recv(1024)
            

        return clientData.RETURN_LOOT