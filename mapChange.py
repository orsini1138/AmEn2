from maps import maps
from testData import mapData

## THIS is the map change chunk that is run when players enter a door. 
## Obviously doing this much hardcoding of states and whatnot is not
## ideal, so figuring a way to store things in a list/dict/tuple would
## be good idea to figure out asap
def changeMap(scr, pl_inp):

    # mapList = [maps.map1, maps.map2]

    ## Map1 ##
    # to map2
    if scr == maps.map1 and pl_inp == 'w':
        mapData.pos_x = 2
        mapData.pos_y = 1
        return maps.map2
    
    ## Map 2 ##
    # to map1
    elif scr == maps.map2 and pl_inp == 'a':
        mapData.pos_x = 6
        mapData.pos_y = 14
        return maps.map1
    # to map3
    elif scr == maps.map2 and pl_inp == 's':
        mapData.pos_x = 1
        mapData.pos_y = 5
        return maps.map3
    
    ## Map3 ##
    # to map2
    elif scr == maps.map3 and pl_inp == 'w':
        mapData.pos_x = 4
        mapData.pos_y = 5
        return maps.map2
    # to secret room3
    elif scr == maps.map3 and pl_inp == 'a':
        mapData.pos_x = 1
        mapData.pos_y = 7
        return maps.map3secret
    # map3secret to return
    elif scr == maps.map3secret and pl_inp == 'd':
        mapData.pos_x = 1
        mapData.pos_y = 1
        return maps.map3