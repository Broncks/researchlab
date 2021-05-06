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
            neighbor_list.append(i + np.random.choice([-1, 0, 1], p=[0.8, 0.1, 0.1]))
        elif i == 3:
            neighbor_list.append(i + np.random.choice([-1, 0, 1], p=[0.8, 0.1, 0.1]))
        else:
            neighbor_list.append(i + np.random.choice([-1, 0, 1], p=[0.9, 0.05, 0.05]))
    return neighbor_list
