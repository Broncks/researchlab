from proj2.simulated_annealing import *
import pprint
import numpy


def sa_split(rmfs, demandlist, solutionlist, cost_random):
    demandlist_split = numpy.array_split(demandlist, 1000)  # 1000 10er listen erstellt aus demandlist
    solutionlist_split = numpy.array_split(solutionlist, 1000)
    print("demandlist_split: ", demandlist_split[0])
    testliste = []
    testliste[1]
    split_counter = 0
    for i in demandlist_split:
        print("split_counter ", split_counter)
        print("demandlist_split: ", demandlist_split[split_counter])
        print("solutionlist_split: ", solutionlist_split[split_counter])
        simulated_annealing(rmfs, demandlist_split[split_counter], solutionlist_split[split_counter], 200000)
        split_counter += 1


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
