# from __future__ import annotations
import random
from typing import Optional, List
from data.training_data import TrainingData


class Individual:
    _gen_list = []
    _gen_len = 0
    _mid_gen = 0
    _KEYS = ['genotype', 'vitality', 'fitness']
    _mutation_chance = 0.5

    def __init__(self, genotype: Optional[dict] = None):
        self.vitality = 0
        self.fitness = None
        if genotype:
            self.genotype = genotype
        else:
            self.genotype = __class__.get_random_genotype()

    def crossover(self, other: 'Individual') -> 'Individual':
        child_genes = {}
        gen_list = Individual._gen_list
        for i in range(Individual._gen_len):
            child_genes[gen_list[i]] = (self.genotype[gen_list[i]] + other.genotype[gen_list[i]]) / 2
        return Individual(child_genes)

    def mutate(self) -> 'Individual':
        child_genes = {}
        mid = Individual._mid_gen
        random.shuffle(Individual._gen_list)
        for g in Individual._gen_list[:mid]:
            child_genes[g] = random.uniform(-1, 1)
        for g in Individual._gen_list[mid:]:
            child_genes[g] = self.genotype[g]
        return Individual(child_genes)

    def calculate_pm10(self, td: TrainingData) -> (int, float):
        result = sum(
            [value * td.__dict__[key] for key, value in self.genotype.items()])
        return result

    def calculate_fitness(self, td: TrainingData):
        result = sum(
            [value * td.__dict__[key] for key, value in self.genotype.items()])
        return abs(td.pm10_after_24h - result)

    def to_dict(self):
        dct = {}
        for key in self._KEYS:
            dct[key] = getattr(self, key)
        return dct

    @staticmethod
    def set_max_vitality(max_vitality: int):
        __class__._max_vitality = max_vitality

    @staticmethod
    def set_gen_list(keys: List[str]):
        __class__._gen_list = keys
        __class__._gen_len = len(keys)
        __class__._mid_gen = int(__class__._gen_len / 2)

    @staticmethod
    def set_mutation_chance(value: (float, int)):
        if value > 0.5:
            value = 0.5
        if value < 0.05:
            value = 0.05
        __class__._mutation_chance = value

    @staticmethod
    def should_mutate():
        if random.uniform(0, 1) <= Individual._mutation_chance:
            return True

    @staticmethod
    def get_mutation_chance():
        return Individual._mutation_chance

    @staticmethod
    def get_random_genotype() -> dict:
        genotype = {}
        if __class__._gen_list:
            for key in __class__._gen_list:
                genotype[key] = random.uniform(-1, 1)
        else:
            raise ValueError(f'{__class__.__name__} keys can\' be empty')

        return genotype

    @staticmethod
    def from_dict(dct: dict):
        genotype = dct.get('genotype', None)
        individual = __class__(genotype)
        for key in individual._KEYS:
            if key == 'max_vitality' or key == 'genotype':
                continue
            value = dct.get(key)
            if value:
                setattr(individual, key, value)
        return individual

    def __repr__(self):
        return '<' + self.__class__.__name__ + '(' + \
               ','.join([key + '=' + str(getattr(self, key)) for key in self._KEYS]) + \
               ')>'
