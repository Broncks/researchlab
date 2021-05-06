from proj2.simulated_annealing import *
import pprint
import numpy


def sa_split(rmfs, demandlist, solutionlist, cost_random):

    solutionlist_split = list(divide_chunks(solutionlist, 10))
    demandlist_split = list(divide_chunks(demandlist, 10))

    #print("Sol list: ", solutionlist_split)
    print("dem list: ", demandlist_split)

    #test_demandlist = [(4, 0), (13, 0), (12, 0), (5, 0), (11, 1), (9, 1), (8, 1), (6, 0), (14, 0), (13, 0)]
    #test_solutionlist = [2, 3, 8, 9, 6, 6, 7, 8, 3, 9]
    #test_demandlist2 = [(0, 0), (13, 1), (14, 0), (5, 0), (10, 1), (12, 0), (8, 0), (14, 0), (11, 0), (12, 1)]
    #test_solutionlist2 = [1, 1, 7, 8, 0, 3, 7, 5, 6, 8]

    split_counter = 0
    #for i in range(1):
    for i in demandlist_split:
        print("split_counter ", split_counter)
        #print("demandlist_split: ", demandlist_split[split_counter])
        #print("solutionlist_split: ", solutionlist_split[split_counter])

        simulated_annealing(rmfs, demandlist_split[split_counter], solutionlist_split[split_counter], 200000)

        #simulated_annealing(rmfs, test_demandlist, test_solutionlist, 200000)

        #simulated_annealing(rmfs, test_demandlist2, test_solutionlist2, 200000)

        split_counter += 1


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]
