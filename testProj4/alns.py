import numpy as np
from warehouse import RMFS
import random
from math import exp



def _destroy(solutionlist, max_placeid, returning_pods):

   
    appearance_counter = np.repeat(0,max(returning_pods)+1)

    for eachpod in returning_pods:
        if eachpod != -1:
            appearance_counter[eachpod] = appearance_counter[eachpod]+1

    pod_probability = appearance_counter/len(returning_pods)

    i=0
    for eachpod in returning_pods:
        solutionlist[i] = np.random.choice([-2, solutionlist[i]], p = [pod_probability[eachpod], 1-pod_probability[eachpod]])
        i += 1

    return solutionlist, 0



def _destroy2(solutionlist, max_placeid, returning_pods):

    current_returning_pods = returning_pods

    i = 0
    for eachpod in returning_pods:

        try:
            distance_next_appearance = np.where(current_returning_pods == eachpod)[0][1]

        except:
            solutionlist[i] = 2

        finally:
            current_returning_pods = np.delete(current_returning_pods,0)
            if distance_next_appearance <= 7:
                solutionlist[i] = -1
            if distance_next_appearance >= 20:
                solutionlist[i] = -3
            i += 1

    
    return solutionlist, 1

def _destroy3(solutionlist, max_placeid, returning_pods):

    
    for eachline in range(len(solutionlist)):
        if np.random.randint(100) <= 15:
            solutionlist[eachline] = -2
        

    return solutionlist, 2

def _repair(solutionlist, max_placeid, returning_pods):

    i = 0
    for eachsolution in solutionlist:

        if eachsolution == -1:
            solutionlist[i] = np.random.choice([0,1], p = [0.999,0.001])
        if eachsolution == -2:
            solutionlist[i] = np.random.choice([0,1,2], p = [0.55,0.35,0.1])
        if eachsolution == -3:
            solutionlist[i] = np.random.choice([1,2,3], p = [0.05,0.7,0.25])
        i += 1

    return solutionlist


def acceptSolution(cost_delta, temperature):

    if exp(-(cost_delta/temperature)) > random.uniform(0,1):
        return True
    else:
        return False


def solve(rmfs, demandlist, initsol, returning_pods, l, waccepted, wrejected, stop):
    """
    Generate a list of pod return places using variable large neighborhood search

    Args:
        rmfs (Warehouse): Warehouse
        demandlist (list): Demand, 1 pod per iteration
        initsol (list): Initial solution, 1 pod return place per iteration
        returning_pods (list): List of returning pods, 1 per iteration
        l (float): lambda, update parameter, see page 23 in presentation
        waccepted (float): w3, see page 23 in presentation
        wrejected (float): w4, see page 23 in presentation
        stop: value for stop criterion for alns
    Returns:
        solutionlist (list): List of pod return places, 1 per iteration
        acceptancerate (float): Acceptance rate of new solutions, (n accepted solutions)/(n iterations)
    """

    # SA-parameters:

    # start:
    temperature = 10000
    # cooling-factor
    cooling_factor = 0.8


    max_placeid = rmfs.nplaces - rmfs.npods + rmfs.nstations*rmfs.qsize
   
    current_solutionlist = initsol.copy()
    best_solutionlist = initsol.copy()

    _ , best_cost = rmfs.run(demandlist, best_solutionlist)

    n_accepted_solutions = 0

    destroy_probabilities = np.array([1.0, 1.0, 1.0])
    destroy_methods = [_destroy,_destroy2,_destroy3]


    for number_of_iterations in range(stop):

        new_solutionlist, destroy_method_id = destroy_methods[np.random.choice(np.arange(len(destroy_methods)), p = destroy_probabilities/sum(destroy_probabilities))](current_solutionlist, max_placeid, returning_pods)
        new_solutionlist = _repair(new_solutionlist, max_placeid, returning_pods)

        _ , new_cost = rmfs.run(demandlist, new_solutionlist)
        _ , current_cost = rmfs.run(demandlist, current_solutionlist)

        if new_cost < best_cost:
            best_cost = new_cost
            best_solutionlist = new_solutionlist.copy()
            current_solutionlist = new_solutionlist.copy()
            destroy_probabilities[destroy_method_id] = waccepted*(1-l)+l*destroy_probabilities[destroy_method_id]
            n_accepted_solutions += 1

        else: 
            if acceptSolution(new_cost - current_cost, temperature): # additional simulated annealing
                current_solutionlist = new_solutionlist.copy()
            destroy_probabilities[destroy_method_id] = wrejected*(1-l)+l*destroy_probabilities[destroy_method_id]

        temperature = temperature * cooling_factor


    return best_solutionlist, n_accepted_solutions/number_of_iterations



