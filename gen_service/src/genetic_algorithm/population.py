import math
import os
import random
from typing import List

from config import Config
from decorators import timer, not_implemented, logger
from multiprocessing import cpu_count

from genetic_algorithm.individual import Individual


class Population:
    # _cpu_count = cpu_count()
    _cpu_count = 1

    def __init__(self, cfg: Config, training_data):
        self.cfg = cfg
        self.population_size = cfg.population_size
        self._sqrt_of_population_size = int(math.sqrt(cfg.population_size))
        self.training_data = training_data
        self._pass_best = cfg.pass_best
        self._max_vitality = cfg.max_vitality
        self.population = []
        self.bests = []
        self.best = None

        self.evolution_types = {
            'default': self._evolve_by_rank,
            'crossing_bests': self._evolve_crossing_bests,
            'roulette': self._evolve_by_roulette,
            'rank': self._evolve_by_rank,
            'ranks': self._evolve_by_rank,
            'tournament': self._evolve_by_tournament,
        }

        self._evolve = self.get_evolution_type(
            os.getenv('EVOLUTION_TYPE', 'default')
        )
        self.populate()

    def add(self, individual):
        self.population.append(individual)

    def clear(self):
        self.population = []
        self.bests = []

    def populate(self):
        new_population = []
        for _ in range(self.population_size):
            new_population.append(Individual())
        self.population.extend(self.calculate_fitness(new_population))

    def get_current_best(self) -> Individual:
        return min(self.population, key=lambda i: i.fitness)

    def get_best(self) -> Individual:
        return self.best

    def set_best(self, individual: Individual):
        if not self.best:
            self.best = individual
            return None
        if individual.fitness < self.best.fitness:
            self.best = individual

    def get_evolution_type(self, evolution_type):
        evolution_type = str(evolution_type).lower().replace(' ', '_')

        if evolution_type not in self.evolution_types.keys():
            print('Invalid evolution type : {}\n'
                  'Evolution type is set to default'
                  .format(evolution_type))
        default = self.evolution_types.get('default')
        return self.evolution_types.get(evolution_type, default)

    @timer
    @logger
    def evolve(self):
        if self._pass_best and self.get_best():
            best = self.get_best()
            self._evolve()
            best.vitality = 0
            self.population.append(best)
        else:
            self._evolve()
        self.set_best(self.get_current_best())
        return self.get_best().fitness

    @not_implemented
    def _evolve_crossing_bests(self):
        self._sort()
        self._calc_bests()
        self._decrement_population()
        children = []
        for mother in self.bests:
            for father in self.bests:
                children.append(mother.crossover(father))
        self.population.extend(self.calculate_fitness(children))

    @not_implemented
    def _evolve_by_tournament(self):
        parents = []
        children = []
        self._shuffle()
        max_size = self._sqrt_of_population_size
        for index in range(max_size):
            if index + 1 != max_size:
                parents.append(
                    min(
                        self.population[index * max_size:(index + 1) * max_size],
                        key=lambda i: i.fitness)
                )
            else:
                parents.append(
                    min(
                        self.population[index * max_size:],
                        key=lambda i: i.fitness)
                )
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

    def _evolve_by_rank(self):
        self._sort(reverse=True)
        rank_list = []
        children = []
        population_size = len(self.population)
        rank_sum = population_size * (population_size + 1) / 2
        for i, phenotype in enumerate(self.population, 1):
            rank_list.append(sum(range(1, i + 1)) / rank_sum)

        max_len = self.cfg.children_max
        crossover_chance = self.cfg.crossover_chance
        mutation_chance = self.cfg.mutation_chance
        for _ in range(max_len):
            if random.uniform(0, 1) <= crossover_chance:
                mother = self.population[self._get_parent_id(rank_list)]
                father = self.population[self._get_parent_id(rank_list)]
                children.append(mother.crossover(father))
            if random.uniform(0, 1) <= mutation_chance:
                mutable = self.population[self._get_parent_id(rank_list)]
                children.append(mutable.mutate())
        self._decrement_population()
        self.population.extend(self.calculate_fitness(children))

    @not_implemented
    def _evolve_by_roulette(self):
        self._sort(reverse=True)
        chance_list = []
        children = []
        chance_sum = sum(map(lambda individual: 1 / individual.fitness, self.population))
        for i in range(1, len(self.population) + 1):
            chance_list.append(sum(map(lambda individual: 1 / individual.fitness, self.population[:i])) / chance_sum)
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

    def _calc_bests(self, reverse=False):
        if reverse:
            self.bests = self.population[self.population_size - self._sqrt_of_population_size:]
        else:
            self.bests = self.population[:self._sqrt_of_population_size]

    def _decrement_population(self):
        for individual in self.population:
            individual.vitality += 1

        self.population = [
            individual
            for individual in self.population
            if individual.vitality <= self._max_vitality
        ]

    def calculate_fitness(self, population):
        if Population._cpu_count > 2 and self.population_size >= 50:
            return self._calculate_fitness_in_parallel(population)
        elif Population._cpu_count > 1 and self.population_size >= 100:
            return self._calculate_fitness_in_parallel(population)
        else:
            return self._calculate_fitness(population)

    # @timer
    def _calculate_fitness(self, population):
        for individual in population:
            individual.fitness = sum((individual.calculate_fitness(td) for td in self.training_data))
        return population

    def _calc(self, individual: Individual):
        individual.fitness = sum((individual.calculate_fitness(t) for t in self.training_data))
        return individual

    # @timer
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

    def get_unique_evolution_types(self) -> List[str]:
        function_types = set(map(lambda key_value: key_value[1], list(self.evolution_types.items())))
        keys = list(self.evolution_types.keys())
        unique_keys = []
        if 'default' in keys:
            keys.remove('default')
        for key in keys:
            e_type = self.evolution_types.get(key)
            if e_type in function_types:
                unique_keys.append(key)
                function_types.remove(e_type)
        return unique_keys
