from time import time
from Source.project2.warehouse import RMFS
from random import *


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

def main():
    ppods = .75
    nplaces = 20
    nstations = 2
    qsize = 3
    max_placeid = nplaces - int(ppods*nplaces) + nstations*qsize

    initstorage = read_storage("initial_storage.txt")
    demandlist = read_demandlist('demandlist.txt')

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

    print("Large Neighborhood Search:")
    start = time()
    # WRITE YOUR CODE HERE
    end = time()
    print(f"Computing Time: {end - start}\n")


if __name__ == '__main__':
    main()