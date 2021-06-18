from random import *
import numpy as np

POPULATION_SIZE = 50
MAX_PLACE_ID = 4
NUM_OF_CHILDREN = 5


def ga(demandlist, rmfs):
    population = Population(demandlist, rmfs)

    population.create_children(NUM_OF_CHILDREN)


class Population:

    def __init__(self, demandlist, rmfs):
        self.rmfs = rmfs
        self.demandlist = demandlist
        self.chromosome_list = self.create_init_population(POPULATION_SIZE, demandlist, MAX_PLACE_ID)
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

        if candidate1.cost > candidate2.cost:
            parent1 = candidate1
        else:
            parent1 = candidate2




        return parent1, parent2

    def crossover(self):
        # One Point Crossover (Split in half)
        pass

    def mutation(self):
        # Inversion
        pass

    def survivor_selection(self):
        # Fitness Based
        pass

    def create_children(self, num_of_children):
        self.parent_selection(self.chromosome_list)
        self.crossover()
        self.mutation()


class Chromosome:
    def __init__(self, genelist, rmfs, demandlist):
        self.genelist = genelist

        storage, self.cost = rmfs.run(demandlist, self.genelist)

        print(f"Erzeuge Kosten von {self.cost}")
