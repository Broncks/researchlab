import random
import math
from proj2.create_neighbor import create_neighbor_list


def simulated_annealing(rmfs, demandlist, initial_list, start_temperature):
    """
        Peforms simulated annealing (SA) algorithm to find a solution

        Args:
            rmfs (Warehouse): Warehouse
            demandlist (list): List of demanded pods (-> one pod per iteration)
            initial_list (list): list based on random algorithm used as initial solution
                                 (-> one pod return place per iteration)
            start_temperature (int): used as initial temperature for SA algorithm

        Return:
            sa_solutionlist (list): List of pod return places of SA algorithm
                                    (-> one pod return place per iteration)
    """


    final_temperature = 10 # perform SA algorithm till final_temperature is reached
    cooling_factor = 0.9
    iterations = 10
    iterations_per_temperature = 0 # mögl. unnötig

    temperature = start_temperature
    sa_solutionlist = initial_list

    # determine storage & cost based on solutionlist_random provided in method-argument
    storage, best_cost = rmfs.run(demandlist, initial_list)
    storage, current_cost = rmfs.run(demandlist, initial_list)

    j = 0 # counter iterations
    while temperature > final_temperature and j < iterations:
        print("Iteration: ", j+1)
        print("Temperature:", temperature)
        #neighbor_solutionlist = [create_neighbor(i) for i in sa_solutionlist] # create neighbors
        neighbor_solutionlist = create_neighbor_list(sa_solutionlist) # create neighbors
        storage, neighbor_cost = rmfs.run(demandlist, neighbor_solutionlist) # check neighbors
        cost_difference = neighbor_cost - current_cost

        if math.exp(-cost_difference / temperature) > random.uniform(0, 1) or cost_difference < 0:
            current_cost = neighbor_cost

            if current_cost < best_cost: # check if current_cost better than best_cost
                best_cost = current_cost
                sa_solutionlist = neighbor_solutionlist


            # iterations_per_temperature += 1
            # if iterations_per_temperature > 10: #SINN???
            temperature *= cooling_factor

        j += 1

    return sa_solutionlist

