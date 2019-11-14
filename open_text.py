import os, sys, time
from msvcrt import getch

def clear():
    os.system('cls')

clear()

title_crawl = '''
     ##### #########   ####    #######   #######   ###  ###     ########## #########
    ###### #########  ######   ########  ########  ###  ###     ########## #########
    ##        ###    ###  ###  ###   ### ###   ### ###  ###     ###    ###    ###
    ######    ###    ###  ###  ###   ### ###   ### ###  ###     ###    ###    ###
    ######    ###    ########  ########  ########  ###  ###     ###    ###    ###
        ##    ###    ########  #######   #######   ###  ###     ###    ###    ###
    ######    ###    ###  ###  ###  ###  ###       ###  ####### ##########    ###
    #####     ###    ###  ###  ###   ### ###       ###  ####### ##########    ###
'''

for x in range (len(title_crawl)):
    print(title_crawl[x], end='')
    sys.stdout.flush()
    time.sleep(.005)

print('\n\t\t\t## SPACE COMBAT ADVENTURES ##\n\t\t\t        [press any key]')

getch()

clear()

print('''
        ====== WELCOME ======

    You are the pilot of a cargo 
    cruiser, a hefty ship made for 
    transportation and light combat.

    Alone without crew, it is up to 
    you to survive in deep space, 
    hunted by pirates, armies, and 
    fortune-seekers hoping to take
    your cargo off your hands.

           Godspeed, pilot.
''')

getch()
clear()

print('''
       ====== INSTRUCTIONS ======

    You are represented by 'X' on the map
    
    Three command stations on your ship
    are represented by the hash '#' char-
    acter. Press 'ENTER' to interact with 
    them and the number keys to select 
    options within them.

    You can save and load your game through
    the pilots command station in the cockpit.

          - WASD to move
          - ESC to exit
          - 1-5 num keys for selecting


''')

getch()