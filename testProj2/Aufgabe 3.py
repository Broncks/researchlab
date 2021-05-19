import numpy as np
from collections import deque


def initialise_demand_list():
    """
    Open the file and create a list of demand from it

    Returns:
        demandlist list((int,int)):     List of tupels
    """




    demandlist = []
    # WRITE YOUR CODE HERE
    with open('demandlist.txt', "r") as file:
        for line in file:
            p = line.split()
            demandlist.append((int(p[0]), int(p[1])))
    file.close()
    return demandlist


def calculate_pod_probability(demandlist, npods):
    """
    Count all Pod occurences to calculate each pods probability

    Args:
        demandlist list((int,int)):     List which contains the simulations demand
        npods (int):                    Number of pods
    Returns:
        pod_probability list(float):    List of tupels

    """

    demand_counter = np.repeat(0, npods)

    for eachpod in demandlist:
        demand_counter[eachpod[0]] = demand_counter[eachpod[0]] + 1

    pod_probability = demand_counter / len(demandlist)

    return pod_probability


def find_returning_pods(demandlist, nstations, qsize):
    """
    Simulate queues to create a list of returning pods

    Args:
        demandlist list((int,int)):     List which contains the simulations demand
        nstations (int):                Number of stations
        qsize (int):                    Length of each stations queue

    Returns:
        returning_pods list(int):       List of returning pods
    """

    queues = {}

    for i in range(nstations):
        queues.update({i: deque([])})
        for x in range(qsize):
            queues[i].append(-1)
        i = i + 1

    returning_pods = []

    for (stationdemand, eachstation) in demandlist:
        returning_pods.append(queues[eachstation][-1])
        queues[eachstation].pop()
        queues[eachstation].appendleft(stationdemand)

    return returning_pods


def create_relevance_index(returning_pods, pod_probability):
    """
    Show relevancy of each returning pod with an index to a returning place which fits each pods probability
    (Low Probability Pods get more expensive places)

    Args:
        returning_pods list(int):       List which contains the simulations demand
        pod_probability list(float):    List containing probability of appearance for each pod

    Returns:
        pod_relevance list(int):        List of relevancy for each returning pod

    """

    pod_probability_sorted = np.sort(pod_probability)[::-1]
    pod_relevance = []
    for eachrow in returning_pods:
        pod_relevance.append(np.where(pod_probability[eachrow] == pod_probability_sorted)[0][0])

    return pod_relevance


def find_best_returning_place(demandlist, pod_relevance, most_expensive_solution, npods):
    """
    Calculating the final solution by mapping the index of relevance to the n-cheapest returning place.
    With n between 0 and 'most_expensive_solution'.

    Args:
        demandlist list((int,int)):     List which contains the simulations demand
        pod_relevance list(int):        List of relevancy for each returning pod
        most_expensive_solution (int):  Most expensive returning place to be possible as solution
        npods (int):                    Number of pods

    Returns:
        result_list list(int):          solutionlist to be written into a file

    """

    result_list = []
    for eachrow, x in zip(demandlist, pod_relevance):
        result_list.append(int(x / npods * (most_expensive_solution)))

    return result_list


def generate_solutionfile(file_path, result_list):
    """
    Create the solution file from the list which contains the calculated solution

    Args:
        result_list list(int):          solutionlist to be written into a file
        file_path (string):             path pointing to the solution file

    """
    oursolution = open(file_path, "a+")
    for eachsolution in result_list:
        solution = str(eachsolution)
        oursolution.write(solution)
        oursolution.write('\n')
    oursolution.close

if __name__ == "__main__":
    npods = 15
    nstations = 2
    qsize = 3
    max_placeid = 11
    lowest_solution = 3

    solution_path = "oursolution.txt"

    demandlist = initialise_demand_list()
    pod_probability = calculate_pod_probability(demandlist, npods)
    pod_relevance = create_relevance_index(find_returning_pods(demandlist, nstations, qsize), pod_probability)
    result = find_best_returning_place(demandlist, pod_relevance, lowest_solution, npods)

    generate_solutionfile(solution_path, result)

