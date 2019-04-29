import os
import random

from data.training_data import TrainingData
from genetic_algorithm.genotype import Genotype


class Phenotype:
    try:
        _vitality = int(os.getenv('VITALITY', 3))
    except (ValueError, TypeError):
        _vitality = 3

    def __init__(self, genotype=None):
        self.fitness = None
        self.vitality = Phenotype._vitality

        if genotype is not None:
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

        return Phenotype(Genotype(**child_genes))

    def mutate(self):
        if random.uniform(0, 1) <= 0.65:
            return True

    def calculate_fitness(self, td: TrainingData):
        result = sum([value*td.__dict__[key] for key, value in self.genotype.__dict__.items()])
        return td.pm10_after_24h - result

    def __repr__(self):
        return '<' + self.__class__.__name__ + '(' + \
               ','.join([key + '=' + str(value) for key, value in self.__dict__.items()]) + \
               ')>'
