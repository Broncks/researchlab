from random import *
import numpy as np

POPULATION_SIZE = 10
MAX_PLACE_ID = 4
NUM_OF_CHILDREN = 2  # only even numbers e.g. 2/4/6/8/...


def ga(demandlist, rmfs):
    population = Population(demandlist, rmfs)

    population.create_children(NUM_OF_CHILDREN)
    population.survivor_selection()


class Population:

    def __init__(self, demandlist, rmfs):
        self.rmfs = rmfs
        self.demandlist = demandlist
        self.chromosome_list = self.create_init_population(POPULATION_SIZE, demandlist, MAX_PLACE_ID)
        self.children_list = []
        print(f"Meine Chromosomliste {len(self.chromosome_list)}")
        print(f"RandChromosomliste ausgabe {self.chromosome_list[0].genelist}")

    def create_init_population(self, population_size, demandlist, MAX_PLACE_ID):
        chromosome_list = []
        for i in range(population_size):
            chromosome_list.append(
                Chromosome([randrange(0, MAX_PLACE_ID) for i in range(len(demandlist))], self.rmfs, demandlist))
            # TODO Vielleicht ist es Sinnvoll eine Gewichtung der Einträge zu erstellen, um dem Algo die nötigen Einträge zu liefern. Kann aber auch sein, dass das so klappt
        return chromosome_list

    def parent_selection(self, chromosome_list):
        # Tournament
        candidate1 = chromosome_list[np.random.choice(len(chromosome_list))]
        candidate2 = chromosome_list[np.random.choice(len(chromosome_list))]
        candidate3 = chromosome_list[np.random.choice(len(chromosome_list))]
        candidate4 = chromosome_list[np.random.choice(len(chromosome_list))]

        if candidate1.cost > candidate2.cost:
            parent1 = candidate1
        else:
            parent1 = candidate2

        if candidate3.cost > candidate4.cost:
            parent2 = candidate3
        else:
            parent2 = candidate4

        return parent1, parent2

    def crossover(self, parent1, parent2):
        # One Point Crossover (Split in half)
        print("Parent1 ", parent1)
        parent1half1 = parent1.genelist[:len(parent1.genelist) // 2]
        parent1half2 = parent1.genelist[len(parent1.genelist) // 2:]

        parent2half1 = parent1.genelist[:len(parent1.genelist) // 2]
        parent2half2 = parent1.genelist[len(parent1.genelist) // 2:]

        genelist1 = parent1half1 + parent2half2
        genelist2 = parent2half1 + parent1half2

        children1 = Chromosome(genelist1, self.rmfs, self.demandlist)
        children2 = Chromosome(genelist2, self.rmfs, self.demandlist)

        return children1, children2

    def mutation(self, children1, children2):
        # Inversion
        MUTATION_SPAN = 6
        MUTATION_PROBABILITY = 0.05
        NUM_OF_MUTATIONS = 1
        children_list = [children1, children2]
        for i in range(len(children_list)):
            print(f"1-MUT_PROB {1- MUTATION_PROBABILITY}")
            mutation_starter = np.random.choice([0, 1], p=[1 - MUTATION_PROBABILITY, MUTATION_PROBABILITY])
            if mutation_starter == 1:
                mutation_pointer = np.random.choice(range(len(children_list[i].genelist) - MUTATION_SPAN))
                for j in range(MUTATION_SPAN):
                    # Einteilung in drei Teile, der mittlere wird inversed
                    children_list[i].genelist = children_list[i].genelist[0:mutation_pointer - 1] + \
                                                children_list[i].genelist[
                                                mutation_pointer:mutation_pointer - MUTATION_SPAN] + \
                                                children_list[i].genelist[
                                                mutation_pointer + MUTATION_SPAN + 1:len(children_list[i].genelist)]
        children1 = children_list[0]
        children2 = children_list[1]
        return children1, children2

    def survivor_selection(self):
        # Fitness Based
        lowest_parent = 999999 #initialwert

        for i in range(len(self.chromosome_list)):
            if lowest_parent > self.chromosome_list[i].cost:
                lowest_parent_position = i


            self.children_list
            #TODO hier gehts weiter


    def create_children(self, num_of_children):
        mutated_children_list = []
        for i in range(int(num_of_children / 2)):
            parent1, parent2 = self.parent_selection(self.chromosome_list)
            children1, children2 = self.crossover(parent1, parent2)
            mutated_child1, mutated_child2 = self.mutation(children1, children2)
            mutated_children_list.append(mutated_child1)
            mutated_children_list.append(mutated_child2)
        self.children_list = mutated_children_list


class Chromosome:
    def __init__(self, genelist, rmfs, demandlist):
        self.genelist = genelist
        self.rmfs = rmfs

        storage, self.cost = self.rmfs.run(demandlist, self.genelist)

        print(f"Erzeuge Kosten von {self.cost}")

    def recalc_fitness(self):
        self.cost = self.rmfs.run(self.demandlist, self.genelist)
