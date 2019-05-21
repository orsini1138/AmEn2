# testData.py - holds global data to be used by 
from maps import maps

class mapData():

    pos_x = 1
    pos_y = 4

    walkables = [' ']
    doors = ['[', ']', '=']
    walls = ['|', '#', 'M', '^', '_',  '-', '.', 'Q', '@', 'A', 'W', 'T', 'O', '\\', '/', '+']

    enemies = []
    friendlies = ['Q', 'M']\
        
    # all maps are saved in order here for saving and loading purposes
    # You don't even need to keep track of the order here lol like literally
    # just make sure to add each map and you're good, the save and load 
    # systems get the indexes and load them properly for you, just
    # kick back and have a beer.
    load_map_list = [maps.map1,
                     maps.map2,
                     maps.map3,
                     maps.map3secret]



class playerData():
    
    HP = 5
    GOLD = 10


class enemyData():
    pass


class worldStates():
    x = 1




