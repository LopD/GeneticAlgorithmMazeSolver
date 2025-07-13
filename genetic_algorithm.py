## custom libs
from field import Field
from maze import Maze
from AStar import astar
from player import Player

## std lib
import random

class GeneticAlgorithm:
    is_end = False          ## is the problem solved, if True then quit
    bestPlayer = None
    def __init__(self, start_position: set, end_position: set, maze: Maze,  max_generations: int=50, population_size: int=100, mutation_rate: float=0.01, min_fitness_difference: float=0.1, elitism_rate: float=0.4,best_path: list=[] ):
        self.population = []
        self.best_path = best_path
        self.maze = maze
        self.max_generations = max_generations                  ## maximum number of generations
        self.current_generation = 0                             ## which generation are we at (the generation that's gonna get drafted for ww3)

        self.min_fitness_difference = min_fitness_difference    ## epsilon. If the fitness between the previous and current generation is less than this then stop the algorithm
        self.fitnesses = [999999999]                            ## save the fitness value for each generation here

        self.population_size = population_size                  ## 
        self.mutation_rate = mutation_rate                      ## 
        self.elitism_rate = elitism_rate                        ## [0-1] percentage of the elitists in the population that stay

        self.start_position = start_position                    ## starting coordinates in the maze. e.g (1,1) or (3,4)...
        self.end_position = end_position                        ## ending coordinates in the maze. e.g (1,1) or (3,4)...


        self.best_path = astar(maze= maze, start= start_position, end= end_position)  ## get the best path
        self.init_population(start=start_position, end=end_position, maze=maze)


    def init_population(self,start: set, end: set, maze: Maze):
        '''
        Sets the initial population.
        '''
        for i in range(self.population_size):
            self.population.append(Player(start, end, maze, self.best_path))
        
        # for i in range(self.population_size//2):
        #     self.population.append(Player(start, end, maze, self.best_path))
        # for i in range(self.population_size//2):
        #     self.population.append(Player(end, start, maze, self.best_path.reverse()))
        self._fitness()


    def get_max_fitness(self):
        return max(map(lambda x: x.fitness,self.population))
    
    def get_min_fitness(self):
        return min(map(lambda x: x.fitness,self.population))


    def _evaluate_population(self):
        '''
        Evaluates/updates the fitness value of all players in the population.
        '''
        for player in self.population:
            player.evaluate(fields=self.maze.fields)        ## optional fields


    def _fitness(self):
        return self.get_min_fitness()

    def get_best_path(self):
        return min(self.population,key=lambda player: player.fitness).path

    def _selection(self):

        ## sort the population by fitness in ascending order
        ## NOTE: fitness is the distance so the lower it is the better
        self.population = sorted(self.population,key=lambda player: player.fitness) 

        ## every players chance to be selected
        selection_chance = [ (self.population_size - id) * random.random() for id in range(self.population_size)]
        selected_count = int((1-self.elitism_rate) * len(self.population))
        selected = random.choices(self.population, weights=selection_chance, k=selected_count) 

        ## cross the selected players
        children = []
        for i in range(0,len(selected),2):
            if i+1 > len(selected):
                break
            # child1,child2 = selected[i].crossover_movement_instruction_stack_method(selected[i+1])
            child1,child2 = selected[i].crossover_random(selected[i+1])
            children.append(child1)
            children.append(child2)
        
        ## remove the worst in the population and then add the children
        elites = max(len(self.population) - len(children), 0)       ## how many elites are staying
        self.population = self.population[:elites]
        self.population += children
        
        

    def _mutation(self):
        for p in self.population:
            if random.random() <= self.mutation_rate:
                p.mutate()


    def is_termination_condition_satisfied(self):
        if self.current_generation >= self.max_generations:  ## too many generations
            return True
        if self.fitnesses[-1] == 0: ## reached the end
            return True
        # if abs(self.fitnesses[self.current_generation] - self.fitnesses[self.current_generation-1]) < self.min_fitness_difference:
        #     return True


    def next_gen(self):
        
        while not self.is_termination_condition_satisfied():
            self.current_generation += 1

            ## update the population fitness values
            self._evaluate_population()

            #select and crossover
            self._selection()

            #mutation with certain probability
            self._mutation()

            # update fitness values for each path
            self._evaluate_population()
            self.fitnesses.append(self._fitness())

            




