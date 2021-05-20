import numpy as np
import math
import random

sa_temperature = 1000  # Start temperature of simulated annealing


def alns(rmfs, rand_solutionlist, demandlist):  # Adaptive Large Neighborhood Search (ALNS)
    global sa_temperature
    iterations = 200
    sa_final_temperature = 50

    solutionlist = rand_solutionlist
    best_solutionlist = solutionlist

    # Weights for ALNS's destroy & repair methods
    weight_destroy = [1.0, 1.0, 1.0, 1.0]  # All options start with the same weight
    weight_repair = [1.0, 1.0, 1.0, 1.0]

    sum_destroy = [0, 0, 0, 0]  # Accumulates all weight values for calculating the average
    sum_repair = [0, 0, 0, 0]

    i = 0  # Counter
    while sa_temperature > sa_final_temperature and i < iterations:
        # List for noting all omegas in one iteration
        omega = [False, False, False, False]
        #         o1,    o2,    o3,    o4

        # Array stores all possible destroy methods
        destroy = [destroy1, destroy2, destroy3, destroy4]
        # Selects index from possible destroy methods by using weights
        index_destroy = np.random.choice(range(len(destroy)), p=weight_to_prob(weight_destroy))
        destroyed_list = destroy[index_destroy](solutionlist)  # Execution of selected method and storing return value

        # Function is the same as above
        repair = [repair1, repair2, repair3, repair4]
        index_repair = np.random.choice(range(len(repair)), p=weight_to_prob(weight_repair))
        candidate_solution = repair[index_repair](destroyed_list)  # Fills candidate solution
        # Candidate solution is a generated solutionlist which will be evaluated for usage

        # Output of current values of iteration
        print("ALNS:", "t:", round(sa_temperature, 1), "i:", str(i).zfill(3), "r:", index_repair, "d:", index_destroy,
              "wd:", [round(i, 1) for i in weight_destroy], "wr:", [round(i, 1) for i in weight_repair])

        # Checks current candidate solution for acceptance
        if accept(rmfs, demandlist, solutionlist, candidate_solution, omega):
            solutionlist = candidate_solution

        storage_sl, cost_sl = rmfs.run(demandlist, solutionlist)
        storage_best, cost_best = rmfs.run(demandlist, best_solutionlist)
        if cost_sl < cost_best:  # f(s') < f(s*)
            best_solutionlist = solutionlist
            omega[0] = True  # o1 is true if f(s') < f(s*)

        # Updates the weights according to their assigned omega (1-4)
        weight_destroy = update_probability(weight_destroy, index_destroy, omega)
        weight_repair = update_probability(weight_repair, index_repair, omega)

        # Summing up the weights for average calculation
        for j in range(len(sum_destroy)):
            sum_destroy[j] += weight_destroy[j]
        for j in range(len(sum_repair)):
            sum_repair[j] += weight_repair[j]

        i += 1

    # Output of reason for stop of iteration
    if sa_temperature <= sa_final_temperature:
        print(f"STOP: Temperature {round(sa_temperature, 1)} below final temperature {sa_final_temperature}")
    elif i >= iterations:
        print(f"STOP: Iterations {i} reached maximum iterations {iterations}")

    print(
        f"Avg. Destroy: {[round(j / i, 2) for j in sum_destroy]} Avg. Repair: {[round(j / i, 2) for j in sum_repair]}")

    sa_temperature = 1000  # Reset of simulated annealing temperature for next iteration
    return best_solutionlist


"""Destroy-Methods"""


def destroy1(solutionlist):
    """
        Destroying each item of solutionlist with defined percentage (15%) to value -1

        Args:
            solutionlist (list): Current solution

        Return:
            sl (list): Modified solution
    """
    sl = solutionlist.copy()
    percentage = 15
    for i in range(len(sl)):
        if np.random.randint(100) <= percentage:
            sl[i] = -1
    return sl


def destroy2(solutionlist):
    """
        Destroying each item of solutionlist with defined percentage (25%) to value -1

        Args:
            solutionlist (list): Current solution

        Return:
            sl (list): Modified solution
    """
    sl = solutionlist.copy()
    percentage = 25
    for i in range(len(sl)):
        if np.random.randint(100) <= percentage:
            sl[i] = -1
    return sl


def destroy3(solutionlist):
    """
        Destroying a value greater than or equal to 3 with a value of -1 in 50% of cases

        Args:
            solutionlist (list): Current solution

        Return:
            sl (list): Modified solution
    """
    sl = solutionlist.copy()
    for i in range(len(sl)):
        rand_int = np.random.choice([0, 1])
        if rand_int == 0:
            if sl[i] >= 3:
                sl[i] = -1
    return sl


def destroy4(solutionlist):
    """
        Destroying a random part of the solution by changing 1000 consecutive values to value -1

        Args:
            solutionlist (list): Current solution

        Return:
            sl (list): Modified solution
    """
    sl = solutionlist.copy()
    random_counter = np.random.randint(0, 9)
    random_part = random_counter * 1000
    for i in range(1000):
        sl[random_part] = -1
        random_part += 1
    return sl


"""Repair-Methods"""


def repair1(solutionlist):
    """
        Repairing values of solutionlist marked with -1 with 0 in 99.9% of cases and 1 in 0.1% of cases

        Args:
            solutionlist (list): Current destroyed solution

        Return:
            sl (list): Repaired solution
    """
    sl = solutionlist.copy()
    for i in range(len(sl)):
        if sl[i] == -1:
            sl[i] = np.random.choice([0, 1], p=[0.999, 0.001])
    return sl


def repair2(solutionlist):
    """
        Repairing values of solutionlist marked with an integer value in range 0-2

        Args:
            solutionlist (list): Current destroyed solution

        Return:
            sl (list): Repaired solution
    """
    sl = solutionlist.copy()
    for i in range(len(sl)):
        if sl[i] == -1:
            sl[i] = np.random.randint(0, 2)
    return sl


def repair3(solutionlist):
    """
        Repairing values of solutionlist marked with -1 with 0 in 95% of cases, 1 in 2.5% of cases & 2 in 2.5% of cases

        Args:
            solutionlist (list): Current destroyed solution

        Return:
            sl (list): Repaired solution
    """
    sl = solutionlist.copy()
    for i in range(len(sl)):
        if sl[i] == -1:
            sl[i] = np.random.choice([0, 1, 2], p=[0.95, 0.025, 0.025])
    return sl


def repair4(solutionlist):
    """
        Repairing values of solutionlist marked with -1 with 0 (equivalent to greedy heuristic)

        Args:
            solutionlist (list): Current destroyed solution

        Return:
            sl (list): Repaired solution
    """
    sl = solutionlist.copy()
    for i in range(len(sl)):
        if sl[i] == -1:
            sl[i] = 0
    return sl


def weight_to_prob(weight_list):
    """
        Converts the weights to percentages

        Args:
            weight_list (list): Contains the current weights for either the repair or destroy methods

        Return:
            wl (list): Weight list with values in percent
    """
    wl = weight_list.copy()
    sum = 0
    for item in wl:
        sum += item

    for i in range(len(wl)):
        wl[i] = wl[i] / sum
    return wl


def calc_psi(omega):
    """
        Returning the correct psi value by only returning the maximum omega

        Args:
            omega (list): Contains boolean values to check for maximum value according to weights of omega

        Return:
            psi (int): Maximum value of all omega from current iteration
    """
    # o1 >= o2 >= o3 >= o4
    o = [5,  # o1 if f(s') < f(s*)
         2.5,  # o2 if f(s') < f(s)
         0.9,  # o3 if s' accepted
         0.4]  # o4 if s' not accepted

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
    """
        Updates the probability at index of the provided list

        Args:
            list (list): Weight list for possible repair & destroy methods
            index (int): Specifies the method in the list which will be updated
            omega (list): List of omega for calculating psi

        Return:
            li (list): List with changed weight at index
    """
    li = list.copy()
    # lamda between 0 and 1
    lamda = 0.8

    li[index] = lamda * li[index] + (1 - lamda) * calc_psi(omega)  # Equation from slide 60
    return li


def accept(rmfs, demandlist, sl, sl_cand, omega):
    """
        Implementation of SA to decided wether to accept candidate solutionlist

        Args:
            rmfs (Warehouse): Warehouse
            demandlist (list): List of demanded pods
            sl (list): Current solutionlist
            sl_cand (list): Candidate solutionlist to be evaluated
            omega (list): List of boolean values to determine omega and psi later on

        Return:
            (bool): State of acceptance
    """
    global sa_temperature
    cooling_factor = 0.98

    # determine storage & cost based on solutionlists provided in method-argument
    storage, current_cost = rmfs.run(demandlist, sl)
    storage, candidate_cost = rmfs.run(demandlist, sl_cand)
    cost_difference = candidate_cost - current_cost

    if candidate_cost < current_cost:
        omega[1] = True  # o2 is true if f(s') < f(s)

    # Functionality of simulated annealing
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
