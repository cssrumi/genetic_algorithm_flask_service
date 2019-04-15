import os
import random


class Phenotype:

    try:
        vitality = int(os.getenv('VITALITY', 5))
        print('try block')
    except (ValueError, TypeError):
        vitality = 5

    def __init__(self, genes=None):
        self.fitness = 0
        self.vitality = Phenotype.vitality

        if genes is not None:
            self.genes = genes
        else:
            self.init_random_genes()

    def init_random_genes(self):
        pass

    def crossover(self, other):
        child_genes = {}
        pass
        if self.mutate():
            pass
        
        return Phenotype(child_genes)

    def mutate(self):
        if random.uniform(0, 1) <= 0.05:
            return True
