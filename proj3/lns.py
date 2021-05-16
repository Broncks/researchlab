import numpy as np
import math
import random

sa_temperature = 1000


def lns(rmfs, rand_solutionlist, demandlist):
    iterations = 200
    
    solutionlist = rand_solutionlist
    best_solutionlist = solutionlist

#    while not stop_criterion:
#   TODO: stop_criterion
    for i in range(iterations):
        candidate_solution = repair(destroy(solutionlist))

        if accept(rmfs, demandlist, solutionlist, candidate_solution):
            solutionlist = candidate_solution

        storage_sl, cost_sl = rmfs.run(solutionlist)
        storage_best, cost_best = rmfs.run(best_solutionlist)
        if cost_sl < cost_best:
            best_solutionlist = solutionlist

    return best_solutionlist
        
        
        
def destroy(sl):
    percentage = 15

    for i in range(len(sl)):
        if np.random.randint(100) <= percentage:
            sl[i] = -1

    return sl


def repair(sl): # TODO

    for i in range(len(sl)):
        if sl[i] == -1:
            sl[i] = np.random.choice([0, 1], p=[0.999, 0.001])

    return sl
    
def accept(rmfs, demandlist, sl, sl_cand): # TODO
    global sa_temperature
    cooling_factor = 0.9

    # determine storage & cost based on solutionlists provided in method-argument
    storage, current_cost = rmfs.run(demandlist, sl)
    storage, neighbor_cost = rmfs.run(demandlist, sl_cand)
    cost_difference = neighbor_cost - current_cost

    if math.exp(-cost_difference / sa_temperature) > random.uniform(0, 1) or cost_difference < 0:
        sa_temperature *= cooling_factor  # cool temperature down
        return True
    else:
        sa_temperature *= cooling_factor  # cool temperature down
        return False




