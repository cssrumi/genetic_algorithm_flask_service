import math
import os
import random

from genetic_algorithm.phenotype_cy import Phenotype
# from genetic_algorithm.phenotype import Phenotype
from decorators import timer, not_implemented
from multiprocessing import cpu_count


class Population:
    _cpu_count = cpu_count()

    def __init__(self, population_size, training_data):
        self.population_size = population_size
        # self.one_tenth = int(population_size / 10) * Phenotype.VITALITY
        self.one_tenth = int(population_size / 10)
        self.training_data = training_data
        self.population = []
        self.bests = []
        self.evolve = self.set_evolution_type(
            os.getenv('EVOLUTION_TYPE', 'default'))
        self.populate()

    def add(self, individual):
        self.population.append(individual)

    def populate(self):
        new_population = []
        for _ in range(self.population_size):
            new_population.append(Phenotype())
        self.population.extend(self.calculate_fitness(new_population))

    def get_best(self):
        return min(self.population, key=lambda i: i.fitness)

    def set_evolution_type(self, evolution_type):
        evolution_type = str(evolution_type).lower()
        evolution_types = {
            'default': self._evolve_by_rank,
            'ten_percent': self._evolve_by_one_tenth,
            'roulette': self._evolve_by_roulette,
            'rank': self._evolve_by_rank,
            'ranks': self._evolve_by_rank,
            'tournament': self._evolve_by_tournament,
        }
        if evolution_type not in evolution_types.keys():
            print('Invalid evolution type : {}\n'
                  'Evolution type is set to default'
                  .format(evolution_type))
        default = evolution_types.get('default')
        return evolution_types.get(evolution_type, default)

    def _evolve_by_one_tenth(self):
        self._sort()
        self._calc_best_ten_percent()
        self._decrement_population()
        children = []
        for mother in self.bests:
            for father in self.bests:
                children.append(mother.crossover(father))
        self.population.extend(self.calculate_fitness(children))

    # @not_implemented
    def _evolve_by_tournament(self):
        how_many = int(math.sqrt(self.population_size))
        parents = []
        children = []
        for _ in range(how_many):
            self._shuffle()
            parents.append(min(self.population[:how_many]))
        for mother in parents:
            for father in parents:
                children.append(mother.crossover(father))
        self._decrement_population()
        self.population.extend(self.calculate_fitness(children))

    def _get_parent_id(self, rank_list):
        for _ in range(self.population_size):
            random_rank = random.uniform(0, 1)
            for i, rank in enumerate(rank_list):
                if rank > random_rank:
                    return i
        return -1

    # @not_implemented
    def _evolve_by_rank(self):
        self._sort(reverse=True)
        rank_list = []
        children = []
        population_size = len(self.population)
        for i, phenotype in enumerate(self.population, 1):
            rank_list.append(i / population_size)
        for _ in range(self.population_size):
            mother = self.population[self._get_parent_id(rank_list)]
            father = self.population[self._get_parent_id(rank_list)]
            children.append(mother.crossover(father))
        self._decrement_population()
        self.population.extend(self.calculate_fitness(children))

    # @not_implemented
    def _evolve_by_roulette(self):
        self._sort(reverse=True)
        chance_list = []
        children = []
        fitness_sum = sum(map(lambda individual: individual.fitness, self.population))
        for i in range(1, len(self.population) + 1):
            chance_list.append(sum(map(lambda individual: individual.fitness, self.population[:i])) / fitness_sum)
        for _ in range(self.population_size):
            mother = self.population[self._get_parent_id(chance_list)]
            father = self.population[self._get_parent_id(chance_list)]
            children.append(mother.crossover(father))
        self._decrement_population()
        self.population.extend(self.calculate_fitness(children))

    def _sort(self, reverse=False):
        self.population.sort(key=lambda i: i.fitness, reverse=reverse)

    def _shuffle(self):
        random.shuffle(self.population)

    def _calc_best_ten_percent(self, reverse=False):
        if reverse:
            self.bests = self.population[self.population_size - self.one_tenth:]
        else:
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
        if Population._cpu_count > 2 and self.population_size >= 50:
            return self._calculate_fitness_in_parallel(population)
        elif Population._cpu_count > 1 and self.population_size >= 100:
            return self._calculate_fitness_in_parallel(population)
        else:
            return self._calculate_fitness(population)

    @timer
    def _calculate_fitness(self, population):
        for individual in population:
            individual.fitness = sum((individual.calculate_fitness(td) for td in self.training_data))
        return population

    def _calc(self, individual: Phenotype):
        individual.fitness = sum((individual.calculate_fitness(t) for t in self.training_data))
        return individual

    @timer
    def _calculate_fitness_in_parallel(self, population):
        from multiprocessing import Pool

        with Pool() as executor:
            return (individual for individual in executor.map(self._calc, population))

    @not_implemented
    def set_calculation_type(self, calculation_type):
        calculation_type = str(calculation_type).lower()
        calculation_types = {
            'default': self._calculate_fitness,
            'one_core': self._calculate_fitness,
            'one core': self._calculate_fitness,
            '1 core': self._calculate_fitness,
            'sequential': self._calculate_fitness,
            'parallel': self._calculate_fitness_in_parallel,
            'in parallel': self._calculate_fitness_in_parallel,
            'in_parallel': self._calculate_fitness_in_parallel,
        }
        if calculation_type not in calculation_types.keys():
            print('Invalid calculation type : {}\n'
                  'Calculation type is set to default'
                  .format(calculation_type))
        default = calculation_types.get('default')
        return calculation_types.get(calculation_type, default)
