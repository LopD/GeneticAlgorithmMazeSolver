## custom libs
from maze import Maze
from AStar import astar
import config as cfg
from genetic_algorithm import GeneticAlgorithm

def run_test(seeds: list=[]):
    test_statistics = []        ## list like [(no_generations,fitness),(no_generations,fitness),...]
    for seed in seeds:
        maze = Maze()
        maze.generate_random_maze(seed_value=seed)
        print("------------ MAZE ------------")
        print(maze)
        print("------------------------------")

        astar_path = astar(maze=maze, start=cfg.START_COORDS, end=cfg.END_COORDS)
        print("------------ ideal path ------------")
        maze.print_with_path(path=astar_path, start=cfg.START_COORDS, end=cfg.END_COORDS)
        print("------------------------------------")

        print("------------ FITNESSES ------------")
        maze.evaluate_fields(start=cfg.START_COORDS, end=cfg.END_COORDS)
        maze.print_field_fitnesses(start=cfg.START_COORDS, end=cfg.END_COORDS)
        print("-----------------------------------")

        gen_algo = GeneticAlgorithm(
            max_generations=cfg.GENERATIONS,
            population_size=cfg.POPULATION_SIZE,
            mutation_rate=cfg.MUTATION_RATE,
            start_position=cfg.START_COORDS,
            end_position=cfg.END_COORDS,
            maze=maze
        )
        gen_algo.next_gen()

        print("FITNESSES THROUGH GENERATIONS:")
        for id,fitness in enumerate(gen_algo.fitnesses):
            print(id,fitness)
        
        ## save the statistics:
        test_statistics.append((len(gen_algo.fitnesses),gen_algo.fitnesses[-1]))
        
        best_path = gen_algo.get_best_path()
        print("Best path=",best_path)
        print("------------ best found path visualized ------------")
        maze.print_with_path(path=best_path, start=cfg.START_COORDS, end=cfg.END_COORDS)
        print("----------------------------------------------------")
        # print('Hello world!')
    
    return test_statistics


if __name__ == '__main__':
    import sys
    print("OUTPUT IS REDIRECTED TO \'output.txt\'!")
    # Open the file for writing
    f = open('output.txt', 'w')

    # Redirect stdout to the file
    sys.stdout = f


    seeds = [42,43,44,45,46,47,48,49,50,51,52]
    # seeds = [52]
    test_statistics = run_test(seeds)
    
    ## print final statistics:
    print("test_statistics:")
    for id in range(len(seeds)):
        print(f"test id={id}; seed={seeds[id]}; num of generations={test_statistics[id][0]}; fitness={test_statistics[id][1]}")

    # Optional: reset stdout back to normal (console)
    sys.stdout = sys.__stdout__
    f.close()
    
    
    