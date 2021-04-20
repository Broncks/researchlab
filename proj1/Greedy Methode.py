
def greedy_method(capacity, weights, values):
    value = 0.
    numOfItems = len(values)

    valuePerWeight = sorted([[v / w, w] for v, w in zip(values, weights)], reverse = True)
    # sort = sortiert die Funktion eine übergebene Liste mit Zahlen einfach der Größe nach
    # berechnen der Verhältnisse und abspeichern in valuePerWeight
    # Reverse = True sortiert die Liste in absteigender Reihenfolge
    # Normalfall Reverse = False: sortiert die Liste in aufsteigender Reihenfolge
    # Bedeutet hier, durch Reverse = True, dass der höchste Wert zuerst steht!

    while capacity > 0 and numOfItems > 0:
        max = 0
        counter = None
        for i in range(numOfItems):  # Länge der Liste
            if valuePerWeight[i][1] > 0 and max < valuePerWeight[i][0]:
                # Bedingung: Gewicht muss größer als 0 und der max muss kleiner als das Verhältnis sein
                # Durchlaufen der Liste und suchen nach dem besten Verhältnis
                max = valuePerWeight[i][0]
                counter = i

        if counter is None:
            return 0. # falls Liste leer bzw. alle Werte 0

        v = valuePerWeight[counter][0] # v = Verhältnis (value/weight)
        w = valuePerWeight[counter][1] # w = Gewicht (weight)

        if w <= capacity:
            value += v * w # Wert des Knapstack aufsummieren
            capacity -= w # Gesamtgewicht des Knapsack vermindern
        else:
            if w > 0:
                value += capacity * v  # anteilige Übertragung des Values auf den Knapstack hinzurechnen
                # fraglich, ob wir das machen sollen
                return value

        valuePerWeight.pop(counter)
        numOfItems -= 1

    return value


if __name__ == '__main__':
    n = 10
    capacity = 269

    values = [55, 10, 47, 5, 4, 50, 8, 61, 85, 87]
    weights = [95, 4, 60, 32, 23, 72, 80, 62, 65, 46]

    opt_value = greedy_method(capacity, weights, values)
    print(opt_value)




   