# testData.py - holds global data to be used by 
from maps import gamePlayMaps
from maps import staticMaps

class mapData():

    pos_x = 4
    pos_y = 5

    walkables = [' ']
    doors = ['[', ']', '=']
    walls = ['|', '#', 'M', '^', '_',  '-', '.', 'Q', '@', 'A', 'W', 'T', 'O', '\\', '/', '+', '`', '(', ')']

    enemies = ['@']
    friendlies = ['Q', 'M']
        
    # all maps are saved in order here for saving and loading purposes
    # You don't even need to keep track of the order here lol like literally
    # just make sure to add each map and you're good, the save and load 
    # systems get the indexes and load them properly for you, just
    # kick back and have a beer.
    load_map_list = [gamePlayMaps.map1,
                     gamePlayMaps.map2,
                     gamePlayMaps.map3,
                     gamePlayMaps.map3secret]



class playerData():
    
    HP = 25
    MAX_HP = 25

    GOLD = 15
    MISSILES = 5
    REPAIRKITS = 2

    CANNON_DAM = 1
    STATS = 0



class enemyClass(object): # to add later: 'attacks', a list of their attacks
    
    def __init__(self, rank, name, hp, basedam, face, messages):
        self.rank = rank
        self.name = name
        self.hp = hp
        self.basedam = basedam
        self.face = face
        self.messages = messages



class enemyData():

    names = ['Miguel', 'Barno', 'Spitz', 'Allejandro', 'Richards', 'Navaro', 'Jobim']
    ranks = ['Colonel', 'Commander', 'Pilot', 'Pirate', 'Captain', 'Corporal']

    current_enemy = None




