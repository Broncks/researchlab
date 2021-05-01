import numpy as np
from collections import deque
from time import time
from math import exp
import random


class Warehouse:
    """Model of RMFS warehouse"""

    def __init__(self, initstorage, ppods, nplaces, nstations, qsize):
        """
        Instantiate Warehouse

        Args:
            ppods (float): Fraction of storage places that are initially occupied by pods
            nplaces (int): Number of storage places
            nstations (int): Number of stations
            qsize (int): Maximum number of pods in each stations queue
        """
        self.npods = int(ppods * nplaces)
        self.nplaces = nplaces
        self.nstations = nstations
        self.qsize = qsize
        self.initstorage = np.asarray(initstorage)

    def run(self, demandlist, solutionlist):
        """
        Run Warehouse

        Args:
            demandlist (list((int, int))): List of (pod, station) tuples
            solutionlist (list(int)): List of pod return places
        """
        cost = 0
        queues = {k: deque(np.repeat(-1, self.qsize), self.qsize) for k in np.arange(self.nstations)}
        storage = self.initstorage

        for demand, solution in zip(demandlist, solutionlist):
            storage, cost = self.remove_pod_from_storage(storage, demand[0], cost)
            queues, returning_pod = self.remove_pod_from_queue(queues, demand[1])
            storage, cost = self.move_pod_to_storage(storage, returning_pod, cost, solution)
            queues = self.move_pod_to_station(queues, demand[0], demand[1])

        return storage, cost

    def remove_pod_from_storage(self, storage, pod, cost):
        """Remove specified pod from storage area, then update cost"""

        cost += (np.where(storage == pod)[0][0]) + 1
        storage = np.asarray([-1 if p == pod else p for p in storage])

        return storage, cost

    def remove_pod_from_queue(self, queues, station):
        """Remove oldest pod from the specified stations queue"""

        returning_pod = queues[station].pop()

        return queues, returning_pod

    def move_pod_to_storage(self, storage, returning_pod, cost, solution):
        """Move returning pod back to storage and update cost"""

        if (returning_pod != -1):
            free_storage = np.where(storage == -1)[0]
            place = free_storage[solution]
            storage[place] = returning_pod
            cost += place + 1

        return storage, cost

    def move_pod_to_station(self, queues, pod, station):
        """Append demanded pod to station queue"""

        queues[station].appendleft(pod)

        return queues


def create_neighbor(initial_return_place):
    """
    Generate a pod return place by changing the initial solutions value.

    Args:
        initial_solution (int): Initial return place

    Returns:
        neighbor_solution (int): Generated pod return place to create neighbor solution
    """

    new_return_index = np.random.choice([-1, 0, 1], p=[0.25, 0.7, 0.05])

    if initial_return_place + new_return_index >= max_placeid:
        new_return_place = initial_return_place + np.random.choice([-4, -5, -6, -7, -8])
    elif initial_return_place + new_return_index < 0:
        new_return_place = initial_return_place + np.random.choice([0, 1, 1, 1])
    else:
        new_return_place = initial_return_place + new_return_index

    if new_return_index > max_placeid / 2:
        new_return_index = new_return_index + np.random.choice([-1, -2, -3, -4])

    return new_return_place


def simulated_annealing(rmfs, demandlist, initsol, starttemp, mintemp, coolingfactor):
    """
    Generate a list of pod return places using simulated annealing

    Args:
        rmfs (Warehouse): Warehouse
        demandlist (list): Demand, 1 pod per iteration
        initsol (list): Initial solution, 1 pod return place per iteration
        starttemp (int): Initial temperature for SA
        mintemp (int): Perform SA until temp reaches this value
        coolingfactor (float): Coolingfactor for SA
    Returns:
        solutionlist (list): List of pod return places, 1 per iteration
    """

    solutionlist = initsol
    temperature = starttemp
    storage, best_cost = rmfs.run(demandlist, solutionlist)
    best_solution = solutionlist
    iterations = 0
    iterations_per_temp = 0
    storage, current_cost = rmfs.run(demandlist, solutionlist)

    while temperature > mintemp and iterations < 1000:
        neighbor_solutionlist = [create_neighbor(i) for i in best_solution]
        storage, new_cost = rmfs.run(demandlist, neighbor_solutionlist)
        delta = new_cost - current_cost

        if delta < 0 or exp(-(delta / temperature)) > random.uniform(0, 1):
            current_cost = new_cost
            solutionlist = neighbor_solutionlist

            if current_cost < best_cost:
                best_cost = current_cost
                best_solution = solutionlist

            iterations_per_temp += 1

            if iterations_per_temp > 10:
                temperature = temperature * coolingfactor

        iterations += 1

    return best_solution


def read_demandlist(filename):
    """
    Read a list of tuples from disk

    Args:
        filename (str): Path to file
    Returns:
        demandlist (list((int,int)))
    """

    demandlist = []
    with open("demandlist.txt") as inputfile:
        for line in inputfile:
            demandtuple = tuple(
                int(num) for num in line.replace('(', '').replace(')', '').replace('\n', '').split(', '))
            demandlist.append(demandtuple)

    return demandlist


def print_stats(storage, cost, steps):
    """Prints simulation results"""
    print(f"Storage Area: \n{storage}")
    print(f"Total cost: {cost}")
    print(f"Avg. cost per pod movement: {cost / steps / 2}")


ppods = .75
nplaces = 20
nstations = 2
qsize = 3

max_placeid = nplaces - int(ppods * nplaces) + nstations * qsize

initstorage = []
with open("initial_storage.txt") as inputfile:
    for line in inputfile:
        storage_place = int(line.replace('\n', ''))
        initstorage.append(storage_place)

demandlist = read_demandlist("demandlist.txt")

rmfs = Warehouse(initstorage, ppods, nplaces, nstations, qsize)

print("Random:")
solutionlist_rand = []
for eachrow in demandlist:
    solutionlist_rand.append(np.random.randint(max_placeid))

storage, random_cost = rmfs.run(demandlist, solutionlist_rand)
print_stats(storage, random_cost, len(demandlist))

print("Cheapest place:")
solutionlist_cheap = [0 for eachrow in demandlist]
storage, cost = rmfs.run(demandlist, solutionlist_cheap)
print_stats(storage, cost, len(demandlist))

print("File:")
solutionlist_file = []
with open("oursolution.txt") as inputfile:
    for line in inputfile:
        storage_place = int(line.replace('\n', ''))
        solutionlist_file.append(storage_place)
storage, custom_cost = rmfs.run(demandlist, solutionlist_file)
print_stats(storage, custom_cost, len(demandlist))

print("Simulated annealing:")
solutionlist = simulated_annealing(rmfs, demandlist, solutionlist_rand, random_cost * 1, 10, 0.90)
storage, cost = rmfs.run(demandlist, solutionlist)
print_stats(storage, cost, len(demandlist))