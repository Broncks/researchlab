import numpy as np
import math
import random

sa_temperature = 1000


def alns(rmfs, rand_solutionlist, demandlist):
    global sa_temperature
    iterations = 200
    sa_final_temperature = 100

    solutionlist = rand_solutionlist
    best_solutionlist = solutionlist
    weight_destroy = [1.0, 1.0, 1.0, 1.0]  # All options start with the same weight
    weight_repair = [1.0, 1.0, 1.0, 1.0]

    i = 0  # counter
    while sa_temperature > sa_final_temperature and i < iterations:
        omega = [False, False, False, False]  # o1, o2, o3, o4

        destroy = [destroy1, destroy2, destroy3, destroy4]
        # Selects index from possible destroy-methods with weights
        index_destroy = np.random.choice(range(len(destroy)), p=weight_to_prob(weight_destroy))
        destroyed_list = destroy[index_destroy](solutionlist)  # Execution of selected method

        repair = [repair1, repair2, repair3, repair4]
        index_repair = np.random.choice(range(len(repair)), p=weight_to_prob(weight_repair))
        candidate_solution = repair[index_repair](destroyed_list) #repair destroyed list & generate candidate solution

        print("ALNS:", "t:", round(sa_temperature, 1), "i:", str(i).zfill(2), "r:", index_repair, "d:", index_destroy,
              "wd:", [round(i, 1) for i in weight_destroy], "wr:", [round(i, 1) for i in weight_destroy])

        # Checks current candidate solution for acceptance
        if accept(rmfs, demandlist, solutionlist, candidate_solution, omega):
            solutionlist = candidate_solution

        storage_sl, cost_sl = rmfs.run(demandlist, solutionlist)
        storage_best, cost_best = rmfs.run(demandlist, best_solutionlist)
        if cost_sl < cost_best:  # f(s') < f(s*)
            best_solutionlist = solutionlist
            omega[0] = True  # o1 is true if f(s') < f(s*)

        # Updates the weights according to the assigned omega (1-4)
        weight_destroy = update_probability(weight_destroy, index_destroy, omega)
        weight_repair = update_probability(weight_repair, index_repair, omega)

        i += 1

    if sa_temperature <= sa_final_temperature:
        print(f"STOP: Temperature {round(sa_temperature, 1)} below final temperature {sa_final_temperature}")
    elif i >= iterations:
        print(f"STOP: Iterations {i} reached maximum iterations {iterations}")

    sa_temperature = 1000  # Reset of simulated annealing temperature for next iteration
    return best_solutionlist


"""Destroy-Methods"""

def destroy1(solutionlist):
    """Destroying each item of solutionlist with defined percentage to value -1"""
    sl = solutionlist.copy()
    percentage = 15
    for i in range(len(sl)):
        if np.random.randint(100) <= percentage:
            sl[i] = -1
    return sl


def destroy2(solutionlist):
    sl = solutionlist.copy()
    random_counter = np.random.randint(0, 9)
    random_part = random_counter * 1000
    for i in range(1000):
        sl[random_part] = -1
        random_part += 1

    return sl


def destroy3(solutionlist):
    sl = solutionlist.copy()
    for i in range(len(sl)):
        rand_int = np.random.randint(0, 1)
        if rand_int == 0:
            if sl[i] >= 3:
                sl[i] = -1

    return sl


def destroy4(solutionlist):
    sl = solutionlist.copy()
    percentage = 30
    for i in range(len(sl)):
        if np.random.randint(100) <= percentage:
            sl[i] = -1

    return sl


"""Repair-Methods"""

def repair1(solutionlist):
    """Repairing values of solutionlist marked with -1 with 0 in 99.9% of cases and 1 in 0.1% of cases"""
    sl = solutionlist.copy()
    for i in range(len(sl)):
        if sl[i] == -1:
            sl[i] = np.random.choice([0, 1], p=[0.999, 0.001])
    return sl


def repair2(solutionlist):
    sl = solutionlist.copy()
    for i in range(len(sl)):
        if sl[i] == -1:
            sl[i] = np.random.randint(0, 9)
    return sl


def repair3(solutionlist):
    sl = solutionlist.copy()
    for i in range(len(sl)):
        if sl[i] == -1:
            sl[i] = np.random.choice([0, 1, 2], p=[0.95, 0.025, 0.025])
    return sl


def repair4(solutionlist):
    sl = solutionlist.copy()
    for i in range(len(sl)):
        if sl[i] == -1:
            sl[i] = 0
    return sl


def weight_to_prob(weight_list):
    """Converts the weights to percentages"""
    wl = weight_list.copy()
    sum = 0
    for item in wl:
        sum += item

    for i in range(len(wl)):
        wl[i] = wl[i] / sum
    return wl


def calc_psi(omega):
    """Returning the correct psi value by only returning the maximum omega"""
    # o1 >= o2 >= o3 >= o4
    o = [5,  # o1 if f(s') < f(s*)
         4,  # o2 if f(s') < f(s)
         2,  # o3 if s' accepted
         0.8]  # o4 if s' not accepted

    # Because o1 >= o2 >= o3 >= o4, only the maximum omega will be returned -> definition of psi
    if omega[0]:
        return o[0]
    elif omega[1]:
        return o[1]
    elif omega[2]:
        return o[2]
    elif omega[3]:
        return o[3]
    else:
        raise IndexError


def update_probability(list, index, omega):
    """Updates the probability at index of the provided list"""
    li = list.copy()
    # lamda zwischen 0 und 1
    lamda = 0.8

    li[index] = lamda * li[index] + (1 - lamda) * calc_psi(omega)  # Folie 60/99
    return li


def accept(rmfs, demandlist, sl, sl_cand, omega):
    """Implementation of SA to decided wether to accept candidate solutionlist"""
    global sa_temperature
    cooling_factor = 0.95

    # determine storage & cost based on solutionlists provided in method-argument
    storage, current_cost = rmfs.run(demandlist, sl)
    storage, neighbor_cost = rmfs.run(demandlist, sl_cand)
    cost_difference = neighbor_cost - current_cost

    if neighbor_cost < current_cost:
        omega[1] = True # o2 is true if f(s') < f(s)

    if math.exp(-cost_difference / sa_temperature) > random.uniform(0, 1) or cost_difference < 0:
        # Candidate solution is accepted
        sa_temperature *= cooling_factor  # Cool temperature down
        omega[2] = True  # o3 is true if s' is accepted
        return True
    else:
        # Candidate solution is declined
        sa_temperature *= cooling_factor  # Cool temperature down
        omega[3] = True  # o4 is true if s' not accepted
        return False
