## std libs
import heapq
import math

## custom libs
from field import Field
# from maze import Maze


def manhattan_distance(a: tuple, b: tuple):
    '''
    Manhattan distance since it's the simplest
    Paramaters: 
        a tuple -- (x,y)
        b tuple -- (x,y)
    Returns:
        int -- manhattan distance
    '''
    a = tuple(a)
    b = tuple(b)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean_distance(a: tuple, b: tuple):
    '''
    Euclidean distance between two 2D points.
    Parameters: 
        a tuple -- (x, y)
        b tuple -- (x, y)
    Returns:
        float -- Euclidean distance
    '''
    a = tuple(a)
    b = tuple(b)
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def astar(maze, start: set, end: set) -> list:
    '''
    STD A* path finding algorithm.
    Params:
        maze Maze -- Maze object with valid 'fields' field
        start: set -- like (0,0)
        end: set -- like (3,4)
    Returns:
        path list -- Path like [start,(1,2),(2,2),...,end]
    '''
    height = maze.height
    width = maze.width
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    heuristic = manhattan_distance                  ## what heuristic is used for scoring
    came_from = {}                                  ## pointer backwards 
    g_score = {start: 0}                            ##
    f_score = {start: heuristic(start, end)}        ##
    DIRECTIONS = [(-1,0),(1,0),(0,-1),(0,1)]        ## directions a player can move (left,up,right,down)

    while open_set:
        _, current_field = heapq.heappop(open_set)

        if current_field == end:
            # Reconstruct path
            path = []
            while current_field in came_from:
                path.append(current_field)
                current_field = came_from[current_field]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in DIRECTIONS:
            
            current_neighbor = (current_field[0]+dx, current_field[1]+dy)
            x, y = current_neighbor
            if 0 <= x < width and 0 <= y < height and maze.fields[x][y].is_wall() == False:
            
                tentative_g_score = g_score[current_field] + 1
                if current_neighbor not in g_score or tentative_g_score < g_score[current_neighbor]:
                    came_from[current_neighbor] = current_field
                    g_score[current_neighbor] = tentative_g_score
                    f_score[current_neighbor] = tentative_g_score + heuristic(current_neighbor, end)
                    heapq.heappush(open_set, (f_score[current_neighbor], current_neighbor))
    
    return None  # No path found



