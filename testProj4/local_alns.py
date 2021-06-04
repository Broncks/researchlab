import numpy as np
from warehouse import RMFS
import random
from math import exp


def _destroy(solutionlist, max_placeid, returning_pods):

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

    
    return solutionlist


def _repair(solutionlist, max_placeid, returning_pods):

    i = 0
    for eachsolution in solutionlist:

        if eachsolution == -1:
            solutionlist[i] = np.random.choice([0,1], p = [0.999,0.001])
        if eachsolution == -3:
            solutionlist[i] = np.random.choice([1,2,3], p = [0.05,0.7,0.25])
        i += 1

    return solutionlist




def solve(rmfs, demandlist, initsol, returning_pods, stop):
    """
    Generate a list of pod return places using variable large neighborhood search

    Args:
        rmfs (Warehouse): Warehouse
        demandlist (list): Demand, 1 pod per iteration
        initsol (list): Initial solution, 1 pod return place per iteration
        returning_pods (list): List of returning pods, 1 per iteration
        waccepted (float): w3, see page 23 in presentation
        wrejected (float): w4, see page 23 in presentation
        stop: value for stop criterion for alns
    Returns:
        solutionlist (list): List of pod return places, 1 per iteration
        acceptancerate (float): Acceptance rate of new solutions, (n accepted solutions)/(n iterations)
    """


    max_placeid = rmfs.nplaces - rmfs.npods + rmfs.nstations*rmfs.qsize
   
    current_solutionlist = initsol.copy()
    best_solutionlist = initsol.copy()

    _ , best_cost = rmfs.run(demandlist, best_solutionlist)


    for number_of_iterations in range(stop):

        new_solutionlist = _destroy(current_solutionlist, max_placeid, returning_pods)
        new_solutionlist = _repair(new_solutionlist, max_placeid, returning_pods)

        _ , new_cost = rmfs.run(demandlist, new_solutionlist)
        _ , current_cost = rmfs.run(demandlist, current_solutionlist)

        if new_cost < best_cost:
            best_cost = new_cost
            best_solutionlist = new_solutionlist.copy()
            current_solutionlist = new_solutionlist.copy()


    return best_solutionlist



