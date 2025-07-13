class Field():

    def __init__(self,is_wall: bool, x: int, y: int, fitness = 999999999) :
        self._is_wall = is_wall              ## is this a walkable field
        self.position = (x,y)                ## set representing the 'x' and 'y' position of the field on the maze. (0,0) is the top left corner of the maze
        self.fitness = fitness

    def __str__(self):
        # return f"Field({self.position[0]},{self.position[1]})=>is_wall={self.is_wall()}"
        return "1" if self.is_wall() else "0"

    def is_wall(self) -> bool:
        '''
        Is this field a wall. (The player is NOT allowed to be on this field)
        '''
        return self._is_wall

    def __call__(self, *args, **kwds) -> bool:
        '''
        Is this field a wall. (The player is NOT allowed to be on this field)
        '''
        return self.is_wall()

    