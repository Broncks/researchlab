# pi describes a particular problem instance = Demandlist???
# tau = Pheromone concentration
# h = Heuristic function for the pheromone update
# TODO: Parallelization (one ant one thread) & Synchronization
import numpy as np


def aco(rmfs, demandlist, rand_solutionlist):
    ANT_POPULATION = 25
    MAX_ITERATIONS = 10  # 100
    EVAPORATION_FACTOR = 0.8
    MAX_PLACE = 4

    solutionlist = []
    best_solutionlist = rand_solutionlist.copy()
    pheromonelist = np.full((len(demandlist), MAX_PLACE), 1000.0)  # initTrails(demandlist)

    colony = Colony(rmfs, pheromonelist, demandlist, ANT_POPULATION, EVAPORATION_FACTOR, MAX_PLACE)

    iterations = 0
    while iterations < MAX_ITERATIONS:
        print(f'Iteration: {iterations}')
        print(pheromonelist)
        solutionlist = colony.iterate()
        storage_sl, cost_sl = rmfs.run(demandlist, solutionlist)
        storage_best, cost_best = rmfs.run(demandlist, best_solutionlist)

        if cost_sl < cost_best:
            best_solutionlist = solutionlist
        iterations += 1
    print(best_solutionlist)
    return best_solutionlist


class Biene:
    def __init__(self):
        self.name = "Maja"


class Ant:
    def __init__(self, wl, dl, MAX_PLACE):  # Konstruktor
        self.weightlist = wl
        self.demandlist = dl.copy()
        self.MAX_PLACE = MAX_PLACE
        print("Ameise!")

    def createSolution(self, weightlist):
        pissweg = []
        for i in range(len(weightlist)):
            pissweg.append(np.random.choice(range(self.MAX_PLACE), p=weightlist[i]))
        return pissweg


class Colony:
    def __init__(self, rmfs, pl, dl, ANT_AMOUNT, EVAPORATION_FACTOR, MAX_PLACE):  # Konstruktor
        self.warehouse = rmfs
        self.pheromonelist = pl
        self.demandlist = dl
        self.ANT_AMOUNT = ANT_AMOUNT
        self.EVAPORATION_FACTOR = EVAPORATION_FACTOR
        self.MAX_PLACE = MAX_PLACE

        self.weightlist = self.weight_to_prob(self.pheromonelist)

        self.ant_list = []
        for i in range(ANT_AMOUNT):
            self.ant_list.append(Ant(self.weightlist, self.demandlist, self.MAX_PLACE))

    def iterate(self):
        pisswege = []
        cost_list = []
        for i in range(len(self.ant_list)):
            pisswege.append(self.ant_list[i].createSolution(self.weightlist))
            storage, cost = self.warehouse.run(self.demandlist, pisswege[i])
            cost_list.append(cost)
        print("Costlist:", sorted(cost_list))
        print("Solution WL:", self.weightlist)

        cost_list_sorted = sorted(zip(cost_list, pisswege))  # descending order
        best_solution_zip = cost_list_sorted[0]
        cost, solution = best_solution_zip  # TODO: Irgendein Error, Listen trennen
        best_solution = solution

        self.update_pheromones(pisswege, cost_list)
        self.weightlist = self.weight_to_prob(self.pheromonelist)
        return best_solution

    def weight_to_prob(self, pl):
        """
            Converts the weights to percentages

            Args:
                weight_list (list): Contains the current weights for either the repair or destroy methods

            Return:
                wl (list): Weight list with values in percent
        """
        weightlist = pl.copy()

        for i in range(len(weightlist)):
            sum = 0
            for item in weightlist[i]:
                sum += item
            for j in range(len(weightlist[i])):
                weightlist[i][j] = weightlist[i][j] / sum
        return weightlist

    def update_pheromones(self, pisswege, cost_list):
        master_table = np.full((len(self.demandlist), self.MAX_PLACE), 0)
        for pw in pisswege:
            for i in range(len(pw)):
                master_table[i][pw[i]] += 1

        for i in range(len(master_table)):
            for j in range(len(master_table[i])):
                # print(f'Zelle: [{i}][{j}]')
                sum_cost = 0
                for k in range(len(pisswege)):
                    if pisswege[k][i] == j:
                        sum_cost += cost_list[k]
                # print(f'[{i}][{j}] Sumcost: {sum_cost}')

                self.pheromonelist[i][j] = (1 - self.EVAPORATION_FACTOR) * self.pheromonelist[i][j]\
                                           + self.EVAPORATION_FACTOR * sum_cost
                self.pheromonelist[i][j] = round(self.pheromonelist[i][j])
                # SUMME ALLER KOSTEN DER LÖSUNGEN (f(s) IN EINEM FELD i,j) OR 0
