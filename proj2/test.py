from time import time
from proj2.warehouse import RMFS
from proj2.simulated_annealing import *
from proj2.sa_plot import create_sa_plot


def read_demandlist(filename):
    demandlist = []
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
    print("Initial positions in storage: ", initstorage)
    print("Demandlist (given in task): ", demandlist)

    print("Random:")
    start = time()
    solutionlist_random = []
    # create solution list for random algorithm
    for i in range(10000):
        solutionlist_random.append(random.randint(0, 10))
    storage, cost_random = (rmfs.run(demandlist, solutionlist_random)) # run warehouse method
    print(storage, cost_random)
    end = time()
    print(f"Computing Time: {end - start}\n")

    print("Greedy:")
    start = time()
    solutionlist_greedy = []
    # create solution list for greedy algorithm
    for i in demandlist:
        solutionlist_greedy.append(0)
    storage_greedy, cost_greedy = rmfs.run(demandlist, solutionlist_greedy)
    print("Greedy Costs", cost_greedy)
    end = time()
    print(f"Computing Time: {end - start}\n")

    print("Simulated Annealing:")
    start = time()
    sa_solutionlist, iterations_list, cost_list = simulated_annealing(
        rmfs, demandlist, solutionlist_random, cost_random)
    create_sa_plot(cost_list, iterations_list) # create a scatterplot as visualisation
    storage, cost_sa = rmfs.run(demandlist, sa_solutionlist) # run warehouse method
    print(storage, cost_sa)
    end = time()
    print(f"Computing Time: {end - start}\n")

if __name__ == '__main__':
    main()
