import numpy as np
from collections import deque

class RMFS:
    """Model of RMFS warehouse"""

    def __init__(self, initstorage, ppods, nplaces, nstations, qsize):
        """
        Instantiate Warehouse

        Args:
            initstorage (collection): Initial state of the storage
            ppods (float): Fraction of storage places that are initially occupied by pods
            nplaces (int): Number of storage places
            nstations (int): Number of stations
            qsize (int): Maximum number of pods in each stations queue
        """
        self.npods = int(ppods*nplaces)
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

        # Simulating pods moving to and from stations according to demandlist
        for demand, solution in zip(demandlist, solutionlist):
            storage, cost = self.remove_pod_from_storage(storage, demand[0], cost)
            queues, returning_pod = self.remove_pod_from_queue(queues, demand[1])
            storage, cost = self.move_pod_to_storage(storage, returning_pod, cost, solution)
            queues = self.move_pod_to_station(queues, demand[0], demand[1])

        return storage, cost

    def remove_pod_from_storage(self, storage, pod, cost):
        """Remove specified pod from storage area, then update cost"""

        cost += np.where(storage == pod)[0][0]+1 
        storage = np.asarray([-1 if p == pod else p for p in storage])

        return storage, cost

    def remove_pod_from_queue(self, queues, station):
        """Remove oldest pod from the specified stations queue"""

        returning_pod = queues[station].pop()

        return queues, returning_pod

    def move_pod_to_storage(self, storage, returning_pod, cost, solution):
        """Move returning pod back to storage and update cost"""

        if(returning_pod != -1):
            free_storage = np.where(storage == -1)[0]
            place = free_storage[solution]
            storage[place] = returning_pod
            cost += place + 1

        return storage, cost
        
    def move_pod_to_station(self, queues, pod, station):
        """Append demanded pod to station queue"""
        
        queues[station].appendleft(pod)

        return queues
