import numpy as np
import math
import random

sa_temperature = 1000


def lns(rmfs, rand_solutionlist, demandlist):
    global sa_temperature
    iterations = 200
    sa_final_temperature = 100

    solutionlist = rand_solutionlist
    best_solutionlist = solutionlist

    i = 0  # counter
    while sa_temperature > sa_final_temperature and i < iterations:
        print("LNS:", "t:", round(sa_temperature, 1), "i:", i)
        candidate_solution = repair(destroy(solutionlist))

        if accept(rmfs, demandlist, solutionlist, candidate_solution):
            solutionlist = candidate_solution

        storage_sl, cost_sl = rmfs.run(demandlist, solutionlist)
        storage_best, cost_best = rmfs.run(demandlist, best_solutionlist)
        if cost_sl < cost_best:
            best_solutionlist = solutionlist

        i += 1

    if sa_temperature <= sa_final_temperature:
        print(f"STOP: Temperature {round(sa_temperature, 1)} below final temperature {sa_final_temperature}")
    elif i >= iterations:
        print(f"STOP: Iterations {i} reached maximum iterations {iterations}")

    sa_temperature = 1000
    return best_solutionlist


def destroy(solutionlist):
    percentage = 15

    sl = solutionlist.copy()
    for i in range(len(sl)):
        if np.random.randint(100) <= percentage:
            sl[i] = -1
    return sl


def repair(solutionlist):
    sl = solutionlist.copy()
    for i in range(len(sl)):
        if sl[i] == -1:
            sl[i] = np.random.choice([0, 1], p=[0.999, 0.001])
    return sl


def accept(rmfs, demandlist, sl, sl_cand):
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
