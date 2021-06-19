from time import time
from proj5.warehouse import RMFS
from random import *
from proj5.ga import *
from proj5.result_collector import Result_collector
from proj5.output import *
import copy

all_results = Result_collector()

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

    all_results.cost_random = cost
    all_results.avg_cost_random = cost / len(solutionlist_rand) / 2

    end = time()
    print(f"Computing Time: {end-start}\n")


    print("Greedy:")
    start = time()
    solutionlist_cheap = [0] * len(demandlist)
    storage, cost = rmfs.run(demandlist, solutionlist_cheap)
    print_stats(storage, cost, len(demandlist))

    all_results.cost_greedy = cost
    all_results.avg_cost_greedy = cost / len(solutionlist_rand) / 2

    end = time()
    print(f"Computing Time: {end - start}\n")


    print("GA:")
    start = time()
    solutionlist_ga = ga(demandlist, rmfs)
    storage, cost = rmfs.run(demandlist, solutionlist_ga)
    print_stats(storage, cost, len(demandlist))

    all_results.cost_greedy = cost
    all_results.avg_cost_greedy = cost / len(solutionlist_rand) / 2

    end = time()
    print(f"Computing Time: {end - start}\n")

    resultlist.append(copy.copy(all_results))


if __name__ == '__main__':
    resultlist = []
    for i in range(3):  # Iterates the three demandlists and executes main() with them
        print(f">> Demandlist {i}")
        main(i+1)
    createOutput(resultlist)
