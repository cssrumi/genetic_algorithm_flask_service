import os
import random
# import sys
#
# sys.path.append(os.path.abspath("."))
# sys.path.append(os.path.abspath("../"))

from data.training_data import TrainingData
# from genotype_cy cimport CyGenotype as Genotype
cimport genotype_cy
# from genotype_cy import Genotype
# import genetic_algorithm.genotype
# from genetic_algorithm.genotype_cy import get_random_genotype, CyGenotype as Genotype


cdef class CyPhenotype:
    try:
        VITALITY = int(os.getenv('VITALITY', 3))
    except (ValueError, TypeError):
        VITALITY = 3

    def __init__(self, genotype=None):
        self.fitness = None
        self.vitality = CyPhenotype.VITALITY
        self.genotype = genotype if genotype else self.init_random_genes()
        self._KEYS = ['fitness', 'vitality', 'genotype']

    property KEYS:
        def __get__(self):
            return self._KEYS

    cdef genotype_cy.CyGenotype init_random_genes(self):
        return genotype_cy.CyGenotype.get_random_genotype()

    cpdef object crossover(self, object other: CyPhenotype):
        cdef dict child_genes = {}
        cdef list gen = self.genotype.gen_list
        random.shuffle(gen)
        cdef unsigned int mid = self.genotype.mid_gen
        cdef unsigned int i
        cdef object g
        for i in range(self.genotype.gen_len):
            if i > mid:
                child_genes[gen[i]] = getattr(self.genotype, gen[i])
            else:
                child_genes[gen[i]] = getattr(other.genotype, gen[i])
        if self.mutate():
            random.shuffle(gen)
            for g in gen[:self.genotype.mid_gen]:
                child_genes[g] = random.uniform(-1, 1)

        return Phenotype(genotype_cy.CyGenotype(**child_genes))

    cdef mutate(self):
        if random.uniform(0, 1) <= 0.65:
            return True
        return False

    cpdef long double calculate_fitness(self, object td: TrainingData):
        cdef long double result = sum(
            [getattr(self.genotype, key)*td.__dict__[key] for key in self.genotype.KEYS])
        return abs(td.pm10_after_24h - result)

    def __repr__(self):
        return '<' + self.__class__.__name__ + '(' + \
               ','.join([key + '=' + str(getattr(self, key)) for key in self._KEYS]) + \
               ')>'


class Phenotype(CyPhenotype):
    pass
