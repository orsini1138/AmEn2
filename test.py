# test.py - a test build of a new and improved terminal RPG engine
'''
    TODO 
    - figure out how to pass in the face/msg into dialogue prompt funct

    Implement:
        -combat
        -shop
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
from maps import maps
from mapChange import changeMap




####################################
#####       GLOBAL DATA        #####
####################################

class globalStates():
    # Gameplay map currently being rendered
    current_map = maps.map1
    # Gameplay commands used from player input for map - first assigned at runtime
    current_commands = None
    # Map to return to from pause menu
    return_map = None



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
    print(f'\nHP: {str(playerData.HP)}   G: {str(playerData.GOLD)}')
    
    ## Print the Map
    for i in range(len(p_map)):
        for j in range(len(p_map[0])):
            print(p_map[i][j], end='')
        print()



###################################
######   DIALOGUE / CONVO    ######
##################################

def dialoguePrompt(face, messages):
    print_face = face
    print_messages = messages
    for i in range(len(print_messages)):
        clear()
        print(random.choice(print_face))
        text = textwrap.wrap(print_messages[i], 25)
        for j in range(len(text)):
            print(text[j].center(36))
        getch()


def speakableList(cur_map):

    #####  MAP 1  #####
    ## Man
    if cur_map == maps.map1:
        if (cur_map[mapData.pos_x][mapData.pos_y+1] == 'M') or \
           (cur_map[mapData.pos_x][mapData.pos_y-1] == 'M'):
            dialoguePrompt(faces.man.face, faces.man.messages)

    #####  MAP 2  #####
    ## GIRL
    if cur_map == maps.map2:
        if (cur_map[mapData.pos_x][mapData.pos_y+1] == 'Q') or \
           (cur_map[mapData.pos_x][mapData.pos_y-1] == 'Q'):
            dialoguePrompt(faces.girl.face, faces.girl.messages)





##################################################
######      FUNCTIONALITY AND GAMEPLAY      ######
##################################################

def clear():
    os.system('cls')


def combat_commands():
    pass


## This is the bulk of movement control. This command-function holds the main inputs
#  by players and does collision detection before making the move. If the move is through
#  a door, this is handled by the if/else blocks inside the cmd='' blocks. It basically
#  checks if the move is going to be into a door, and if it is, it returns True. This is
#  returned in the main loop, where a true return results in that info being sent to another
#  function to load the map in. This is all still being done manually, so there might be 
#  a better way (there IS, of course lol) to figure out in the future. 
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
        globalStates.current_map = maps.menu
        globalStates.current_commands = menu_commands
        
        
    ## 'Enter' command
    elif cmd == '\r' and ((cur_map[mapData.pos_x][mapData.pos_y+1] in mapData.friendlies) or
                          (cur_map[mapData.pos_x][mapData.pos_y-1] in mapData.friendlies)):
        speakableList(globalStates.current_map)


    ## DELETO THISO AMIGO LOLO #############################################################
    elif cmd == 'g':
        playerData.GOLD += 1


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
        clear()
        print(' > EXIT? [ENTER] TO CONFIRM')
        confirmation = getch()

        if bytes.decode(confirmation) == '\r':
            sys.exit(0)
        else:
            pass



####################################
#####        SAVE / LOAD       #####
####################################

def save_game():
    ## SAVE ORDER: xpos, ypos, current_map, pl_hp, pl_gold
    save_xpos = str(mapData.pos_x)
    save_ypos = str(mapData.pos_y)
    ####save_cur_map = str(globalStates)            HOW TF TO DO THIS LOL ###################
    save_cur_map = str(mapData.load_map_list.index(globalStates.return_map))
    save_hp = str(playerData.HP)
    save_gold = str(playerData.GOLD)

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
        ## SAVE ORDER: xpos, ypos, current_map, pl_hp, pl_gold
        openfile.truncate()
        openfile.write(save_xpos); openfile.write("\n")
        openfile.write(save_ypos); openfile.write("\n")
        openfile.write(save_cur_map); openfile.write("\n")
        openfile.write(save_hp); openfile.write("\n")
        openfile.write(save_gold); openfile.write("\n")

        print(f'\n  SAVED TO: {saveFiles[int(fileChoice)-2]} ')
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
            ## ORDER: xpos, ypos, current_map, pl_hp, pl_gold
            load_xpos = int(load_file.readline())
            load_ypos = int(load_file.readline())
            load_cur_map = int(load_file.readline())
            load_pl_hp = int(load_file.readline())
            load_pl_gold = int(load_file.readline())
            load_file.close()
                
            #World_Stats.pl_name = load_name.rstrip('\n')    #rstrip to remove 'n' so that player name isnt indented a line when they load the game
            mapData.pos_x = load_xpos
            mapData.pos_y = load_ypos
            globalStates.current_map = mapData.load_map_list[load_cur_map]
            playerData.HP = load_pl_hp
            playerData.GOLD = load_pl_gold
                
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

        if current_screen != maps.menu:
            overwrite_map(current_screen)
            ## Set current coordinates on the map to pl character
            current_screen[mapData.pos_x][mapData.pos_y] = 'X'
            print_map(current_screen)
        else:
            print(current_screen)

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