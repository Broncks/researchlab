from time import time
from proj2.warehouse import RMFS
import random


def read_demandlist(filename):
    demandlist = []
        # WRITE YOUR CODE HERE
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
    # WRITE YOUR CODE HERE
    end = time()
    print(f"Computing Time: {end-start}\n")

    print("Greedy:")
    start = time()
    # WRITE YOUR CODE HERE
    end = time()
    print(f"Computing Time: {end - start}\n")

    print("Simulated Annealing:")
    start = time()
    # WRITE YOUR CODE HERE
    end = time()
    print(f"Computing Time: {end - start}\n")


if __name__ == '__main__':
    main()