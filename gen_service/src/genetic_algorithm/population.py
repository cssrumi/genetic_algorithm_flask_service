import random

from genetic_algorithm.phenotype import Phenotype
from decorators import timer


class Population:

    def __init__(self, population_size, training_data):
        self.population_size = population_size
        # self.one_tenth = int(population_size / 10) * Phenotype.VITALITY
        self.one_tenth = int(population_size / 10)
        self.training_data = training_data
        self.evolution_type = None
        self.population = []
        self.bests = []
        self.populate()

    def add(self, individual):
        self.population.append(individual)

    def populate(self):
        new_population = []
        for _ in range(self.population_size):
            new_population.append(Phenotype())
        self.calculate_fitness(new_population)

    def get_best(self):
        return min(self.population, key=lambda i: i.fitness)

    # @timer
    def evolve(self):
        if self.evolution_type in ['default', 'ten_percent', None]:
            self._evolve_by_one_tenth()

        elif self.evolution_type in ['roulette']:
            raise TypeError('Not implemented : {}'.format(self.evolution_type))

        elif self.evolution_type in ['rank', 'ranks']:
            raise TypeError('Not implemented : {}'.format(self.evolution_type))

        elif self.evolution_type in ['tournament']:
            raise TypeError('Not implemented : {}'.format(self.evolution_type))

        else:
            raise TypeError('Invalid evolution type : {}'.format(self.evolution_type))

    def _evolve_by_one_tenth(self):
        self._sort()
        self._calc_best_ten_percent()
        self._decrement_population()
        new_population = []
        for mother in self.bests:
            for father in self.bests:
                new_population.append(mother.crossover(father))
        self.calculate_fitness(new_population)

    # NOT IMPLEMENTED YET
    def _evolve_by_tournament(self):
        self._decrement_population()
        self._shuffle()

    # NOT IMPLEMENTED YET
    def _evolve_by_rank(self):
        self._decrement_population()
        self._sort()

    def _sort(self):
        self.population.sort(key=lambda i: i.fitness, reverse=False)

    def _shuffle(self):
        random.shuffle(self.population)

    def _calc_best_ten_percent(self):
        self.bests = self.population[:self.one_tenth]

    def _decrement_population(self):
        for individual in self.population:
            individual.vitality -= 1

        self.population = [
            individual
            for individual in self.population
            if individual.vitality > 0
        ]

    def calculate_fitness(self, population):
        from multiprocessing import cpu_count

        if cpu_count() > 2 and self.population_size > 50:
            self._calculate_fitness_in_parallel(population)
        else:
            self._calculate_fitness(population)

    @timer
    def _calculate_fitness(self, population):
        for individual in population:
            individual.fitness = sum((individual.calculate_fitness(td) for td in self.training_data))
        self.population.extend(population)

    def _calc(self, individual: Phenotype):
        individual.fitness = sum((individual.calculate_fitness(t) for t in self.training_data))
        return individual

    @timer
    def _calculate_fitness_in_parallel(self, population):
        from multiprocessing import Pool

        with Pool() as executor:
            self.population.extend([individual for individual in executor.map(self._calc, population)])
