import xlsxwriter as xs

def createDataSets():
    print("createDataSets")
    dataSetList = []
    input_list = [
        "../proj1/inputfiles/f1_l-d_kp_10_269.txt",
        "../proj1/inputfiles/f2_l-d_kp_20_878.txt",
        "../proj1/inputfiles/f3_l-d_kp_4_20.txt",
        "../proj1/inputfiles/f4_l-d_kp_4_11.txt",
        "../proj1/inputfiles/f6_l-d_kp_10_60.txt",
        "../proj1/inputfiles/f7_l-d_kp_7_50.txt",
        "../proj1/inputfiles/f8_l-d_kp_23_10000.txt",
        "../proj1/inputfiles/f9_l-d_kp_5_80.txt",
        "../proj1/inputfiles/f10_l-d_kp_20_879.txt"
    ]


    for i in range(len(input_list)):

        print("Liste wird erzeugt mit: ", input_list[i])
        dataSetList.append(DataSet(input_list[i]))

    return dataSetList

class DataSet:

    def __init__(self, filePath):
        self.valItems = []
        self.weightItems = []
        self.num_of_items = 0
        self.knapsack_cap = 0
        self.file = filePath

        with open(filePath, "r") as file:

            line_number = 0

            for line in file:
                p = line.split()
                if line_number == 0:
                    self.num_of_items = p[0]
                    self.knapsack_cap = p[1]
                else:
                    self.valItems.append(p[0])
                    self.weightItems.append(p[1])
                line_number += 1

        file.close()

        #print("values of items", self.valItems)
        #print("weight of items ", self.weightItems)
        #print("num_of_items ", num_of_items)
        #print("knapsack_cap ", knapsack_cap)


if __name__ == "__main__":
    # TODO write class/function for output
    outWorkbook = xs.Workbook("output.xlsx")
    outWorksheet = outWorkbook.add_worksheet()

    # for i in range(len(knapsack_vars)):
    #    knapsack_vars[i] = knapsack_vars[i][:-1]

    outWorksheet.write(0, 0, "Instance")
    outWorksheet.write(0, 1, "Results Random")
    outWorksheet.write(0, 2, "Computing Time")
    outWorksheet.write(0, 3, "% of Optimum")
    outWorksheet.write(0, 4, "Results Greedy")
    outWorksheet.write(0, 5, "Computing Time")
    outWorksheet.write(0, 6, "% of Optimum")
    outWorksheet.write(0, 7, "Optimum")
    # TODO optimizing: Array + Loop

    # for i in range(len(movies)):
    #
    #     outWorksheet.write(i, 0, movies[i][:-4])
    #     outWorksheet.write(i, 1, movies[i][-4:])

    outWorkbook.close()
