## std libs
import random
import copy

## custom libs
from AStar import astar,manhattan_distance,euclidean_distance

class Player:
    '''
    Unit in the population of the genetic algorithm
    '''
    fitness = 0                             ## The lower the better
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]      ## directions the unit can traverse. down,right,up,left
    can_walk = True                         ## can the player walk or is he stuck

    def __init__(self, start: set, end: set, maze, best_path: list):
        self.movement_instructions = []     ## list of directions e.g. [(0,1),(1,0),...] all the way to the last position
        self.path = [start]                 ## the path this player took. e.g [start,(2,3),(3,3),...,end]
        self.maze = maze                    ## the Maze object
        self.end = end                      ## end coordinates
        # self.color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
        self.best_path = best_path                  ## best path returned by the A* algorithm
        # self.maxdistance = len(best_path)           ## 
        # self.maxdistance = manhattan(init[1],init[0],end[1],end[0])

    def __str__(self):
        return str(self.path)+" Fitness: "+str(self.fitness)


    def _get_new_pos(self, d: set, pos: set=None):
        """
        Returns the new position.
        Paramaters:
            d set -- direction in which to move
            pos set -- position from which to move in said direction. If none is given then take the last position in the path as the position
        """
        if pos is not None and len(pos) >= 2 and isinstance(pos[0],int) and isinstance(pos[1],int):
            return pos[0]+d[0], pos[1]+d[1]
        
        return self.path[-1][0]+d[0], self.path[-1][1]+d[1]
        

    def _is_valid_direction(self, d, pos: set=None, allow_backtracking: bool=False) -> bool:
        '''
        The direction must lead to field within bounds that is not a wall and has not been visited yet.
        Paramaters:
            pos set -- postiion from which to find the valid directions e.g. (5,3) 
            allow_backtracking bool -- are directions that lead onto a field that's already in the path allowed
        '''
        newpos = self._get_new_pos(d,pos=pos)
        is_valid = self.maze.is_within_bounds(newpos[0],newpos[1]) and self.maze.fields[newpos[0]][newpos[1]].is_wall() == False    
        if not allow_backtracking:
            is_valid = is_valid and newpos not in self.path
        return is_valid 


    def _get_valid_dirs_for_position(self,pos: set, allow_backtracking: bool=False) -> list:
        '''
        Paramaters:
            pos set -- postiion from which to find the valid directions e.g. (5,3) 
            allow_backtracking bool -- are directions that lead onto a field that's already in the path allowed
        Returns:
            valid_dirs list -- list of directions e.g. [(1,0),(0,-1),...]
        '''
        valid_dirs = []
        for d in self.dirs:
            if self._is_valid_direction(d, pos= pos, allow_backtracking= allow_backtracking):
                valid_dirs.append(d)
        return valid_dirs

    
    def step(self, direction: set=None):
        '''
        Step into a radom direction.
        Player does not move onto a field that he has been to and he does not step into a wall.
        If no direction is specified then pick a random one.
        Paramaters:
            d set -- direction e.g. (1,0) or (0,-1)
        '''
        if direction is None:
            valid_directions = list(filter(lambda d: self._is_valid_direction(d),self.dirs))

            if len(valid_directions) > 0:
                direction = random.choice(valid_directions)
    
        if direction is not None and self._is_valid_direction(direction):
            self.movement_instructions.append(direction)
            new_position = self._get_new_pos(direction)
            self.current_position = new_position
            self.path.append(new_position)
            
            if self.path[-1] == self.end:
                self.can_walk = False
                self.win = True
        else:
            self.can_walk = False        ## this player has reached a dead end


    def walk(self, movement_instructions_stack: list=None):
        '''
        Player moves in random direction until he hits a dead end or the exit.
        Player does not move onto a field that he has been to and he does not step into a wall.
        If 'movement_instructions_stack' is given then:
            Finds first valid direction for player in the given directions list and steps there. 
            If no valid direction is found then it goes in a random direction.
        Paramaters:
            movement_instructions_stack list -- list of directions e.g. [(1,0),...]
        '''
        if movement_instructions_stack is None or len(movement_instructions_stack) <= 0:
            ## walk at random
            while self.can_walk:
                self.step()
            return 
        
        while self.can_walk:
            
            first_valid_direction, id = self._find_first_valid_direction(movement_instructions_stack)
            
            ## if no valid direction is found then pick one at random
            if first_valid_direction is None:
                valid_directions = list(filter(lambda d: self._is_valid_direction(d),self.dirs))
                if len(valid_directions) > 0:
                    first_valid_direction = random.choice(valid_directions)
            
            if id is not None:
                ## remove the direction from 'movement_instructions_stack'
                movement_instructions_stack.pop(id)

            self.step(first_valid_direction)
            
            # if first_valid_direction is not None:
            #     ## step
            #     self.movement_instructions.append(first_valid_direction)
            #     new_position = self._get_new_pos(first_valid_direction)
            #     self.current_position = new_position
            #     self.path.append(new_position)
            #     if self.path[-1] == self.end:
            #         self.canwalk = False
            #         self.win = True
            # else:
            #     self.canwalk = False        ## this player has reached a dead end

    def evaluate(self, fields: list = None):
        '''
        Moves the player and then updates the players fitness value.
        Returns:
            fitness -- the updated fitness value
            fields 2D list -- fields from the maze object
        '''
        self.walk()                     ## get a solution
        last_position = self.path[-1]
        

        ## evaluate them in a simple manner
        ##! MANNHATTAN DISTANCE
        # self.fitness = manhattan_distance(last_position,self.end) 
        
        ##! EUCLIDIAN DISTANCE
        self.fitness = euclidean_distance(last_position,self.end) 

        ## EUCLIDEAN DISTANCE OF ALL ELEMENTS IN THE PATH
        # new_fitness = 0
        # for position in self.path:
        #     new_fitness += euclidean_distance(position,self.end)
        # self.fitness = new_fitness
        
        ## 3rd OPTION OF USING THE FITNESS OF THE FIELDS
        ##! try using the fields fitness
        # if fields is not None:
        #     self.fitness = fields[last_position[0]][last_position[1]].fitness
        # else:
        #     self.fitness = -99 

        return self.fitness



    def crossover_movement_instruction_stack_method(self, partner):
        '''
        Single point crossover where the child gets a the 1st part of its path from one parent and the 2nd part is then created by trying to use the movement instructions from the other parent.
        Paramaters:
            partner Player -- 
        Returns:
            Player -- new Player object representing the cross over child
        '''
        better_parent = min(self,partner,key=lambda x: x.fitness)                 ## find the better parent
        other_parent  = max(self,partner,key=lambda x: x.fitness)                 
        
        crossover_index = random.random() * min(len(better_parent.path),len(other_parent.path))  ## find the crossover point
        crossover_index = max(crossover_index,1) ## must contain the start
        crossover_index = int(crossover_index)

        child1 = Player(start= better_parent.path[0], end= better_parent.end, maze= better_parent.maze, best_path= better_parent.best_path)
        child1.path = better_parent.path[:crossover_index]
        child1.movement_instructions = better_parent.movement_instructions[:crossover_index-1]
        
        ## use the other parents movement instructions as a stack to repair the path (aka. find a path to the end)
        remaining_movement_instructions =  other_parent.movement_instructions[:].copy()
        child1.walk(remaining_movement_instructions)

        ## do the same for the second child
        child2 = Player(start= other_parent.path[0], end= other_parent.end, maze= other_parent.maze, best_path= other_parent.best_path)
        child2.path = other_parent.path[:crossover_index]
        child2.movement_instructions = other_parent.movement_instructions[:crossover_index-1]
        remaining_movement_instructions = better_parent.movement_instructions[:].copy()
        child2.walk(remaining_movement_instructions)

        return child1,child2


    def crossover_random(self,partner):
        '''
        Single point crossover where the child gets a the 1st part of its path from one parent and the 2nd part is created at random.
        Paramaters:
            partner Player -- 
        Returns:
            Player -- new Player object representing the cross over child
        '''
        
        better_parent = min(self,partner,key=lambda x: x.fitness)                 ## find the better parent
        other_parent  = max(self,partner,key=lambda x: x.fitness)                 
        
        crossover_index = random.random() * min(len(better_parent.path),len(other_parent.path))  ## find the crossover point
        crossover_index = max(crossover_index,1) ## must contain the start
        crossover_index = int(crossover_index)

        child1 = Player(start= better_parent.path[0], end= better_parent.end, maze= better_parent.maze, best_path= better_parent.best_path)
        child1.path = better_parent.path[:crossover_index]
        child1.movement_instructions = better_parent.movement_instructions[:crossover_index-1]
        
        ## use the other parents movement instructions as a stack to repair the path (aka. find a path to the end)
        remaining_movement_instructions =  other_parent.movement_instructions[:].copy()
        child1.walk()

        ## do the same for the second child
        child2 = Player(start= other_parent.path[0], end= other_parent.end, maze= other_parent.maze, best_path= other_parent.best_path)
        child2.path = other_parent.path[:crossover_index]
        child2.movement_instructions = other_parent.movement_instructions[:crossover_index-1]
        remaining_movement_instructions = better_parent.movement_instructions[:].copy()
        child2.walk()

        return child1,child2




    def _find_first_valid_direction(self,movement_instructions_stack: list):
        '''
        Finds first valid direction for player in the given directions list. 
        If no valid direction is found then None is returned.
        Paramaters:
            movement_instructions_stack list -- list of directions e.g. [(1,0),...]
        Returns:
            direction set -- e.g. (1,0) or (0,-1)
            id int -- the id of the direction in the list
        '''
        id = 0
        while id < len(movement_instructions_stack):
            if self._is_valid_direction(movement_instructions_stack[id]):
                return movement_instructions_stack[id], id
            id += 1
        return None,None
        

    def mutate(self):
        '''
        Performs mutation on the given player by picking a new path to go down.
        '''
        
        mutatable_positions = []      ## position that are junctions with an unexplored path. e.g. [(3,(5,5)),(8,(9,4))] the first is the id in the path and the second is the position in the maze
        
        ## find all positions that we can perform a mutation on
        for id,pos in enumerate(self.path):
            tmp = len(self._get_valid_dirs_for_position(pos= pos))
            if len(self._get_valid_dirs_for_position(pos= pos)) >= 1:
                mutatable_positions.append((id,pos))
        
        if len(mutatable_positions) <= 0:
            return 

        ## mutation position
        id,pos = random.choice(mutatable_positions)

        old_move = self.movement_instructions[id]
        valid_dirs = self._get_valid_dirs_for_position(pos= pos)
        valid_dirs = list(filter(lambda d: d != old_move,valid_dirs))
        new_move = random.choice(valid_dirs) 

        ## cut the path 
        self.path = self.path[:max(id,1)]           
        self.movement_instructions = self.movement_instructions[:max(id-1,0)]

        ## set the next move 
        remaining_movement_instructions = [new_move]
        self.can_walk = True
        self.walk(remaining_movement_instructions)
        




