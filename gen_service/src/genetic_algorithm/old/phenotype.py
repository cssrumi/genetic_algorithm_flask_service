import random

from data.training_data import TrainingData
from genetic_algorithm.old.genotype import Genotype


class Phenotype:
    def __init__(self, genotype=None):
        self.fitness = None
        self.generations = 0

        if genotype:
            self.genotype = genotype
        else:
            self.init_random_genes()

    def init_random_genes(self):
        self.genotype = Genotype.get_random_genotype()

    def crossover(self, other):
        child_genes = {}
        gen = Genotype.gen_list
        random.shuffle(gen)
        mid = Genotype.mid_gen
        for i in range(Genotype.gen_len):
            if i > mid:
                child_genes[gen[i]] = self.genotype.__dict__[gen[i]]
            else:
                child_genes[gen[i]] = other.genotype.__dict__[gen[i]]
        if self.mutate():
            random.shuffle(gen)
            for g in gen[:Genotype.mid_gen]:
                child_genes[g] = random.uniform(-1, 1)

        return self.__class__(Genotype(**child_genes))

    def mutate(self):
        if random.uniform(0, 1) <= 0.65:
            return True

    def calculate_fitness_cy(self, td: TrainingData):
        result = 0
        for k, v in self.genotype.__dict__.items():
            result += v * td.__dict__.get(k)
        return abs(td.pm10_after_24h - result)

    def calculate_fitness(self, td: TrainingData):
        result = sum([value*td.__dict__[key] for key, value in self.genotype.__dict__.items()])
        return abs(td.pm10_after_24h - result)

    def __repr__(self):
        return '<' + self.__class__.__name__ + '(' + \
               ','.join([key + '=' + str(value) for key, value in self.__dict__.items()]) + \
               ')>'
