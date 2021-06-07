solutionlist =

for eachline in solutionList:
    eachPheromoneLineUpdate1 = time.time()
    if costDelta > 0:
        pheromoneTable[i][eachline] += ((bestCost / bestAntCost) ** 2) * 1000
    i += 1