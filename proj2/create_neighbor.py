import numpy as np


def create_neighbor_list(best_solution):
    neighbor_list = []
    # Hohe Werte dekrementieren
    # 0-Werte beibehalten oder Inkrementieren
    # Alle anderen werte entweder beibehalten, inkrementieren oder dekrementieren

    for i in best_solution:
        if i >= 5:
            neighbor_list.append(i - 4)

        elif i == 0:
            neighbor_list.append(i + np.random.choice([-1, 0, 1], p=[0.0, 0.50, 0.50]))
        elif i == 1:
            neighbor_list.append(i + np.random.choice([-1, 0, 1], p=[0.50, 0.25, 0.25]))
        elif i == 2:
            neighbor_list.append(i + np.random.choice([-1, 0, 1], p=[0.4, 0.4, 0.2]))
        else:

            neighbor_list.append(i + np.random.choice([-1, 0, 1], p=[0.45, 0.45, 0.1]))
    return neighbor_list
