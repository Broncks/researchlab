from time import time
from proj3.warehouse import RMFS
from proj3.lns import *
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

def main(list_number):
    ppods = .75
    nplaces = 20
    nstations = 2
    qsize = 3
    max_placeid = nplaces - int(ppods*nplaces) + nstations*qsize

    initstorage = read_storage("initial_storage.txt")
    demandlist = read_demandlist(f'demandlist{list_number}.txt')

     #TODO Warehouse
    rmfs = RMFS(initstorage, ppods, nplaces, nstations, qsize)

    print("Random:") #TODO Random ist scheiße!
    start = time()
    solutionlist_rand = [randrange(0, max_placeid) for i in range(len(demandlist))]
    storage, cost = rmfs.run(demandlist, solutionlist_rand)
    # Fehler tritt auf, wenn ein Wert der Solution zufällig größer ist, als die aktuell freien Plätze der Storage
    # Nur bei der 2. Demandlist sind IMMER zu Beginn für 3 Iterationen nur 9 Plätze im Storage frei
    # Wenn in diesen Iterationen ein Wert größer-gleich 9 in der Solution steht, gibt's Index out of bounds
    # Warum? Immer noch keine Ahnung...
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
    solutionlist_lns = lns(rmfs, solutionlist_rand, demandlist)
    storage, cost = rmfs.run(demandlist, solutionlist_lns)
    print_stats(storage, cost, len(demandlist))
    end = time()
    print(f"Computing Time: {end - start}\n")


if __name__ == '__main__':
    for i in range(3):
        print("Hauptschleife: ", i)
        main(i+1)
