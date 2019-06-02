from maps import gamePlayMaps
from data import mapData

## THIS is the map change chunk that is run when players enter a door. 
## Obviously doing this much hardcoding of states and whatnot is not
## ideal, so figuring a way to store things in a list/dict/tuple would
## be good idea to figure out asap
def changeMap(scr, pl_inp):

    ## Map1 ##
    # to map2
    if scr == gamePlayMaps.map1 and pl_inp == 'd':
        mapData.pos_x = 2
        mapData.pos_y = 6
        return gamePlayMaps.map2
    
    ## Map 2 ##
    # to map1
    elif scr == gamePlayMaps.map2 and pl_inp == 'a':
        mapData.pos_x = 2
        mapData.pos_y = 7
        return gamePlayMaps.map1
    # to map3
    elif scr == gamePlayMaps.map2 and pl_inp == 's':
        mapData.pos_x = 1
        mapData.pos_y = 5
        return gamePlayMaps.map3
    
    ## Map3 ##
    # to map2
    elif scr == gamePlayMaps.map3 and pl_inp == 'w':
        mapData.pos_x = 4
        mapData.pos_y = 5
        return gamePlayMaps.map2
    # to secret room3
    elif scr == gamePlayMaps.map3 and pl_inp == 'a':
        mapData.pos_x = 1
        mapData.pos_y = 7
        return gamePlayMaps.map3secret
    # map3secret to return
    elif scr == gamePlayMaps.map3secret and pl_inp == 'd':
        mapData.pos_x = 1
        mapData.pos_y = 1
        return gamePlayMaps.map3