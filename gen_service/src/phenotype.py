import random

from gen_service.src.signs import signs_set
from gen_service.src.test_cases import test_types

genes_list = ['test_type', 'a_b', 'b_c', 'a_1', 'b_1', 'c_1']
genes_set = set(genes_list)
mutable_genes = ('a_1', 'b_1', 'c_1')
# mutable_genes = genes_list
genes_iterator = [i for i in range(len(genes_set))]
mid_gen = len(genes_set) / 2


class Phenotype:
    def __init__(self, genes=None):
        self.score = 0
        if genes is not None:
            self.genes = genes
        else:
            self.init_random_genes()

    def init_random_genes(self):
        self.genes = {
            'test_type': random.choice(test_types),
            'a_b': random.choice(signs_set),
            'b_c': random.choice(signs_set),
            'a_1': random.uniform(-10, 10),
            'b_1': random.uniform(0, 10),
            'c_1': random.uniform(0, 10)
        }

    def crossover(self, other):
        child_genes = {}
        random.shuffle(genes_list)
        for key, i in zip(genes_list, genes_iterator):
            if i < mid_gen:
                child_genes[key] = self.genes.get(key)
            else:
                child_genes[key] = other.genes.get(key)
        if self.mutate():
            key = random.choice(genes_list)
            if key in mutable_genes:
                child_genes[key] = child_genes.get(key) * random.uniform(-10, 10)
            elif key == 'test_type':
                child_genes[key] = random.choice(test_types)
            else:
                child_genes[key] = random.choice(signs_set)
        
        return Phenotype(child_genes)

    def mutate(self):
        if random.uniform(0, 1) <= 0.05:
            return True
