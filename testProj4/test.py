import numpy as np
from time import time
from warehouse import RMFS
import aco
import alns


def read_demandlist(filename):
    with open(filename) as f:
        demandlist = [tuple(map(int, i.replace('(','').replace(')','').split(','))) for i in f]
    return demandlist

def print_stats(storage, cost, steps):
    print(f"Storage Area: \n{storage}")
    print(f"Total cost: {cost}")
    print(f"Avg. cost per pod movement: {cost/steps/2}")

def main():
    ppods = .75
    nplaces = 20
    nstations = 2
    qsize = 3
    max_placeid = nplaces - int(ppods*nplaces) + nstations*qsize

    initstorage = np.loadtxt('initial_storage.txt', int)
    demandlist = read_demandlist('demandlist.txt')
    returning_pods = np.loadtxt('returning_pods.txt', int)

    rmfs = RMFS(initstorage, ppods, nplaces, nstations, qsize)

    print("Random:")
    solutionlist_rand = np.random.randint(max_placeid, size = len(demandlist))
    storage, cost = rmfs.run(demandlist, solutionlist_rand)
    print_stats(storage, cost, len(demandlist))

    print("Cheapest place:")
    solutionlist_cheap = [0] * len(demandlist)
    storage, cost = rmfs.run(demandlist, solutionlist_cheap)
    print_stats(storage, cost, len(demandlist))

    # print("Large Neighborhood Search:")
    # start = time()
    # solutionlist, acceptance_rate = alns.solve(rmfs, demandlist, solutionlist_cheap, returning_pods, 0.8, 25, 1, 200)
    # storage, cost = rmfs.run(demandlist, solutionlist)
    # print_stats(storage, cost, len(demandlist))

    print("aco-sequentially:")
    start = time()
    solutionlist = aco.acoSolve(rmfs, demandlist, solutionlist_rand, returning_pods, 25, 50, 0.6)
    storage, cost = rmfs.run(demandlist, solutionlist)
    print_stats(storage, cost, len(demandlist))

    print("aco-parallel:")
    start = time()
    solutionlist = aco.solve_parallel(rmfs, demandlist, solutionlist_rand, returning_pods, 25, 50, 0.6)
    storage, cost = rmfs.run(demandlist, solutionlist)
    print_stats(storage, cost, len(demandlist))

    #print(f"Acceptance Rate: {acceptance_rate}")
    end = time()
    print(f"Computing time: {end - start}")

if  __name__ == '__main__':
    main()