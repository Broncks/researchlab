
from proj1.compTime import *
from proj1.input import *


class Results:
    numEntries = 0

    def __init__(self, result, compTime, perOfOpt): #Konstruktor
        self.result = result
        self.compTime = compTime
        self.perOfOpt = perOfOpt
        Results.numEntries += 1


def greedy_method(capacity, weights, values):
    value = 0
    numOfItems = len(values) #length of list

    valuePerWeight = sorted([[v / w, w] for v, w in zip(values, weights)], reverse = True) #descending order
    # print(valuePerWeight) #list with all ratios and respective weights
    #Könnten wir im finalen Programm mögl. rauslassen, aber als Übersicht eig ganz gut geeignet

    while capacity > 0 and numOfItems > 0:
        max = 0
        counter = None
        for i in range(numOfItems):  #length of list
            if valuePerWeight[i][1] > 0 and max < valuePerWeight[i][0]:
                max = valuePerWeight[i][0]
                counter = i

        if counter is None:
            return 0 #empty list or weight or value egual zero

        v = valuePerWeight[counter][0] #v = ratio (value/weight)
        w = valuePerWeight[counter][1] #w = weight

        if w <= capacity: #check for potential capacity
            value += v * w #sum up value
            capacity -= w #reduce capacity by weight
        else:
            break

        valuePerWeight.pop(counter)
        numOfItems -= 1

    return value

def createGreedyResults():
    greedyResults = []
    dataSetList = createDataSets()

    for i in range(len(dataSetList)):
        trackTime = ComputingTime()
        trackTime.computingTimeStart()

        capacity = int(dataSetList[i].knapsack_cap)
        weights = list(map(int, dataSetList[i].weightItems))
        values = list(map(int, dataSetList[i].valItems))

        print("")
        print("Berechnung ", i+1, " Greedy")

        greedyValue = greedy_method(capacity, weights, values)
        print("Greedy Value: ", greedyValue)

        compTime = trackTime.giveComputingTimeAndStop()
        print("Computing Time: ", compTime)

        optima = int(dataSetList[i].optima)
        perOfOpt = greedyValue / optima
        print("Prozent vom Optimum: ", perOfOpt)

        greedyResults.append(Results(greedyValue, compTime, perOfOpt)) #append results to list

    return greedyResults




