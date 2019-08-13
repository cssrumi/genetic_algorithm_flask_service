import random
# import sys
#
# sys.path.append(os.path.abspath("."))
# sys.path.append(os.path.abspath("../"))

from data.training_data import TrainingData
# from genotype_cy cimport CyGenotype as Genotype
# cimport genotype_cy
from genetic_algorithm.old.genotype import Genotype
# from genotype_cy import Genotype
# from genetic_algorithm.genotype_cy import get_random_genotype, CyGenotype as Genotype


cdef class CyPhenotype:
    def __init__(self, genotype=None):
        self.fitness = None
        self.generations = 0
        self.genotype = genotype if genotype else self.init_random_genes()
        self._KEYS = ['fitness', 'generations', 'genotype']

    property KEYS:
        def __get__(self):
            return self._KEYS

    cdef object init_random_genes(self):
        return Genotype.get_random_genotype()

    cpdef object crossover(self, object other: CyPhenotype):
        cdef dict child_genes = {}
        cdef list gen = self.genotype.gen_list
        random.shuffle(gen)
        cdef unsigned int mid = self.genotype.mid_gen
        cdef unsigned int i
        cdef object g
        for i in range(Genotype.gen_len):
            if i > mid:
                child_genes[gen[i]] = self.genotype.__dict__[gen[i]]
            else:
                child_genes[gen[i]] = other.genotype.__dict__[gen[i]]
        if self.mutate():
            random.shuffle(gen)
            for g in gen[:self.genotype.mid_gen]:
                child_genes[g] = random.uniform(-1, 1)

        return Phenotype(Genotype(**child_genes))

    cdef mutate(self):
        if random.uniform(0, 1) <= 0.65:
            return True
        return False

    cpdef long double calculate_pm10(self, object td: TrainingData):
        cdef long double result = sum(
            [value*td.__dict__[key] for key, value in self.genotype.__dict__.items()])
        return result

    cpdef long double calculate_fitness(self, object td: TrainingData):
        cdef long double result = sum(
            [value*td.__dict__[key] for key, value in self.genotype.__dict__.items()])
        return abs(td.pm10_after_24h - result)


    cpdef to_dict(self):
        dct = {}
        for key in self._KEYS:
            if key == 'genotype':
                dct[key] = vars(self.genotype)
            else:
                dct[key] = getattr(self, key)
        return dct

    @classmethod
    def from_dict(cls, dct: dict):
        genotype_dict = dct.get('genotype', None)
        genotype = Genotype(**genotype_dict.items())
        print(cls.__name__)
        phenotype = cls(genotype)
        for key in phenotype.KEYS:
            if key == 'genotype':
                continue
            value = dct.get(key)
            if value:
                setattr(phenotype, key, value)
        return phenotype


    def __repr__(self):
        return '<' + self.__class__.__name__ + '(' + \
               ','.join([key + '=' + str(getattr(self, key)) for key in self._KEYS]) + \
               ')>'


class Phenotype(CyPhenotype):
    pass
