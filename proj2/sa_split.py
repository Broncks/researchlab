from proj2.simulated_annealing import *
import pprint
import numpy

def sa_split(rmfs, demandlist, solutionlist, cost_random):




    demandlist_split = numpy.array_split(demandlist, 1000) #1000 10er listen erstellt aus demandlist
    solutionlist_split = numpy.array_split(solutionlist, 1000)

    n = numpy.arange(1)
    print(n)
    split_counter = 0
    for i in solutionlist_split:

        simulated_annealing(rmfs, demandlist_split[split_counter], solutionlist_split[split_counter], 200000)
        split_counter += 1

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]