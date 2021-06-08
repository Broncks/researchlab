from time import time
from proj4.warehouse import RMFS
from random import *
from proj4.aco import *


def read_demandlist(filename):
    with open(filename) as f:
        demandlist = [tuple(map(int, line.removesuffix("\n").split(" "))) for line in f]
    return demandlist

def read_storage(filename):
    with open(filename) as f:
        initstorage = [int(line) for line in f]
    return initstorage

def print_stats(storage, cost, steps):
    print(f"Storage Area: \n{storage}")
    print(f"Total cost: {cost}")
    print(f"Avg. cost per pod movement: {cost/steps/2}")

def main(list_number):
    ppods = .75
    nplaces = 20
    nstations = 2
    qsize = 3
    max_placeid = nplaces - int(ppods*nplaces) + nstations*qsize

    initstorage = read_storage("initial_storage.txt")
    demandlist = read_demandlist(f'demandlist{list_number}.txt')

    rmfs = RMFS(initstorage, ppods, nplaces, nstations, qsize)

    print("Random:")
    start = time()
    solutionlist_rand = [randrange(0, max_placeid) for i in range(len(demandlist))]
    storage, cost = rmfs.run(demandlist, solutionlist_rand)
    print_stats(storage, cost, len(demandlist))
    end = time()
    print(f"Computing Time: {end-start}\n")

    print("Greedy:")
    start = time()
    solutionlist_cheap = [0] * len(demandlist)
    storage, cost = rmfs.run(demandlist, solutionlist_cheap)
    print_stats(storage, cost, len(demandlist))
    end = time()
    print(f"Computing Time: {end - start}\n")

    print("Ant Colony Optimization:")
    start = time()
    solutionlist_aco = aco(rmfs, demandlist, solutionlist_rand)
    storage, cost = rmfs.run(demandlist, solutionlist_aco)
    print_stats(storage, cost, len(demandlist))
    end = time()
    print(f"Computing Time: {end - start}\n")


if __name__ == '__main__':
    for i in range(3):  # Iterates the three demandlists and executes main() with them
        print(f">> Demandlist {i}")
        main(i + 1)