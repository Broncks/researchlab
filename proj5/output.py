import xlsxwriter as xs


def createOutput(resultlist):
    outWorkbook = xs.Workbook("outputfiles/output.xlsx")
    outWorksheet = outWorkbook.add_worksheet()
    outWorksheet.set_column(1, 6, 35)

    outWorksheet.write(0, 0, "Demandlist")
    outWorksheet.write(0, 1, "Total cost (Random)")
    outWorksheet.write(0, 2, "Average cost per pod movement (Random)")
    outWorksheet.write(0, 3, "Total cost (Greedy)")
    outWorksheet.write(0, 4, "Average cost per pod movement (Greedy)")
    outWorksheet.write(0, 5, "Total cost (GA)")
    outWorksheet.write(0, 6, "Average cost per pod movement (GA)")

    outWorksheet.write(1, 0, "1")
    outWorksheet.write(2, 0, "2")
    outWorksheet.write(3, 0, "3")

    for i in range(len(resultlist)):
        outWorksheet.write(i + 1, 1, resultlist[i].cost_random)
        outWorksheet.write(i + 1, 2, resultlist[i].avg_cost_random)

        outWorksheet.write(i + 1, 3, resultlist[i].cost_greedy)
        outWorksheet.write(i + 1, 4, resultlist[i].avg_cost_greedy)

        outWorksheet.write(i + 1, 5, resultlist[i].cost_aco)
        outWorksheet.write(i + 1, 6, resultlist[i].avg_cost_aco)

    outWorkbook.close()
