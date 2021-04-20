from proj1.inputOutput import createDataSets

if __name__ == "__main__":

    dataSetList = createDataSets()
    print(dataSetList)
    print("ValItems Eintrag 1 aus Inputfiles 1", dataSetList[0].valItems[0])
    print("WeightItems Eintrag 6 aus Inputfiles 3", type(dataSetList[2].weightItems[3]))
    print("num_of_items aus Inputfiles 3", type(dataSetList[2].num_of_items))
    print("knapsack_cap aus Inputfiles 3", dataSetList[2].knapsack_cap)


