# pi describes a particular problem instance
# tau = Pheromone concentration
# h = Heuristic function for the pheromone update
# TODO: Parallelization (one ant one thread) & Synchronization

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
