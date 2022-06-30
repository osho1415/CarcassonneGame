''' file: carcassonne_tile.py
    author: Osho Sharma
    course: CSC120
    This file defines CarcassoneTile class which represents an 
    tile object in the carcassonne project.
'''

class CarcassonneTile: 
    '''
        The CarcassonneTile class represents an tile object in the carcassonne project.
        Each tile has five private attributes which are :
            1) name : (str), represents the name of the tile.
            2) roads: (list), a list containing list, with each list representing a 
            different road, set contains to and from edges. 
            3) cities: (list), a list containing list, with each list representing a 
            different city, a set contains all the edges covered by the city. 
            4) edge: a dictionary, with edges as keys and terrains as values.
            5) direcs : a dictionary with int as keys and str as values, converts integers to 
            their respective direction. 
        Directions represented by integers as following: 
            N = 0 , E = 1, S = 2, W = 3
        The class has the following methods: 
            1) edge_info(self,road,cities): creates and returns a dict to self._edge, upon reading data from 
            self._raods and self._cities. 
            2) get_edge(side): describes the terrain on the given edge of the tile
            3) edge_has_city/road(side): returns True/False based on whether the given edge has a city/road.
            4) has_crossroads: returns True/False based on whether the tile has crossroads.
            5) road_get_connection(side): returns the other edge to which the road is connected. 
            6) city_connects(sideA,sideB): returns True if the same city on both the given edges
            7) rotate(): returns a new object by rotating the features of the parent object by 90 degress clockwise.
        The constructor can be called with name (str), roads (list of lists) and cities (list of list)
    '''

    def __init__(self, name, roads, cities): 
        ''' Creates an object that represents a tile, which can be placed on a map. 
            Parameters: self, name(str), road/cities(list~ 2D arrays)
            Returns: None 
        '''
        self._name = name 
        self._roads = roads
        self._cities = cities
        self._edge = self.edge_info(self._roads,self._cities) 
        self._edge_to_direc = {0: 'N', 1: 'E', 2: 'S', 3: 'W', -1: 'C'}
    
    def edge_info(self,roads,cities): 
        ''' Reads values from roads and cities attributes and assigns
            terrains to each edge. Returns the dictionary to self._edge attribute.
            Parameters: roads, cities 
            Returns: edge (dict)
        '''
        edge = {0:'', 1: '', 2: '', 3: '', -1: ''}

        # reads in data for different roads.
        for elems in roads: 
            # roads can have only a to and from edge.
            assert len(elems) == 2, f'{elems} need 2 edges for road.'
            for direc in elems: 
                # for -1,  only possible option is crossroad. 
                if direc != -1: 
                    edge[direc] = 'grass+road'
                if direc == -1 : 
                    edge[direc] = 'crossroad'
        
        # reads in data for different cities. 
        for elems in cities: 
            # cities can have atmost 4 edges 
            assert len(elems) <=  4, f'{elems} at most 4 edges for city.'

            for direc in elems: 
                # center not an edge for a city. 
                assert direc != -1, f'cannot have -1 as edge for city.'
                edge[direc] = 'city'
        
        # assigns grass to all the remaining edges. 
        for direc in edge: 
            if direc != -1 and edge[direc] == '': 
                edge[direc] = 'grass'
        
        return edge
    
    def get_edge(self,side):
        ''' Returns the terrain present at the given edge. 
            Parameters: self, side(int)
            Returns: self._edge[side] (str)
        ''' 
        return self._edge[side]
    
    def edge_has_road(self,side): 
        ''' Returns true/false based on if an edge has road on it.
            Parameters: self, side(int)
            Returns: True/False (bool)
        '''
        if self._edge[side] == 'grass+road':
            return True
        return False 
    
    def edge_has_city(self,side): 
        ''' Returns True/False based on whether if an edge has city on it. 
            Parameters: self, side(int)
            Returns: True/False
        '''
        if self._edge[side] == 'city': 
            return True
        return False 
    
    def has_crossroads(self):
        ''' Returns True/False based on whether the tile has crossroads. 
            Parameters: self
            Returns: True/False(bool)
        ''' 
        if self._edge[-1] == 'crossroad':
            return True 
        return False 
    
    def road_get_connection(self,from_side): 
        ''' Gives the other edge connected by road when passed an edge.
            Parameters: self, from_side(int)
            Returns: road[0] (int)
        '''
        for elem in self._roads: 
            road = elem.copy() 
            if from_side in road: 
                road.remove(from_side)
                return road[0]
    
    def city_connects(self,sideA, sideB): 
        ''' Returns True/False based on whether both edges has city on them.
            Paramters: self, sideA/sideB (int)
            Returns: True/False (bool)
        '''
        for elems in self._cities: 
            if sideA in elems and sideB in elems: 
                return True 
        return False 

    def rotate(self): 
        ''' Reeturns a new object by rotating the features of the 
            parent object by 90 degress clockwise.
            Parameters: self
            Returns: CarcassonneTile object
        '''
        new_roads = list() 
        new_cities = list()

        for elems in self._roads: 
            new_road = list() 

            for direcs in elems: 
                # if edge not -1/3
                if direcs != -1 and direcs != 3: 
                    new_road.append(direcs+1)
                if direcs == 3: 
                    new_road.append(0)
                if direcs == -1: 
                    new_road.append(-1)
            # adding new attributes for each road in tile.
            new_roads.append(new_road)
        
        for elems in self._cities: 
            new_city = list() 

            for direcs in elems: 
                # check if edge is not 3
                if direcs != 3: 
                    new_city.append(direcs+1)
                else: 
                    new_city.append(0)
            # adding new attributes for all the cities in tile
            new_cities.append(new_city)

        return CarcassonneTile(self._name,new_roads,new_cities)

# intializes the various tiles, with their major features encoded in the attributes of each object.
tile01 = CarcassonneTile('tile01',[[1,3]],[[0]])
tile02 = CarcassonneTile('tile02',[],[[1,0,3]])
tile03 = CarcassonneTile('tile03',[[0,-1],[1,-1],[2,-1],[3,-1]],[])
tile04 = CarcassonneTile('tile04',[[2,1]],[[0]])
tile05 = CarcassonneTile('tile05',[],[[0,1,2,3]])
tile06 = CarcassonneTile('tile06',[[0,2]],[])
tile07 = CarcassonneTile('tile07',[],[[3],[1]])
tile08 = CarcassonneTile('tile08',[],[[1,3]])
tile09 = CarcassonneTile('tile09',[],[[0,1]])
tile10 = CarcassonneTile('tile10',[[1,-1],[2,-1],[3,-1]],[])
tile11 = CarcassonneTile('tile11',[[2,1]],[[0,3]])
tile12 = CarcassonneTile('tile12',[[3,2]],[[0]])
tile13 = CarcassonneTile('tile13',[[1,-1],[2,-1],[3,-1]],[[0]])
tile14 = CarcassonneTile('tile14',[],[[0],[1]])
tile15 = CarcassonneTile('tile15',[[3,2]],[])
tile16 = CarcassonneTile('tile16',[],[[0]])
