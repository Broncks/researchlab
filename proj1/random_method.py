import random
from proj1.inputOutput import *
from proj1.compTime import *

class results():
    numEntries = 0

    def __init__(self, result, compTime, perOfOpt): #Konstruktor
        self.result = result
        self.compTime = compTime
        self.perOfOpt = perOfOpt
        results.numEntries += 1

def random_method(capacity, weights, values):

    numOfItems = len(values)
    value = 0
    listvw = [[v , w] for v, w in zip(values, weights)] #zip values and weights into one list togehter
    random.shuffle(listvw) #after the zip command, the list is shuffled randomly

    while capacity > 0 and numOfItems > 0: #as long as the capacity is over 0 and there are more than 0 items
        counter = None
        for i in range(numOfItems): # going through all Items
            counter = i

        if counter is None: #if the list is empty
            return 0

        v = listvw[counter][0] #picks the value, cause v should be the value
        w = listvw[counter][1] #picks the weight, cause w is equal to the weight

        if w <= capacity:
            value += v #adds v to the value
            capacity -= w #on the other side the weight should reduce the capacity until the capacity is 0
        else:
            break

        listvw.pop(counter) #deletes the counter out of the list
        numOfItems -= 1 #therefore the itemnumber is reduced by -1

    return value


def createRandomResults():
    randomResults = []
    dataSetList = createDataSets()

    for i in range(len(dataSetList)):
        trackTime = ComputingTime()
        trackTime.computingTimeStart()

        capacity = int(dataSetList[i].knapsack_cap)
        weights = list(map(int, dataSetList[i].weightItems))
        values = list(map(int, dataSetList[i].valItems))

        randomValue = random_method(capacity, weights, values)
        print("Random Value: ", randomValue)

        compTime = trackTime.giveComputingTimeAndStop()
        print("Computing Time: ", compTime)

        optima = int(dataSetList[i].optima)
        perOfOpt = randomValue / optima
        print("Prozent vom Optimum: ", perOfOpt)

        randomResults.append([results(randomValue, compTime, perOfOpt)]) #append results to list

    return randomResults

