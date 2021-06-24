from random import *
import numpy as np

ITERATIONS = 10
POPULATION_SIZE = 10
ELITE_PERCENTAGE = 0.2
MAX_PLACE = 4
NUM_OF_CHILDREN = POPULATION_SIZE * ELITE_PERCENTAGE


def ga(demandlist, rmfs):
    population = Population(demandlist, rmfs, ELITE_PERCENTAGE)


    i = 0
    while i < ITERATIONS:  # TODO: Termination criterion Folie S. 57/62
        # TODO: iterate iterate iterate
        population.create_children(NUM_OF_CHILDREN)
        #parent1, parent2 = population.parent_selection(population.chromosome_list)
        #child1, child2 = population.crossover(parent1, parent2)
        #child1, child2 = population.mutation(child1, child2)
        population.survivor_selection()
        print(f'Iteration {i + 1}')
        i += 1

    population.chromosome_list.sort(key=lambda x: x.cost)
    return population.chromosome_list[0].genelist


class Population:

    def __init__(self, demandlist, rmfs, ELITE_PERCENTAGE):
        self.rmfs = rmfs
        self.demandlist = demandlist
        self.chromosome_list = self.create_init_population(POPULATION_SIZE, demandlist, MAX_PLACE)

        self.children_list = []
        self.ELITE_PERCENTAGE = ELITE_PERCENTAGE
        # print(f"Meine Chromosomliste {len(self.chromosome_list)}")
        # print(f"RandChromosomliste ausgabe {self.chromosome_list[0].genelist}")

    def create_init_population(self, population_size, demandlist, MAX_PLACE_ID):
        chromosome_list = []
        for i in range(population_size):
            chromosome_list.append(
                Chromosome([randrange(0, MAX_PLACE_ID) for i in range(len(demandlist))], self.rmfs, demandlist))
            # TODO Vielleicht ist es Sinnvoll eine Gewichtung der Einträge zu erstellen, um dem Algo die nötigen Einträge zu liefern. Kann aber auch sein, dass das so klappt


        return chromosome_list

    def parent_selection(self):
        # Tournament


        candidate = []
        for i in range(4):
            candidate.append(self.chromosome_list[np.random.choice(len(self.chromosome_list))])

        if candidate[0].cost > candidate[1].cost:
            parent1 = candidate[0]
        else:
            parent1 = candidate[1]

        if candidate[2].cost > candidate[3].cost:
            parent2 = candidate[2]
        else:
            parent2 = candidate[3]

        print("parent_selection() parent1.genelist len", len(parent1.genelist))
        print("parent_selection() parent2.genelist len", len(parent2.genelist))
        return parent1, parent2

    def crossover(self, parent1, parent2):
        # One Point Crossover (Split in half)

        print("parent1.genelist ", len(parent1.genelist))
        print("parent2.genelist ", len(parent2.genelist))

        parent1half1 = parent1.genelist[:len(parent1.genelist) // 2]
        parent1half2 = parent1.genelist[len(parent1.genelist) // 2:]

        parent2half1 = parent2.genelist[:len(parent2.genelist) // 2]
        parent2half2 = parent2.genelist[len(parent2.genelist) // 2:]

        genelist1 = parent1half1 + parent2half2
        genelist2 = parent2half1 + parent1half2


        print("parent1half1 ", len(parent1half1))
        print("parent1half2 ", len(parent1half2))
        print("parent2half1 ", len(parent2half1))
        print("parent2half2 ", len(parent2half2))

        children1 = Chromosome(genelist1, self.rmfs, self.demandlist)
        children2 = Chromosome(genelist2, self.rmfs, self.demandlist)

        return children1, children2

    def mutation(self, children1, children2):
        # Inversion
        MUTATION_SPAN = 1000
        MUTATION_PROBABILITY = 0.5  # 0.05

        children_list = [children1, children2]

        print("mutation()children1 len ", len(children_list[0].genelist))
        print("mutation()children2 len ", len(children_list[1].genelist))
        for i in range(len(children_list)):

            mutation_starter = np.random.choice([0, 1], p=[1 - MUTATION_PROBABILITY, MUTATION_PROBABILITY])
            if mutation_starter == 1:
                mutation_pointer = np.random.choice(range(MUTATION_SPAN, len(children_list[i].genelist) - MUTATION_SPAN))
                # Einteilung in drei Teile, der mittlere wird inversed
                children_list_part1 = children_list[i].genelist[0:mutation_pointer]


                children_list_part2 = list(
                    reversed(children_list[i].genelist[mutation_pointer - MUTATION_SPAN : mutation_pointer]))
                children_list_part3 = children_list[i].genelist[
                                      mutation_pointer + MUTATION_SPAN:len(children_list[i].genelist)]
                print("Mutant len ", len(children_list_part1 + children_list_part2 + children_list_part3))
                children_list[i].genelist = children_list_part1 + children_list_part2 + children_list_part3
                children_list[i].recalc_fitness()

        children1 = children_list[0]
        children2 = children_list[1]
        return children1, children2

    def survivor_selection(self):
        # Fitness Based
        self.chromosome_list.sort(key=lambda x: x.cost)

        for i in range(int(len(self.chromosome_list) * self.ELITE_PERCENTAGE)):
            self.chromosome_list.pop()

        for child in self.children_list:
            self.chromosome_list.append(child)
        # TODO hier gehts weiter (oder war's das schon?)

    def create_children(self, num_of_children):
        mutated_children_list = []
        for i in range(int(num_of_children / 2)):

            #Just debugging
            for j in range(len(self.chromosome_list)):
                print("Umpalumpa ", len(self.chromosome_list[j].genelist))

            parent1, parent2 = self.parent_selection()
            children1, children2 = self.crossover(parent1, parent2)
            mutated_child1, mutated_child2 = self.mutation(children1, children2)
            mutated_children_list.append(mutated_child1)
            mutated_children_list.append(mutated_child2)
        self.children_list = mutated_children_list

    def kill_children(self):
        self.children_list = []

class Chromosome:
    def __init__(self, genelist, rmfs, demandlist):
        self.genelist = genelist
        self.rmfs = rmfs
        self.demandlist = demandlist

        storage, self.cost = self.rmfs.run(demandlist, self.genelist)

        print(f"Erzeuge Kosten von {self.cost}")

    def recalc_fitness(self):  # TODO: Aufruf in mutation (?)
        print("Kosten vor fitness ",self.cost)
        storage, self.cost = self.rmfs.run(self.demandlist, self.genelist)
        print("Kosten durch Fitness Func nach Mutation angepasst auf:", self.cost)
