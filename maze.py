## custom libs
import config as cfg        ## config file
from field import Field
from player import Player
## std libs
import random               



class Maze():
    def __init__(self):
        self.width = cfg.MAZE_WIDTH
        self.height = cfg.MAZE_HEIGHT
        self.fields = []                             ## 2D array of 'Field' objects representing the fields of the maze

    # def __call__(self, *args, **kwds):
    #     return self.fields    

    def is_within_bounds(self, x:int, y:int) -> bool:
        '''
        Are coordinates within bounds.
        '''
        return 0 <= x < self.width and 0 <= y < self.height

    def generate_random_maze(self,seed_value: int=42):
        '''
        Generates the fields of the maze at random
        Paramters:
            seed_value int -- The seed used for generating the maze
        '''
        
        random.seed(seed_value)
        # print([random.randint(1, 10) for _ in range(5)])
        # random_boolean = random.choice([True, False])
        self._prims_maze_generation_algorithm(cfg.START_COORDS,cfg.END_COORDS)
    

    def __str__(self):
        return_value = ""
        for y in range(self.height):
            # return_value += "# "
            for x in range(self.width):
                return_value += f"{ '#' if self.fields[x][y].is_wall() else ' '}"
            return_value += "\n"
        return return_value

        
    def _prims_maze_generation_algorithm(self,start_position: set,end_position: set ) -> list:
        '''
        Generates the fields of the maze at random using prims algorithm.
        Paramters:
            start_position set -- The starting position of the algorithm. e.g. (0,0)
            end_position set -- The end position of the algorithm. e.g. (3,4) x=3, y=4
        Returns:
            self.fields list -- 2D list of Field objects.
        '''

        ## all fields are initially walls
        self.fields = [[Field(is_wall=True,x=x,y=y) for y in range(self.height)] for x in range(self.width )]

        DIRS = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        def is_in_bounds(x:int, y:int) -> bool:
            '''helper function'''
            return 0 <= x < self.width and 0 <= y < self.height

        def get_neighbors(x:int, y:int) -> list:
            '''Retuns a list of neighbors for the field with x,y positions'''
            nbs = []
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if is_in_bounds(nx, ny):
                    nbs.append((nx, ny))
            return nbs
        
        sx, sy = start_position                      ## tmp variables since the code got messy, start_x, start_y
        self.fields[sx][sy]._is_wall = False         ## mark the starting location as open
        wall_list = []                               ## list of all '(walkable_cell, wall)' pairs encountered in the algorithm

        for new_x, new_y in get_neighbors(sx, sy):
            if self.fields[new_x][new_y].is_wall():
                wall_list.append(((sx, sy), (new_x, new_y)))
        
        while wall_list: ## while wall_list is not empty

            cell, neighbor = random.choice(wall_list)
            wall_list.remove((cell, neighbor))

            x1, y1 = cell
            x2, y2 = neighbor
            wall_x, wall_y = (x1 + x2) // 2, (y1 + y2) // 2

            if self.fields[x2][y2].is_wall():
                self.fields[x2][y2]._is_wall = False
                self.fields[wall_x][wall_y]._is_wall = False
                for nnx, nny in get_neighbors(x2, y2):
                    if self.fields[nnx][nny].is_wall():
                        wall_list.append(((x2, y2), (nnx, nny)))

        # Ensure end point is open (bottom-right corner or closest odd cell)
        ex, ey = end_position
        if self.fields[ex][ey].is_wall():
            self.fields[ex][ey]._is_wall = False
            # Optionally: connect it to a neighbor if isolated
            for new_x, new_y in get_neighbors(ex, ey):
                if self.fields[new_x][new_y] == 0:
                    wall_x, wall_y = (ex + new_x) // 2, (ey + new_y) // 2
                    self.fields[wall_x][wall_y] = 0
                    break

        return self.fields
    
    
    def evaluate_fields(self,start:set, end:set):
        '''
        Sets the fintess of each field in the maze.
        The fitness of the end position is 0.
        Paramaters:
            start set -- e.g. (1,1)
            end set -- e.g. (1,1)
        '''
        stack = [end]                           ## nodes that need to be visited
        visited_positions = []                  ## nodes that have been visited
        dirs = Player.dirs                      ## directions the unit can traverse. down,right,up,left

        def get_neighboring_positions(pos: set):
            neighbors = []
            for direction in dirs:
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if self.is_within_bounds(new_pos[0],new_pos[1]) and not self.fields[new_pos[0]][new_pos[1]].is_wall():
                    neighbors.append(new_pos)
            return neighbors

        self.fields[end[0]][end[1]].fitness = 0

        while len(stack) > 0:
            current_pos = stack.pop(0)
            if current_pos in visited_positions:
                continue
            visited_positions.append(current_pos)

            neighboring_pos = get_neighboring_positions(current_pos)
            neighboring_pos = list(filter(lambda neighbor_position: neighbor_position not in visited_positions,neighboring_pos))
            
            ## update the fitness of the neighbors
            for pos in neighboring_pos:
                self.fields[pos[0]][pos[1]].fitness = min(self.fields[pos[0]][pos[1]].fitness, self.fields[current_pos[0]][current_pos[1]].fitness+1)
            
            ## append neighbors
            stack.extend( neighboring_pos )


    def print_with_path(self, path: list, start: set, end:set):
        """
        Prints the Maze object with a valid path.
        Paramaters:
            path list -- e.g. [(1,1),(1,2),...]
            start set -- e.g. (1,1) just a different sign
            end set -- e.g. (1,1) just a different sign
        """
        if path is None: 
            print("path is None!")
            return
        
        path_set = set(path)
        
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if (x, y) == start:
                    line += 'S'
                elif (x, y) == end:
                    line += 'E'
                elif (x, y) in path_set:
                    line += '1'
                else:
                    line += '#' if self.fields[x][y].is_wall() else ' '
            print(line)
        

    def print_field_fitnesses(self, start: set, end:set):
        """
        Prints the fields fitnesses.
        Paramaters:
            start set -- e.g. (1,1) just a different sign
            end set -- e.g. (1,1) just a different sign
        """
        
        ## the max number of digits in any fields fitness
        max_num_width = max([ len(str(self.fields[x][y].fitness) if not self.fields[x][y].is_wall() else "#" ) for y in range(self.height) for x in range(self.width )])
        
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if (x, y) == start:
                    line += 'S' * max_num_width
                elif (x, y) == end:
                    line += 'E' * max_num_width
                elif self.fields[x][y].is_wall():
                    line += '#' * max_num_width
                else:
                    line += f"{str(self.fields[x][y].fitness):>{max_num_width}}"
                line += ' '
            print(line)