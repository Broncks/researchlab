from random import *
import numpy as np

"""Static parameters"""
ITERATIONS = 100
POPULATION_SIZE = 40
NOOB_PERCENTAGE = 0.8
MAX_PLACE = 3
FITNESS_FACTOR = 5
NUM_OF_CHILDREN = int(POPULATION_SIZE * NOOB_PERCENTAGE)


def ga(demandlist, rmfs, init_cost):
    """
        Performs Genetic Algorithm (GA) to find a solution

        Args:
            demandlist (list): List of demanded pods (-> one pod per iteration)
            rmfs (warehouse): Warehouse
            init_cost (int): Cost of random solution

        Return:
            genelist (list): Solution list of pod return places of GA heuristic
                                      (-> one pod return place per iteration)
    """
    population = Population(demandlist, rmfs, NOOB_PERCENTAGE)
    avg_cost = init_cost
    prev_cost = init_cost+1
    latest_costs = []

    i = 0
    while avg_cost / prev_cost < 1 and i < ITERATIONS:
        population.create_children(NUM_OF_CHILDREN)  # Generate new set of children
        population.survivor_selection()

        latest_costs.append(population.get_best_solution())
        if i >= FITNESS_FACTOR:  # Not active for first n iterations
            latest_costs.pop(0)
            prev_cost = avg_cost
            avg_cost = 0
            for item in latest_costs:
                avg_cost += item
            avg_cost = avg_cost / FITNESS_FACTOR
        print("Bestsolution:", population.get_best_solution())
        print(f'Iteration {i + 1} – avg cost {avg_cost} – prev cost {prev_cost} – percentage {avg_cost / prev_cost}')

        i += 1

    population.chromosome_list.sort(key=lambda x: x.cost)
    return population.chromosome_list[0].genelist


class Population:

    def __init__(self, demandlist, rmfs, NOOB_PERCENTAGE: float):
        """
            Creates and initializes Population() object

            Args:
                demandlist (list): Demandlist of demanded pods (-> one pod per iteration)
                rmfs (warehouse): Warehouse
                NOOB_PERCENTAGE (int): Limits highest possible solution value in heuristic
        """
        self.rmfs = rmfs
        self.demandlist = demandlist
        self.chromosome_list = self.create_init_population(POPULATION_SIZE, demandlist, MAX_PLACE)
        self.best_solution = 0
        self.children_list = []
        self.NOOB_PERCENTAGE = NOOB_PERCENTAGE

    def get_best_solution(self):
        """
            Returns cost of best solution from current iteration

            Returns:
                best_solution (int): Cost of best solution from current iteration
        """
        return self.best_solution

    def create_init_population(self, population_size, demandlist, MAX_PLACE_ID):
        """
            Generates the initial chromosomes

            Args:
                population_size (int): Size of population
                demandlist (list): Demandlist of demanded pods (-> one pod per iteration)
                MAX_PLACE_ID (int): Limits highest possible solution value in heuristic

            Returns:
                chromosome_list (list): Initial chromosomes
        """
        chromosome_list = []
        for i in range(population_size):
            chromosome_list.append(
                Chromosome([randrange(0, MAX_PLACE_ID) for i in range(len(demandlist))], self.rmfs, demandlist))
        return chromosome_list

    def parent_selection(self):
        """
            Select parents with best fitness
            -> Tournament

            Returns:
                parent1 (chromosome): Chromosome of parent 1
                parent2 (chromosome): Chromosome of parent 2
        """

        candidate = []
        for i in range(4):
            candidate.append(self.chromosome_list[np.random.choice(len(self.chromosome_list))])

        if candidate[0].cost < candidate[1].cost:
            parent1 = candidate[0]
        else:
            parent1 = candidate[1]

        if candidate[2].cost < candidate[3].cost:
            parent2 = candidate[2]
        else:
            parent2 = candidate[3]

        return parent1, parent2

    def crossover(self, parent1, parent2):
        """
            Merge chromosomes of parents to create children
            -> One Point Crossover (Split in half)

            Args:
                parent1 (chromosome): Chromosome of parent 1
                parent2 (chromosome): Chromosome of parent 2

            Returns:
                children1 (chromosome): Chromosome of child 1
                children2 (chromosome): Chromosome of child 2
        """

        parent1half1 = parent1.genelist[:len(parent1.genelist) // 2]
        parent1half2 = parent1.genelist[len(parent1.genelist) // 2:]

        parent2half1 = parent2.genelist[:len(parent2.genelist) // 2]
        parent2half2 = parent2.genelist[len(parent2.genelist) // 2:]

        genelist1 = parent1half1 + parent2half2
        genelist2 = parent2half1 + parent1half2

        children1 = Chromosome(genelist1, self.rmfs, self.demandlist)
        children2 = Chromosome(genelist2, self.rmfs, self.demandlist)

        return children1, children2

    def mutation1(self, children1, children2):
        """
            Mutates children by randomly selecting a span and inverting the genes
            -> Inversion

            Args:
                children1 (chromosome): Chromosome of child 1
                children2 (chromosome): Chromosome of child 2

            Returns:
                children1 (chromosome): Mutated chromosome of child 1
                children2 (chromosome): Mutated chromosome of child 2

        """
        MUTATION_SPAN = 1000
        MUTATION_PROBABILITY = 0.5

        children_list = [children1, children2]

        for i in range(len(children_list)):

            mutation_starter = np.random.choice([0, 1], p=[1 - MUTATION_PROBABILITY, MUTATION_PROBABILITY])
            if mutation_starter == 1:
                mutation_pointer = np.random.choice(
                    range(MUTATION_SPAN, len(children_list[i].genelist) - MUTATION_SPAN))
                # Split in three parts of which the second one will be inversed
                children_list_part1 = children_list[i].genelist[0:mutation_pointer]

                children_list_part2 = list(
                    reversed(children_list[i].genelist[mutation_pointer - MUTATION_SPAN: mutation_pointer]))
                children_list_part3 = children_list[i].genelist[
                                      mutation_pointer + MUTATION_SPAN:len(children_list[i].genelist)]

                children_list[i].genelist = children_list_part1 + children_list_part2 + children_list_part3
                children_list[i].recalc_fitness()

        children1 = children_list[0]
        children2 = children_list[1]
        return children1, children2

    def mutation2(self, children1, children2):
        """
            Mutates children by randomly selecting a span and randomizing the genes
            -> Bit flipping

            Args:
                children1 (chromosome): Chromosome of child 1
                children2 (chromosome): Chromosome of child 2

            Returns:
                children1 (chromosome): Mutated chromosome of child 1
                children2 (chromosome): Mutated chromosome of child 2

        """
        MUTATION_SPAN = 1000
        MUTATION_PROBABILITY = 0.5

        children_list = [children1, children2]

        for i in range(len(children_list)):

            mutation_starter = np.random.choice([0, 1], p=[1 - MUTATION_PROBABILITY, MUTATION_PROBABILITY])
            if mutation_starter == 1:
                mutation_pointer = np.random.choice(
                    range(MUTATION_SPAN, len(children_list[i].genelist) - MUTATION_SPAN))
                # Split in three parts of which the second one will be randomized
                children_list_part1 = children_list[i].genelist[0:mutation_pointer]

                children_list_part2 = []
                for j in range(MUTATION_SPAN):
                    children_list_part2.append(np.random.choice([0, 1]))

                children_list_part3 = children_list[i].genelist[
                                      mutation_pointer + MUTATION_SPAN:len(children_list[i].genelist)]

                children_list[i].genelist = children_list_part1 + children_list_part2 + children_list_part3
                children_list[i].recalc_fitness()

        children1 = children_list[0]
        children2 = children_list[1]
        return children1, children2

    def survivor_selection(self):
        """
            Selecting survivors by fitness and replace others with new children
        """
        self.chromosome_list.sort(key=lambda x: x.cost)

        for i in range(int(len(self.chromosome_list) * self.NOOB_PERCENTAGE)):
            self.chromosome_list.pop()

        for child in self.children_list:
            self.chromosome_list.append(child)

        self.chromosome_list.sort(key=lambda x: x.cost)
        self.best_solution = self.chromosome_list[0].cost

    def create_children(self, num_of_children):
        """
            Create a list of new children

            Args:
                num_of_children (int): Amount of children to be created
        """
        mutated_children_list = []
        for i in range(int(num_of_children / 2)):
            parent1, parent2 = self.parent_selection()
            children1, children2 = self.crossover(parent1, parent2)
            mutated_child1, mutated_child2 = self.mutation2(children1, children2)
            mutated_children_list.append(mutated_child1)
            mutated_children_list.append(mutated_child2)
        self.children_list = mutated_children_list


class Chromosome:
    def __init__(self, genelist, rmfs, demandlist: list):
        """
            Creates and initializes Chromosome() object

            Args:
                genelist (list): Solution list of pod return places of GA heuristic
                rmfs (warehouse): Warehouse
                demandlist (int): Demandlist of demanded pods (-> one pod per iteration)
        """
        self.genelist = genelist
        self.rmfs = rmfs
        self.demandlist = demandlist

        storage, self.cost = self.rmfs.run(demandlist, self.genelist)

    def recalc_fitness(self):
        """
            Recalculating fitness
        """
        storage, self.cost = self.rmfs.run(self.demandlist, self.genelist)
