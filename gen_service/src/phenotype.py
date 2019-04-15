import random


class Phenotype:
    def __init__(self, genes=None):
        self.fitness = 0

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
