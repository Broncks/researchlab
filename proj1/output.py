import xlsxwriter as xs


def createOutput(greedyResultsList, randomResultsList):
    outWorkbook = xs.Workbook("outputfiles/output.xlsx")
    outWorksheet = outWorkbook.add_worksheet()

    greedyResultsList[0].result

    outWorksheet.write(0, 0, "Instance")
    outWorksheet.write(0, 1, "Results Random")
    outWorksheet.write(0, 2, "Computing Time (sec)")
    outWorksheet.write(0, 3, "% of Optimum")
    outWorksheet.write(0, 4, "Results Greedy")
    outWorksheet.write(0, 5, "Computing Time (sec)")
    outWorksheet.write(0, 6, "% of Optimum")
    outWorksheet.write(0, 7, "Optimum")

    outWorksheet.write(1, 0, "f1")
    outWorksheet.write(2, 0, "f2")
    outWorksheet.write(3, 0, "f3")
    outWorksheet.write(4, 0, "f4")
    outWorksheet.write(5, 0, "f6")
    outWorksheet.write(6, 0, "f7")
    outWorksheet.write(7, 0, "f8")
    outWorksheet.write(8, 0, "f9")
    outWorksheet.write(9, 0, "f10")

    outWorksheet.write(1, 7, "295")
    outWorksheet.write(2, 7, "1024")
    outWorksheet.write(3, 7, "35")
    outWorksheet.write(4, 7, "23")
    outWorksheet.write(5, 7, "52")
    outWorksheet.write(6, 7, "107")
    outWorksheet.write(7, 7, "9767")
    outWorksheet.write(8, 7, "130")
    outWorksheet.write(9, 7, "1025")

    for i in range(len(greedyResultsList)):
        outWorksheet.write(i + 1, 1, randomResultsList[i].result)
        outWorksheet.write(i + 1, 2, randomResultsList[i].compTime)
        outWorksheet.write(i + 1, 3, round(randomResultsList[i].perOfOpt*100, 2))

        outWorksheet.write(i + 1, 4, greedyResultsList[i].result)
        outWorksheet.write(i + 1, 5, greedyResultsList[i].compTime)
        outWorksheet.write(i + 1, 6, round(greedyResultsList[i].perOfOpt*100, 2))

    outWorkbook.close()
