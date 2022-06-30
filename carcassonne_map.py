''' file: carcassonne_map.py
    author: Osho Sharma
    course: CSC120
    This file defines CarcassoneMap class which represents a 
    map object which can hold tiles from the CarcassonneTile class.
'''
import carcassonne_tile

class CarcassonneMap: 
    ''' This class represents a map object which can hold tiles from the CarcassonneTile class. 
        An object of this class has three private attributes: 
            1) self._map: represents a dictionary which contains all the tiles placed as values and their coordinates as keys.
                initialized with tile01 at the (0,0)
            2) self._adj: a dictionary containing integers representing directions as keys and the change in coordinates as values. 
                (0 = N , 1 = E , 2 = S , 3 = W )
            3) self._map_borders: a set of all the possible coordinates where tiles can be added in future.
            4) self._adj_side = a dictionary containing integers representing edges as keys and integers representing adjacent edge 
                in other tile as the value.  
        The constructor can be called without passing any parameters, it creates a map object with tile01 at (0,0) coordinate. 
        This class has following methods: 
            1) get_all_coords(): returns a set of all the coordinates which have tiles in them. 
            2) find_map_border(): returns a set of all the coordinates which can have tiles in future. 
            3) get(x,y): returns the tile at given x,y coordinates, if no tile present returns None 
            4) add(x,y,tile,confirm,tryOnly): takes in x,y coordinates and returns True if a tile can be added, else returns False
            adds a tile based on values of Confirm, tryOnly. 
            5) adj_tile_check(x,y,tile): checks all the adjacent coordinates for (x,y) to see if a tile can be added to (x,y), returns true if yes, 
            else returns false. 
            6) trace_road_one_direction(x,y,side): Follows the road and records all the tiles and edges until it ends, or loops.
            7) trace_road(x,y,side): Follows the road in both direction and records all the tiles and edges until it ends, or loops at both side.
            8) trace_city(x,y,side): Records all the edges of a connected city along with all the tiles this city is present on.
    '''
    def __init__(self): 
        ''' Creates a map object, while defining the various private attributes for the object. 
            Initializes the self._map attribute with tile01 at the (0,0)
            Parameters: self 
            Returns : None 
        '''
        self._map = {(0,0): carcassonne_tile.tile01}
        self._adj = {0:[0,1], 2 :[0,-1], 1:[1,0], 3:[-1,0]}
        self._adj_side = {0:2, 2:0, 1:3, 3:1}
        self._map_borders = self.find_map_border()
    

    def get_all_coords(self): 
        ''' This function returns a set of all the coordinates which have tiles in them. 
            Parameters: self 
            Returns: coords_set(set)
        '''
        coords_set = set()
        # gets all the coordinates present in the map. 
        for coords in sorted(self._map):
            coords_set.add(coords)

        return coords_set
    
    def find_map_border(self):
        ''' This function returns a set of all the coordinates which can have tiles in future.
            Parameters: self 
            Returns: coords_set (set)
        '''
        coords_set = set() 

        for coords in sorted(self._map): 

            for elems in self._adj: 
                # pos_cod are all the adjacent coordinate for particular (x,y)
                pos_cod = (coords[0]+self._adj[elems][0],\
                coords[1]+self._adj[elems][1])

                # checks if the coordinate doesn't have a tile in it. 
                if pos_cod not in self._map: 
                    coords_set.add(pos_cod)

        return coords_set 

    def get(self,x,y): 
        ''' This function returns the tile present at given (x,y), if none present 
            returns None.
            Parameters: self, x/y (int)
            Returns: CarcassonneTile object/ None 
        '''
        if (x,y) in self._map: 
            return self._map[(x,y)]
        return None 

    def add(self,x,y,tile,confirm = True, tryOnly = False):
        ''' This function takes in x,y coordinates and returns True if a tile can be added,
            else returns False adds a tile based on values of Confirm, tryOnly.
            1) Confirm: True ~ do error check, False ~ no error check 
            2) TryOnly: True ~ don't add tile, False ~ add tile
            Parameters: self, x/y (int), tile (CarcassonneTile), confirm/tryOnly (bool)
            Returns: True/ False 
        '''
        # confirm allows error checking 
        if confirm:  

            # checks if coordinates in map borders but not occupied by any tile.
            if (x,y) in self._map_borders and (x,y) not in self._map:

                # checks compatibility with adjacent tiles. 
                tile_check = self.adj_tile_check(tile,x,y)
                if tile_check:

                    # adds tile only when tryOnly is false
                    if not tryOnly: 
                        self._map[(x,y)] = tile 
                        # extends the map border attributes based on the new added tile. 
                        self._map_borders = self.find_map_border()
                    return True

                else: 
                    return False 

            else: 
                return False
        # if confirm false and tryOnly both false, then adds the tile without errorchecking.
        if not tryOnly: 
            self._map[(x,y)] = tile
            # extends the map border attributes based on the new added tile. 
            self._map_borders = self.find_map_border()

            return True
                    
    
    def adj_tile_check(self,tile,x,y): 
        ''' This function checks all the adjacent coordinates for (x,y) to see if a tile can be added to (x,y), 
            returns true if yes, else returns false.
            Parameters: self, tile(CarcassonneTile), x/y (int)
            Returns: True/False
        '''
        check = True

        for elems in self._adj:
            # checks all possible adjacent coordinates.
            pos_cod = (x + self._adj[elems][0], y + self._adj[elems][1]) 
            # checks if a tile present at that coordinate.
            if pos_cod in self._map:  

                if self._adj[elems][0] == 0: 
                    adj_edge = elems+2*(self._adj[elems][1])

                    # checks if the adjacent sides of the tiles are not same (N-S) 
                    if tile.get_edge(elems) != \
                        self._map[pos_cod].get_edge(adj_edge):
                        check = False

                elif self._adj[elems][1] == 0: 
                    adj_edge = elems + 2*(self._adj[elems][0])

                    # checks if the adjacent sides of the tiles are not same (E-W)
                    if tile.get_edge(elems) != \
                        self._map[pos_cod].get_edge(adj_edge):
                        check = False
        return check      

    def trace_road_one_direction(self,x,y,side): 
        ''' Follows a road from the given tile and side and record all the tiles,
            along the edges it follows till the road ends, or loops.
            Parameters: self, x/y/side(int)
            Returns: retval (list)
        ''' 
        retval = []
        c_tile, c_side = (x,y), side 

        while True: 
            # avoids KeyError when being parsed from road_trace() 
            if side == -1: 
                break 

            # finds the coordinate of adjacent tile
            n_tile = (c_tile[0] + self._adj[c_side][0],\
                c_tile[1] + self._adj[c_side][1])

            # checks if the adjacent tile exists, breaks loop if it doesn't
            if n_tile not in self._map: 
                break 
            
            # moves into next tile, updates c_side / c_tile
            c_tile = n_tile 
            c_side = self._adj_side[c_side]
            
            # gets the other edge of the road. 
            n_side = self._map[c_tile].road_get_connection(c_side)

            # adds the details of the tiles in an array.
            retval.append((c_tile[0],c_tile[1],c_side,n_side))

            # breaks if we looped back to beginning tile or crossroad found.
            if c_tile == (x,y): 
                break 
            elif n_side == -1: 
                break 
            else:
                c_side = n_side
            
        return retval 
        
    def trace_road(self,x,y,side): 
        ''' Calls upon trace_road_one_direction function 
            to get the road's status on both side.
            Parameters: self, x/y/side (int)
            Return: retval (list)
            
        '''
        # gets the other edge of the road
        oth_side = self._map[(x,y)].road_get_connection(side)

        # gets the status of the road on both sides of starting point
        b_cur = self.trace_road_one_direction(x,y,oth_side)
        f_cur = self.trace_road_one_direction(x,y,side)
        upd_b_cur = list()

        # updates the upd_b_cur to represent status of the road from behind to the starting point
        for elem in b_cur: 
            upd_b_cur.append((elem[0],elem[1],elem[3],elem[2]))
        upd_b_cur = upd_b_cur [::-1]

        # checks if the road has a loop 
        if len(upd_b_cur) != 0 and len(f_cur) != 0: 
            if upd_b_cur[0] == f_cur[-1]: 
                return f_cur 
        
        retval = upd_b_cur + [(x,y,oth_side,side)] + f_cur 
        return retval 

    def trace_city(self,x,y,side): 
        ''' Look at all the edges of the of a city in all the tiles it is present
            Record a tuple, with bool telling if city is complete and then a set of tuples
            giving (x,y,edge) for all the edge in a given tile. 
            Parameters: self, x/y/side(int)
            Returns: tuple (bool,set)
        '''         
        city = {(x,y,side)}

        city_complete = True
        keep_searching = True 

        while keep_searching: 
            keep_searching = False
            dup_city = list(city)

            for loc in dup_city:

                # checks for all the other edges of the current tile.
                for s in range(4): 

                    # checks if the edge not the same as given, 
                    # and same city at that edge.
                    if s != loc[-1] and \
                    self._map[(loc[0],loc[1])].city_connects(loc[-1],s):

                        # checks if the other edge of the tile not in city set.
                        if (loc[0],loc[1],s) not in city: 

                            # adds the new edge, with tile to city. 
                            city.add((loc[0],loc[1],s))
                            keep_searching = True 
                
                # neighboring tile at that side
                adj_tile = (loc[0]+self._adj[loc[-1]][0],\
                            loc[1]+self._adj[loc[-1]][1])
                
                # check if the neighbor space is not a recorded tile in map.
                if adj_tile not in self._map: 
                    city_complete = False 

                else:  
                    new_loc = (adj_tile[0],adj_tile[1],\
                        self._adj_side[loc[-1]])

                    # checks if the given elem not in city
                    if new_loc not in city: 
                        city.add(new_loc)
                        keep_searching = True 

        return (city_complete,city)

        
