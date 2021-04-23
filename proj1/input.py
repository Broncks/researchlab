def createDataSets():
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

    optima_list = [
        "../proj1/optima/f1_l-d_kp_10_269.txt",
        "../proj1/optima/f2_l-d_kp_20_878.txt",
        "../proj1/optima/f3_l-d_kp_4_20.txt",
        "../proj1/optima/f4_l-d_kp_4_11.txt",
        "../proj1/optima/f6_l-d_kp_10_60.txt",
        "../proj1/optima/f7_l-d_kp_7_50.txt",
        "../proj1/optima/f8_l-d_kp_23_10000.txt",
        "../proj1/optima/f9_l-d_kp_5_80.txt",
        "../proj1/optima/f10_l-d_kp_20_879.txt"
    ]

    for i in range(len(input_list)):
        print("Liste wird erzeugt mit: ", input_list[i], "und ", optima_list[i])
        dataSetList.append(DataSet(input_list[i], optima_list[i]))
    print()

    return dataSetList


class DataSet:

    def __init__(self, filePath_input, filePath_optima):
        self.valItems = []
        self.weightItems = []
        self.num_of_items = 0
        self.knapsack_cap = 0
        self.file = filePath_input
        self.optimaPath = filePath_optima
        self.optima = 0

        with open(filePath_input, "r") as file:

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

        with open(filePath_optima, "r") as file:
            for line in file:
                self.optima = line