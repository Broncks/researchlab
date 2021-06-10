import numpy as np


def aco(rmfs, demandlist, rand_solutionlist):
    """
        Performs Ant Colony Optimization (ACO) heuristic to find a solution

        Args:
            rmfs (warehouse): Warehouse
            demandlist (list): List of demanded pods (-> one pod per iteration)
            rand_solutionlist (list): list based on random algorithm used as initial solution
                                      (-> one pod return place per iteration)

        Return:
            best_solutionlist (list): List of pod return places of ACO heuristic
                                      (-> one pod return place per iteration)
    """

    """Static parameters"""
    ANT_POPULATION = 25
    MAX_ITERATIONS = 100
    EVAPORATION_FACTOR = 0.8
    MAX_PLACE = 4

    best_solutionlist = rand_solutionlist.copy()
    pheromonelist = np.full((len(demandlist), MAX_PLACE), 1000.0)  # initTrails(demandlist)

    colony = Colony(rmfs, pheromonelist, demandlist, ANT_POPULATION, EVAPORATION_FACTOR, MAX_PLACE)

    iterations = 0
    while iterations < MAX_ITERATIONS:
        print(f'Iteration: {iterations+1}')
        solutionlist = colony.iterate()
        storage_sl, cost_sl = rmfs.run(demandlist, solutionlist)
        storage_best, cost_best = rmfs.run(demandlist, best_solutionlist)

        if cost_sl < cost_best:
            best_solutionlist = solutionlist
        iterations += 1
    return best_solutionlist


class Ant:
    def __init__(self, wl, dl, MAX_PLACE):  # Constructor
        """
            Creates and initializes Ant() object

            Args:
                wl (list): Weightlist which contains the percentages of a cell being picked
                dl (list): Demandlist of demanded pods (-> one pod per iteration)
                MAX_PLACE (int): Limits highest possible solution value in heuristic
        """
        self.weightlist = wl
        self.demandlist = dl.copy()
        self.MAX_PLACE = MAX_PLACE

    def create_solution(self, weightlist):
        """
            Creating a solution for this ant to return to the colony

            Args:
                weightlist (list): Weightlist which contains the percentages of a cell being picked
                
            Returns:
                ant_solution (list): Solutionlist created by ant
        """
        ant_solution = []
        for i in range(len(weightlist)):
            ant_solution.append(np.random.choice(range(self.MAX_PLACE), p=weightlist[i]))
        return ant_solution


class Biene:
    def __init__(self):
        """
            Creates and initializes Biene() object
        """
        self.name = "Maja"


class Colony:
    def __init__(self, rmfs, pl, dl, ANT_AMOUNT, EVAPORATION_FACTOR, MAX_PLACE):  # Constructor
        """
            Creates and initializes Colony() object

            Args:
                rmfs (warehouse): Warehouse
                pl (list): Pheromonelist containing pheremone scores for every cell
                dl (list): Demandlist of demanded pods (-> one pod per iteration)
                ANT_AMOUNT (int): Number of ants spawned by Colony
                EVAPORATION_FACTOR (float): Factor between 0 and 1 influencing phermone evaporation
                MAX_PLACE (int): Limits highest possible solution value in heuristic
        """
        self.warehouse = rmfs
        self.pheromonelist = pl
        self.demandlist = dl
        self.ANT_AMOUNT = ANT_AMOUNT
        self.EVAPORATION_FACTOR = EVAPORATION_FACTOR
        self.MAX_PLACE = MAX_PLACE
        self.BIENE = Biene()

        self.weightlist = self.weight_to_prob(self.pheromonelist)  # Conversion of pheromones to percentages

        self.ant_list = []
        for i in range(ANT_AMOUNT):  # Spawning the ants
            self.ant_list.append(Ant(self.weightlist, self.demandlist, self.MAX_PLACE))

    def iterate(self):
        """
            Iterates the Colony by letting the ants create and return their solutions

            Returns:
                best_solution (list): Best solution of all ants from current iteration
        """
        all_solutions = []
        cost_list = []
        for i in range(len(self.ant_list)):  # Calculating the cost for all solutions
            all_solutions.append(self.ant_list[i].create_solution(self.weightlist))
            storage, cost = self.warehouse.run(self.demandlist, all_solutions[i])
            cost_list.append(cost)

        cost_list_sorted = sorted(zip(cost_list, all_solutions))  # Sorting solutions by cost
        best_solution_zip = cost_list_sorted[0]
        cost, solution = best_solution_zip
        best_solution = solution

        self.update_pheromones(all_solutions, cost_list)
        self.weightlist = self.weight_to_prob(self.pheromonelist)  # Updating the weight list with current pheromones
        return best_solution

    def weight_to_prob(self, pl):
        """
            Converts the weights to percentages

            Args:
                pl (list): Pheromonelist contains the current pheromone values

            Return:
                weightlist (list): Weight list with values in percent
        """
        weightlist = pl.copy()

        for i in range(len(weightlist)):
            sum = 0
            for item in weightlist[i]:
                sum += item
            for j in range(len(weightlist[i])):
                weightlist[i][j] = weightlist[i][j] / sum
        return weightlist

    def update_pheromones(self, all_solutions, cost_list):
        """
            Converts the weights to percentages

            Args:
                all_solutions (list): All solutions created by the ants
                cost_list (list): List of costs for all solutions
        """
        master_table = np.full((len(self.demandlist), self.MAX_PLACE), 0)  # Table stores number of usages of each cell
        for pw in all_solutions:
            for i in range(len(pw)):
                master_table[i][pw[i]] += 1

        for i in range(len(master_table)):  # Calculating the cost of all solutions using the cell[i][j]
            for j in range(len(master_table[i])):
                sum_cost = 0
                for k in range(len(all_solutions)):
                    if all_solutions[k][i] == j:
                        sum_cost += cost_list[k]

                self.pheromonelist[i][j] = (1 - self.EVAPORATION_FACTOR) * self.pheromonelist[i][j] \
                                           + self.EVAPORATION_FACTOR * sum_cost  # May not be correct ❌
                self.pheromonelist[i][j] = round(self.pheromonelist[i][j])
