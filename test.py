# test.py - a test build of a new and improved terminal RPG engine
'''
    TODO 
    - change the face/text for each combatant with their name and message. not as important as implementing
      a shop rn but will need to be done

    Implement:
        -local multiplayer combat

'''
from msvcrt import getch
import sys
import os
import textwrap
import random
import ast

import faces
from testData import mapData
from testData import playerData
from testData import enemyData
from testData import enemyClass
from maps import gamePlayMaps
from maps import staticMaps
from mapChange import changeMap




####################################
#####       GLOBAL DATA        #####
####################################

class globalStates():

    ## gold won in combat to be printed later
    won_gold = 0
    
    # Gameplay map currently being rendered
    current_map = gamePlayMaps.map1
    
    # Gameplay commands used from player input for map - first assigned at runtime
    current_commands = None
    
    # Map to return to from pause menu
    return_map = None

    ## List of static maps for referencing in play loop
    static_maps = [staticMaps.menu, staticMaps.console_menu, staticMaps.shop_menu]
    combat_maps = [staticMaps.combat_map_enemy, staticMaps.combat_map_pl]



####################################
#####       MAP FUNCTIONS      #####
####################################

def overwrite_map(w_map):
    
    for i in range(len(w_map)):
        for j in range(len(w_map[0])):
            if w_map[i][j] == 'X':
                w_map[i][j] = ' '


def print_map(p_map):

    ## Print player data at top of map
    print(f'\n  HP: {str(playerData.HP)}/{str(playerData.MAX_HP)}   G: {str(playerData.GOLD)}')

    ## Print the Map
    for i in range(len(p_map)):
        for j in range(len(p_map[0])):
            print(p_map[i][j], end='')
        print()


def print_combat_screen(turn):

    ## Set map to players turn
    if turn == 1 or turn == 0:
        globalStates.current_map = staticMaps.combat_map_pl
    if turn == 2:
        globalStates.current_map = staticMaps.combat_map_enemy
    ## Print the map
    print(globalStates.current_map)


    ## print combatants health
    print(f'      HP: {playerData.HP}/{playerData.MAX_HP}     {enemyData.current_enemy.rank} {enemyData.current_enemy.name}: {enemyData.current_enemy.hp}')
    if turn == 0:
        print(f'\n\t[1] Laser Cannon\n\t[2] Missile ({str(playerData.MISSILES)})\n\t[3] Repairkit ({str(playerData.REPAIRKITS)})')




###################################
######   DIALOGUE / CONVO    ######
##################################

def dialoguePrompt(face, messages):
    print_face = face
    print_message = random.choice(messages)

    clear()
    print(f'\t\n      {enemyData.current_enemy.rank} {enemyData.current_enemy.name} says:')
    print(random.choice(print_face))
    text = textwrap.wrap(print_message, 25)
    for j in range(len(text)):
        print(text[j].center(36))
    getch()


# ### cut ###
# def speakableList(cur_map):

#     #####  MAP 2  #####
#     ## GIRL
#     if cur_map == gamePlayMaps.map2:
#         if (cur_map[mapData.pos_x][mapData.pos_y+1] == 'Q') or \
#            (cur_map[mapData.pos_x][mapData.pos_y-1] == 'Q'):
#             dialoguePrompt(faces.girl.face, faces.girl.messages)





##################################################
######      FUNCTIONALITY AND GAMEPLAY      ######
##################################################

def clear():
    os.system('cls')



################################################
#######         INPUT AND COMMANDS       #######
################################################


## This is the bulk of movement control. This command-function holds the main inputs
#  by players and does collision detection before making the move. If the move is through
#  a door, this is handled by the if/else blocks inside the cmd='' blocks. It basically
#  checks if the move is going to be into a door, and if it is, it returns True. This is
#  returned in the main loop, where a true return results in that info being sent to another
#  function to load the map in.  
def map_commands(cmd, cur_map):
    
    if cmd == 'w' and cur_map[mapData.pos_x - 1][mapData.pos_y] not in mapData.walls:
        if cur_map[mapData.pos_x - 1][mapData.pos_y] in mapData.doors:
            return True
        else:
            mapData.pos_x -= 1
    
    elif cmd == 's' and cur_map[mapData.pos_x + 1][mapData.pos_y] not in mapData.walls:
        if cur_map[mapData.pos_x + 1][mapData.pos_y] in mapData.doors:
            return True
        else:
            mapData.pos_x += 1
    
    elif cmd == 'a' and cur_map[mapData.pos_x][mapData.pos_y - 1] not in mapData.walls:
        if cur_map[mapData.pos_x][mapData.pos_y - 1] in mapData.doors:
            return True
        else:
            mapData.pos_y -= 2
    
    elif cmd == 'd' and cur_map[mapData.pos_x][mapData.pos_y + 1] not in mapData.walls:
        if cur_map[mapData.pos_x][mapData.pos_y + 1] in mapData.doors:
            return True
        else:
            mapData.pos_y += 2
    

    ## MENU command
    elif cmd == 'p':
        globalStates.return_map = globalStates.current_map
        globalStates.current_map = staticMaps.menu
        globalStates.current_commands = menu_commands
        
        
    # ## 'Enter' command
    # elif cmd == '\r' and ((cur_map[mapData.pos_x][mapData.pos_y+1] in mapData.friendlies) or
    #                       (cur_map[mapData.pos_x][mapData.pos_y-1] in mapData.friendlies)):
    #     speakableList(globalStates.current_map)
    
    ## Enter on command console
    elif cmd == '\r' and ((cur_map[mapData.pos_x][mapData.pos_y+1] == '#') or\
    (cur_map[mapData.pos_x-1][mapData.pos_y+1] == '#') or\
    (cur_map[mapData.pos_x][mapData.pos_y-1] == '#') or\
    (cur_map[mapData.pos_x-1][mapData.pos_y-1] == '#')):
        globalStates.current_commands = console_commands
        globalStates.return_map = globalStates.current_map
        globalStates.current_map = staticMaps.console_menu




def menu_commands(cmd, cur_screen):
    
    ## Continue
    if cmd == '1':
        globalStates.current_commands = map_commands
        globalStates.current_map = globalStates.return_map
    
    ## SAVE 
    elif cmd == '2':
        clear()
        save_game()

    ## LOAD
    elif cmd == '3':
        clear()
        load_game()

    ## EXIT
    elif cmd == '4':
        print('\n > EXIT? [ENTER] TO CONFIRM')
        confirmation = getch()

        if bytes.decode(confirmation) == '\r':
            sys.exit(0)
        else:
            pass
    

def console_commands(cmd, cur_map):
    
    if cmd == '1':  ## Combat

        ## initialize enemy to fight ##
        ## Randomize rank
        rank = random.choice(enemyData.ranks)
        ## Random name
        name = random.choice(enemyData.names)

        ## randomize hp and basedam 
        ## These are calculated based on the players current stat level
        en_hp = random.randint(int(round(playerData.STATS / 5)), int(round(playerData.STATS / 2.5))) + 6
        en_basedam = random.randint(int(round(playerData.STATS / 25)), int(round(playerData.STATS / 7)))
        if en_basedam < 1:
            en_basedam = 1

        ## initialize randomized enemy instance
        enemyData.current_enemy = enemyClass(rank, name, en_hp, en_basedam, faces.shopkeeper.face, faces.shopkeeper.messages)
        ## enemy speaks before combat
        dialoguePrompt(enemyData.current_enemy.face, enemyData.current_enemy.messages)

        #globalStates.return_map = globalStates.current_map
        globalStates.current_commands = combat_commands
        globalStates.current_map = staticMaps.combat_map_enemy

        # player gold reward for victory assigned beforehand so sue me. if you die you lose anyway                   
        won_gold = int(round(enemyData.current_enemy.hp / 2)) + random.randint(1, 8)
        playerData.STATS += int(round(enemyData.current_enemy.hp / 5)-1)
        playerData.GOLD += won_gold
        globalStates.won_gold = won_gold


    elif cmd == '2':    ## Shop
        globalStates.current_commands = shop_commands
        globalStates.current_map = staticMaps.shop_menu
    
    else:
        globalStates.current_map = globalStates.return_map
        globalStates.current_commands = map_commands


def shop_commands(cmd, cur_map):

    gp = playerData.GOLD
    no_gp = '\n     ** NOT ENOUGH GOLD **'

    if cmd == '1':
        if gp >= 10:
            playerData.REPAIRKITS += 1
            print('\n      +REPAIRKIT PURCHASED+')

            playerData.GOLD -= 10
            playerData.STATS += 1
            getch()

        else:
            print(no_gp)
            getch()


    elif cmd == '2':
        if gp >= 10:
            playerData.MISSILES += 1
            print('\n      +MISSILE PURCHASED+')
        
            playerData.GOLD -= 10
            playerData.STATS += 1
            getch()

        else:
            print(no_gp)
            getch()
    

    elif cmd == '3':
        if gp >= 20:
            playerData.CANNON_DAM += 1
            print('\n      +CANNON UPGRADED +')

            playerData.GOLD -= 20
            playerData.STATS += 1
            getch()

        else:
            print(no_gp)
            getch()


    elif cmd == '4':
        if gp >= 15:
            playerData.MAX_HP += 3
            playerData.HP = playerData.MAX_HP
            print('\n      +SHIELD UPGRADED +')

            playerData.GOLD -= 15
            playerData.STATS += 1
            getch()

        else:
            print(no_gp)
            getch()

    else:
        globalStates.current_commands = console_commands
        globalStates.current_map = staticMaps.console_menu




def combat_commands(cmd, cur_map):

    turn_completed = False

    ## Cannon
    if cmd == '1':
        damage = random.randint(playerData.CANNON_DAM, playerData.CANNON_DAM + 4)
        enemyData.current_enemy.hp -= damage
        if enemyData.current_enemy.hp < 0:
            enemyData.current_enemy.hp = 0

        clear()
        print_combat_screen(1)
        print(f'\n\tCannon does {str(damage)} dam')
        getch()

        turn_completed = True

    ## Missiles
    elif cmd == '2':
        if playerData.MISSILES > 0:
            ## subtract missile from inventory
            playerData.MISSILES -= 1

            ## calculate enemy damage and enact it
            damage = random.randint(playerData.CANNON_DAM + 4, playerData.CANNON_DAM + 9)
            enemyData.current_enemy.hp -= damage
            if enemyData.current_enemy.hp < 0:
                enemyData.current_enemy.hp = 0
        
            ## Print damage report
            clear()
            print_combat_screen(1)
            print(f'\n\tMissile does {str(damage)} dam')
            getch()

            turn_completed = True
        
        else:
            print('\t**  NO MISSILES  **')
            getch()

    ## Repair
    elif cmd == '3':
        if playerData.REPAIRKITS > 0 and playerData.HP == playerData.MAX_HP:
            print('\t**  HEALTH MAXIMUM  **')
            getch()

        elif playerData.REPAIRKITS > 0:
            
            playerData.REPAIRKITS -= 1

            ## If player health plus repairkit is more than their max hp, just make it equal max hp
            if (playerData.HP + 10) > playerData.MAX_HP:
                playerData.HP = playerData.MAX_HP
            else:
                playerData.HP += 10

            clear()
            print_combat_screen(1)
            print(f'\n\tShip Repaired +10 hp')
            getch()

            turn_completed = True
        else:
            print('\t**  NO REPAIRKITS  **')
            getch()

    else:
        pass

    if turn_completed and enemyData.current_enemy.hp > 0:
        enemyTurn()


def enemyTurn():
    clear()

    ##Damage range for enemy based on their base damage
    player_dam = random.randint(enemyData.current_enemy.basedam, enemyData.current_enemy.basedam + 3)
    playerData.HP -= player_dam

    if playerData.HP < 0:
        playerData.HP = 0
    
    print_combat_screen(2)
    print(f'\n\t{enemyData.current_enemy.name} attacks for -{str(player_dam)} dam')
    getch()

    if playerData.HP <= 0:
        clear()
        print('\n\n\n\tYOU HAVE DIED\n\n\tsucks to fuckin suck fuckeroni')
        getch()
        sys.exit()



####################################
#####        SAVE / LOAD       #####
####################################

def save_game():
    ## SAVE ORDER: xpos, ypos, current_map, pl_hp, pl_gold, missiles, maxhp, stats, repairkits, candam
    save_xpos = str(mapData.pos_x)
    save_ypos = str(mapData.pos_y)
    save_cur_map = str(mapData.load_map_list.index(globalStates.return_map))
    save_hp = str(playerData.HP)
    save_gold = str(playerData.GOLD)
    save_missiles = str(playerData.MISSILES)
    save_max_hp = str(playerData.MAX_HP)
    save_stats = str(playerData.STATS)
    save_repairkits = str(playerData.REPAIRKITS)
    save_cannon_dam = str(playerData.CANNON_DAM)


    clear()
    ## Print save files and ask for file input 
    saveFiles = []
    for filename in os.listdir('.'):
        if filename.startswith('savegame'):
            saveFiles.append(filename)
    print('\n    --SAVE AS:')
    print('    [1] New Save')

    i = 2
    for file in saveFiles:
        print('    ['+str(i)+'] '+file)
        i +=1
    print('\n    ['+str(i)+'] Back')

    fileinp = getch()
    fileChoice = bytes.decode(fileinp)

    ## Name new save file
    invalidChars = ['?', '\\', '/', ':', '"', '<', '>', '*']
    if fileChoice == str(i):
        return
    else:
        if fileChoice == '1':
            ## CHECK IF 7+ save files already
            if len(saveFiles) >= 7:
                print('\n   MAXIMUM NUMBER OF SAVE FILES REACHED')
                getch()
                return 
            else:
                clear()
                print('    ENTER A NAME FOR FILE:')
                name = input('    > ')
                for i in invalidChars:
                    if i in name:
                        print('\n    #INVALID CHARACTERS IN NAME#')
                        input()
                        return
                openfile = open('savegame_'+name+'.txt', 'w+')
                
        ## Try to open and rewrite save file
        else:
            try:
                openfile = open(saveFiles[int(fileChoice)-2], 'w+')
            except (ValueError, IndexError):
                print('> Unable to save to this file')
                getch()
                return


        ## WRITE DATA TO FILE
        ## SAVE ORDER: xpos, ypos, current_map, pl_hp, pl_gold missiles, maxhp, stats
        openfile.truncate()
        openfile.write(save_xpos); openfile.write("\n")
        openfile.write(save_ypos); openfile.write("\n")
        openfile.write(save_cur_map); openfile.write("\n")
        openfile.write(save_hp); openfile.write("\n")
        openfile.write(save_gold); openfile.write("\n")
        openfile.write(save_missiles); openfile.write("\n")
        openfile.write(save_max_hp); openfile.write("\n")
        openfile.write(save_stats); openfile.write("\n")
        openfile.write(save_repairkits) ; openfile.write("\n")
        openfile.write(save_cannon_dam) ; openfile.write("\n")     

        print(f'\n  GAME SAVED')
        getch()
        

def load_game():
    clear()

    ## List out all saved games in current directory
    saved_files_list = []
    for savefile in os.listdir('.'):
        if savefile.startswith('savegame'):
            saved_files_list.append(savefile)
    
    ## Print the saved files
    print('\n      -- SAVE FILES --')
    
    ## index numb for printing and selection
    i = 1
    for file in saved_files_list:
        print('    ['+str(i)+'] '+file)
        i+=1

    print('\n    ['+str(i)+'] BACK')
    
    file_input = getch()
    file_choice = bytes.decode(file_input)

    if file_choice == str(i):
        return
    else:
        try:
            load_file = open(saved_files_list[int(file_choice)-1])
        except (ValueError, IndexError):
            return
            
        try:
            ## LOAD DATA FROM FILE
            ## ORDER: xpos, ypos, current_map, pl_hp, pl_gold, missiles, maxhp, stats, repairkits, candam
            load_xpos = int(load_file.readline())
            load_ypos = int(load_file.readline())
            load_cur_map = int(load_file.readline())
            load_pl_hp = int(load_file.readline())
            load_pl_gold = int(load_file.readline())
            load_pl_missiles = int(load_file.readline())
            load_pl_max_hp = int(load_file.readline())
            load_pl_stats = int(load_file.readline())
            load_pl_repairkits = int(load_file.readline())
            load_pl_cannon_dam = int(load_file.readline())
            load_file.close()
                
            mapData.pos_x = load_xpos
            mapData.pos_y = load_ypos
            globalStates.current_map = mapData.load_map_list[load_cur_map]
            playerData.HP = load_pl_hp
            playerData.GOLD = load_pl_gold
            playerData.MISSILES = load_pl_missiles
            playerData.MAX_HP = load_pl_max_hp
            playerData.STATS = load_pl_stats
            playerData.REPAIRKITS = load_pl_repairkits
            playerData.CANNON_DAM = load_pl_cannon_dam
                
            print('\n       GAME LOADED')

            globalStates.current_commands = map_commands
                    

        except ValueError:
            clear()
            print('\n\n    #  SAVE FILE CORRUPTED OR EMPTY  #')
            print('    # PLEASE SELECT A DIFFERENT FILE #')
            print('\n    [press key]')
            getch()
        



####################################
#####      THE OL GAME LOOP    #####
#################################### 


def Main():

    while True:

        ## Assign current screen (map, menu, combat) to be printed and modified
        current_screen = globalStates.current_map
        ## Assign uncalled command function for current maps avaliable inputs
        current_command = globalStates.current_commands

        clear()
        
        ## Gameplay for menus- static screens with options instead of motion
        if current_screen in globalStates.static_maps:
            if current_screen != staticMaps.menu:   
                print(f'\n  HP: {str(playerData.HP)}/{str(playerData.MAX_HP)}   G: {str(playerData.GOLD)}')
            for line in current_screen:
                print(line)
        
        ## COMBAT MODE
        elif current_screen in globalStates.combat_maps:
            
            ## While enemy is still alive, keep combat going
            if enemyData.current_enemy.hp > 0:
                ## Print combat map and character data
                print_combat_screen(0)
            
            ## Player death condition ############## dubious at best
            elif playerData.HP <= 0:
                clear()
                print('\n\n\n\tYOU HAVE DIED\n\n\tsucks to fuckin suck fuckeroni')
                getch()
                sys.exit()
            
            ## Enemy death
            else:
                globalStates.current_map = staticMaps.console_menu
                globalStates.current_commands = console_commands

                ## random event, 1 in 6 chance player gets a free missile
                win_event = random.randint(1,10)
                
                ## victory message
                print(f'\n\n\t  +++VICTORY+++ \n\n\t{enemyData.current_enemy.name} is defeated\n\n\t      +{str(globalStates.won_gold)}gp')
                
                ## if win, give shit and whatnot
                if win_event == 2:
                    print('\n     You scavenge +1 missile')
                    playerData.MISSILES += 1
                elif win_event == 9:
                    print('\n     You scavenge +1 repairkit')
                    playerData.REPAIRKITS += 1

                getch()
                continue


        ## GAMEPLAY DYNAMIC MODE
        else:
            ## erase last player location
            overwrite_map(current_screen)
            ## Set current coordinates on the map to pl character
            current_screen[mapData.pos_x][mapData.pos_y] = 'X'
            print_map(current_screen)

    
        ## Get the ol player input key
        player_input = getch()

        ## Run input through the current commands to get results
        returnAction = current_command(bytes.decode(player_input), current_screen)
        
        ## If player has entered new room, the movement command is sent to changeMap in MapChange.py
        ## where it takes the input to know which door the player is moving through and which room 
        ## they're in, thus calculating which room to move to. Below returns the map to the current map.
        if returnAction:
            globalStates.current_map = changeMap(current_screen, bytes.decode(player_input))




## Assign player commands at runtime
globalStates.current_commands = map_commands
Main()