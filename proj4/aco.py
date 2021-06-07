# pi describes a particular problem instance
# tau = Pheromone concentration
# h = Heuristic function for the pheromone update
# TODO: Parallelization (one ant one thread) & Synchronization
import random
import multiprocessing as mp
import numpy as np


pheromonlist = np.full((10000, 4), 1000)
print('Wacka wacka', pheromonlist[500][3])

def aco(rmfs, pi, h, f):
    solutionlist = []
    best_solutionlist = []  # Ist das wirklich eine leere Liste? Siehe Folie 14/29 Zeile 2
    tau = initTrails(pi)

    while not terminate(pi, solutionlist):
        solutionlist = construct(pi, tau, h)
        solutionlist = localSearch(pi, solutionlist)  # Optional, but recommended
        if best(pi, solutionlist) < cost(best_solutionlist):  # TODO: Implement cost calculation f(s*)
            best_solutionlist = best(pi, solutionlist)
        tau = updateTrails(pi, solutionlist, tau)


def initTrails(pi):
    pass

def terminate(pi, s):
    return bool

def construct(pi, tau, h):
    pass

def localSearch(pi, s):
    pass

def best(pi, s):
    pass

def updateTrails(pi, s, tau):
    pass






    """
    processes = []
    manager = mp.Manager()
    colonyResult = manager.list()

    for _ in range(antPopulation):
        ant = Ant([])
        p = mp.Process(target=ant.createSolution())
        processes.append(p)
        p.start()

    for process in processes:
        process.join()"""



class Ant:
    def __init__(self, pheromone_list):  # Konstruktor
        self.pl = pheromone_list.copy()
        print("Ameise!")

    def createSolution(self):
        pissweg = [random.randint(0, 3) for i in range(10000)]
        print("pissweg:", pissweg)
        return pissweg


class Colony:
    ant_amount = 20
    ant_list = []
    for i in range(ant_amount):
        ant_list.append(Ant(pheromonlist))


if __name__ == '__main__':

    """
    Colony()
    ant = Ant([])
    ant.createSolution()"""
