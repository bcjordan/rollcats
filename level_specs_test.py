#!/usr/bin/python

global lvl
#lvl = None

class Level():
    def __init__(self, *args):
        self.ground_height_field = args[0]
        self.scenery = []#{}
        self.drawbridges = []
        
    def add_scenery(self, image_url, position,  z_index, orientation):
        #self.scenery[len(self.scenery)] = {"img_url":image_url, "pos": position, "orientation": orientation}
        self.scenery.append({"img_url":image_url, "pos": position, "z_index": z_index, "orientation": orientation})
        
    def add_drawbridge(self, image_urls, positions, z_indices, fallsLeft, orientations):
        self.drawbridges.append(({"img_url":image_urls[0], "pos":positions[0], "z_index":z_indices[0], "fallsLeft":fallsLeft, "orientation":orientations[0]}, 
                                 {"img_url":image_urls[1], "pos":positions[1], "z_index":z_indices[1], "orientation":orientations[1]}))


class Levels():
    """docstring for Level"""
    def __init__(self):
        self._list = []
    
    def add_level(self, *args):
        tmp = Level([el for el in args])
        self._list.append(tmp)
        
    def display(self, target):
        if target == "ground_height_field":
            print "Ground height-fields:"
            print ""
            for index, each in enumerate(self._list):
                print "level", repr(index + 1) + ":", each.ground_height_field
            print ""
            

        if target == "scenery":
            print "Scenery list:"
            print ""
            for index, each in enumerate(self._list):
                if each.scenery:
                    print "level", repr(index+1)+":", each.scenery
                    
    def return_height_fields(self, level_num): return self._list[level_num].ground_height_field
            
    def return_scenery(self, level_num): return self._list[level_num].scenery
    
    def return_bridges(self, level_num): return self._list[level_num].drawbridges

    
def initializeLevels():
    """docstring for main"""
    global lvl
    lvl = Levels()
#    print "Hello"
    
    # Level 1
    lvl.add_level((0, 275), (270, 275), (735, 450), (735, 275), (1200, 275))
    #lvl._list[0].add_scenery("bush1.png", (50.0, 50.0), 2, None)
    lvl._list[0].add_scenery("cloud1.png", (450.0, 450.0), 1, None) # should randomize these
    lvl._list[0].add_scenery("cloud1.png", (950.0, 680.0), 1, None)
        
    # Level 2
    lvl.add_level((0, 275), (270, 275), (465,380), (465, -100), (550, -100), (550, 410), (650, 410), (650, -100), (735, -100), (735, 380), (930, 275), (1200, 275))
    lvl._list[1].add_scenery("cloud1.png", (450.0, 450.0), 1, None) # should randomize these
    lvl._list[1].add_scenery("cloud1.png", (950.0, 680.0), 1, None)
    
    # Level 3
    lvl.add_level((0, 170), (468, 170), (468, -100), (754, -100), (754, 170), (1200, 170))
    lvl._list[2].add_scenery("cloud1.png", (450.0, 450.0), 1, None) # should randomize these
    lvl._list[2].add_scenery("cloud1.png", (950.0, 680.0), 1, None)
    lvl._list[2].add_drawbridge(  ("Drawbridge.png","Switch.png"), ((740,185),(800,165)), (1,1), True, (None,None) ) 
    
    # Level 4
    lvl.add_level((0, 170), (422, 170), (754, 170), (802, 170), (910, 280), (910, 170), (1200, 170))    
    lvl._list[3].add_scenery("cloud1.png", (450.0, 450.0), 1, None) # should randomize these
    lvl._list[3].add_scenery("cloud1.png", (950.0, 680.0), 1, None)
    lvl._list[3].add_drawbridge(  ("Drawbridge.png","Switch.png"), ((754,180),(1800,165)), (1,1), True, (None,None) ) 
    
    # Level 5
    lvl.add_level((0, 275), (465, 275), (465, 20), (760, 20), (760, 275), (1200, 275))
    lvl._list[4].add_scenery("cloud1.png", (450.0, 450.0), 1, None) # should randomize these
    lvl._list[4].add_scenery("cloud1.png", (950.0, 680.0), 1, None)
    
    
    #print "\ntesting return functions:\n"
    #for ind, each in enumerate(lvl._list):
    #    print "level", repr(ind+1)+":"
    #    if each.ground_height_field: print each.ground_height_field
    #    if each.scenery: print each.scenery
    return lvl

if __name__ == '__main__':
    initializeLevels()
