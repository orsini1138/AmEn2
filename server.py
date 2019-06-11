## TODO:
'''
    -make host an input by player and validate host

'''

import socket
import os
import threading
import time
import sys
from maps import staticMaps
import random


## to change later to get automatically of local ip instead of localhost
HOST = '127.0.0.1'
## gets port from cmdline argument sent when player runs server from multiplayer_lobby_cmds
PORT = int(sys.argv[1])
BUFF_SIZE = 2048
ADDR = (HOST, PORT)

## Run socket
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

## Running message and ip/port data
print('\n[*] SERVER RUNNING\n\n[*] IP: '+HOST+'\n[*] PORT: '+str(PORT)+'\n')



class serverData():

    CLIENTS = {}
    ADDRESSES = {}

    PLAYER_ALTERNATOR = 0

    PLAYER_A = {'name':'', 'hp':0, 'max_hp':0, 'dam':0, 'missiles':0, 'repairkits':0}
    PLAYER_B = {'name':'', 'hp':0, 'max_hp':0, 'dam':0, 'missiles':0, 'repairkits':0}

    map_list = [staticMaps.combat_map_pl, staticMaps.combat_map_enemy]



## To broadcast a msg to all players
def broadcast(message):
    for user in serverData.CLIENTS:
        user.send(f"{message}".encode())


## So host can close server from server terminal
def server_cmds():
    while True:
        cmd = input('> ')

        if cmd.lower() == 'help':
            print('[*] \'quit\' to close server and exit current game')
            print('[*] \'help\' for list of commands (limited at the moment)')
        elif cmd.lower() == 'quit':
            SERVER.close()
            os.sys.exit(0)



def accept_clients():

    total_clients = 0

    while True:
        ## List amt of clients currently
        print('[*] '+str(total_clients) + ' client(s) connected')
        SERVER.listen(2)

        client_socket, client_address = SERVER.accept()
        serverData.ADDRESSES[client_socket] = client_address

        total_clients += 1
        
        print('\n[*] Connected by ', client_address)
        client_socket.sendall('> You are now connected to server. Enter username: '.encode())

        ## Receive client name
        client_name = client_socket.recv(BUFF_SIZE).decode()
        serverData.CLIENTS[client_socket] = client_name

        print(f'[*] {client_name} has joined the game.\n')

        if total_clients == 2:
            print('[*] Connections successful- Starting Game')
            # time.sleep(3)
            break



def load_game(player_a, player_b):
    
    ## Run server commands while game goes on
    # CMD_THREAD = threading.Thread(target=server_cmds)
    # CMD_THREAD.start()

    ## get player a stats
    player_a.send('stats'.encode())
    player_a_stats = []
    
    while True:
        player_a_stats = player_a.recv(BUFF_SIZE).decode().split('.')
        break
        
    serverData.PLAYER_A['name'] = player_a_stats[0]
    serverData.PLAYER_A['hp'] = int(player_a_stats[1])
    serverData.PLAYER_A['max_hp'] = int(player_a_stats[2])
    serverData.PLAYER_A['dam'] = int(player_a_stats[3])
    serverData.PLAYER_A['missiles'] = int(player_a_stats[4])
    serverData.PLAYER_A['repairkits'] = int(player_a_stats[5])

    ## get player b stats
    player_b.send('stats'.encode())
    player_b_stats = []

    while True:
        player_b_stats = player_b.recv(BUFF_SIZE).decode().split('.')
        break
        
    serverData.PLAYER_B['name'] = player_b_stats[0]
    serverData.PLAYER_B['hp'] = int(player_b_stats[1])
    serverData.PLAYER_B['max_hp'] = int(player_b_stats[2])
    serverData.PLAYER_B['dam'] = int(player_b_stats[3])
    serverData.PLAYER_B['missiles'] = int(player_b_stats[4])
    serverData.PLAYER_B['repairkits'] = int(player_b_stats[5])



def run_game(player_a, player_b):
    
    print('\n[*] GAME RUNNING [*]')
    
    while True:
        # break
        ## make map and health id text/img. The pl_alternator + 2 is to avoid dividing 0 on first move
        send_map = serverData.map_list[(serverData.PLAYER_ALTERNATOR+2) % 2] + \
            (f"\n    {serverData.PLAYER_A['name']}").ljust(15) + (f'{serverData.PLAYER_B["name"]}').rjust(21) + \
            (f"\n    {serverData.PLAYER_A['hp']}/{serverData.PLAYER_A['max_hp']}").ljust(15) + \
            (f"{serverData.PLAYER_B['hp']}/{serverData.PLAYER_B['max_hp']}").rjust(21) + '\n'

        ## broadcast map and health 
        broadcast(send_map)

        ## WIN CONDITIONS ##
        ## check if player a has health below 0
        if serverData.PLAYER_A['hp'] <= 0 or serverData.PLAYER_B['hp'] <= 0:
            
            ## check if player a is dead
            if serverData.PLAYER_A['hp'] <= 0:
                broadcast(f'->> {serverData.PLAYER_B["name"]} Wins! <<-')
                
                ## Player a loot
                time.sleep(1)
                player_a.send('5'.encode())
                
                ## Player b loot
                player_b_loot = round((serverData.PLAYER_B['max_hp'] / 6) + serverData.PLAYER_B['hp'])
                player_b.send(str(player_b_loot).encode())
                
                # time.sleep(3)

            ## player b is dead
            elif serverData.PLAYER_B['hp'] <= 0:
                broadcast(f'->> {serverData.PLAYER_A["name"]} Wins! <<-')
                
                ## Player a loot
                time.sleep(1)
                player_a_loot = round((serverData.PLAYER_A['max_hp'] / 6) + serverData.PLAYER_A['hp'])
                player_a.send(str(player_a_loot).encode())

                ## Player b loot
                player_b.send('5'.encode())
                
                # time.sleep(3)
            
            for client in serverData.CLIENTS:
                client.close()
            
            SERVER.close()
            os.sys.exit(0)
            # break
                

        ## re assignable variables for attacker and defender set to none
        attacker = player_a
        attacker_stats = serverData.PLAYER_A
        defender = player_b
        defender_stats = serverData.PLAYER_B

        ## if player alternator is odd number, swap attacker and defender vars
        if serverData.PLAYER_ALTERNATOR % 2 != 0:
            attacker = player_b
            attacker_stats = serverData.PLAYER_B
            defender = player_a
            defender_stats = serverData.PLAYER_A

        time.sleep(.1)

        ## send to A a list of their items and options
        attacker.send('> Your Turn'.encode())
        defender.send((f'> {attacker_stats["name"]}\'s turn').encode())

        # recv player a action
        attacker_action = attacker.recv(BUFF_SIZE)
        
        ## MSG to later broadcast with the resulting damage
        damage_report = ''

        ## Calculate damage and results
        ## laser cannon
        if attacker_action.decode() == '1':
            
            dam = random.randint(attacker_stats['dam'], attacker_stats['dam'] + 4)
            defender_stats['hp'] -= dam 

            if defender_stats['hp'] < 0:
                defender_stats['hp'] = 0

            damage_report = '\n\t> Laser Cannon does -' + str(dam) + ' damage'
            #del
            print(attacker_stats['name']+ ' uses laser cannon - '+str(dam)+' dam')
        
        ## Missile
        elif attacker_action.decode() == '2':
            
            attacker_stats['missiles'] -= 1
            dam = random.randint(attacker_stats['dam'] + 4, attacker_stats['dam'] + 9)
            defender_stats['hp'] -= dam

            if defender_stats['hp'] < 0:
                defender_stats['hp'] = 0

            damage_report = '\n\t> Missile does -' + str(dam) + ' damage' 
            #del
            print(attacker_stats['name']+ ' uses missile - '+str(dam)+' dam')

        ## repairkit
        elif attacker_action.decode() == '3':
            
            attacker_stats['repairkits'] -= 1
            repair_amount = 10 + random.randint(1,5)

            if (attacker_stats['hp'] + repair_amount) > attacker_stats['max_hp']:
                attacker_stats['hp'] = attacker_stats['max_hp']
            else:
                attacker_stats['hp'] += repair_amount
            
            damage_report = '\n\t'+attacker_stats['name'] + '\'s ship repaired +' + str(repair_amount) + ' hp' 
            #del
            print(attacker_stats['name']+ ' uses repairkit - '+str(repair_amount)+' hp')
        
        
        ## quit
        elif attacker_action.decode() == '4':
            broadcast('quit')
            SERVER.close()

        
        ## rebroadcast map n health
        broadcast(send_map)
        broadcast(damage_report)

        time.sleep(3)
        
        ## ++ player alternator
        serverData.PLAYER_ALTERNATOR += 1
        
        ## broadcast confirmation to continue
        broadcast('conf')

        ## time.sleep(.1 or .2 ) to keep sync
        time.sleep(.1)



def main():

    ## recieve players
    accept_clients()

    ## create list of player socket ids
    client_list = []
    for cli in serverData.CLIENTS:
        client_list.append(cli)

    ## Collect players data and save to vars
    load_game(client_list[0], client_list[1])

    ## Begin the gameplay
    run_game(client_list[0], client_list[1])



main()
SERVER.close()
