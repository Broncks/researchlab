from time import time
from proj2.warehouse import RMFS
from proj2.simulated_annealing import *

def read_demandlist(filename):
    demandlist = []
    # WRITE YOUR CODE HERE
    with open(filename, "r") as file:
        for line in file:
            p = line.split()
            demandlist.append((int(p[0]), int(p[1])))
    file.close()

    return demandlist


def read_storage(filename):
    with open(filename) as f:
        initstorage = [int(line) for line in f]
    return initstorage


def print_stats(storage, cost, steps):
    print(f"Storage Area: \n{storage}")
    print(f"Total cost: {cost}")
    print(f"Avg. cost per pod movement: {cost / steps / 2}")


def main():
    ppods = .75
    nplaces = 20
    nstations = 2
    qsize = 3
    max_placeid = nplaces - int(ppods * nplaces) + nstations * qsize

    initstorage = read_storage("initial_storage.txt")
    demandlist = read_demandlist('demandlist.txt')

    rmfs = RMFS(initstorage, ppods, nplaces, nstations, qsize)

    print("Random:")
    start = time()
    # WRITE YOUR CODE HERE

    """Eigener Code Anfang"""
    solutionlist = []
    demandlist = read_demandlist("demandlist.txt")
    print("demandlist ", demandlist)
    for i in range(10000):
        solutionlist.append(random.randint(0, 10))

    print("solutionlist ", solutionlist)
    print("länge solutionlist ", len(solutionlist))
    print("länge demandlist ", len(demandlist))
    storage, cost_random = (rmfs.run(demandlist, solutionlist))
    print(storage, cost_random)
    print(type(cost_random))
    """Eigener Code Ende"""

    # benötig: solutionlist_random

    end = time()
    print(f"Computing Time: {end - start}\n")

    print("Greedy:")
    start = time()
    # WRITE YOUR CODE HERE
    end = time()
    print(f"Computing Time: {end - start}\n")

    print("Simulated Annealing:")
    start = time()
    sa_solutionlist = simulated_annealing(rmfs, demandlist, solutionlist, cost_random)
    storage, cost_sa = rmfs.run(demandlist, sa_solutionlist)
    print(storage, cost_sa)
    end = time()
    print(f"Computing Time: {end - start}\n")


if __name__ == '__main__':
    main()
