from math import fabs

from phenotype import Phenotype


class GeneticAlgorithmImpl:
    def __init__(self, test_cases, population_size=100, max_generation=100):
        self.test_cases = test_cases.get_tests()
        self.population_size = population_size
        self.max_generation = max_generation
        self.population = []
        self.bests = []
        self.populate()
        self.one_tenth = int(population_size / 10)

    def run(self):
        for i in range(self.max_generation):
            self.evolve_population()

    def get_best(self):
        return self.bests[0]

    def populate(self):
        for _ in range(self.population_size):
            self.population.append(Phenotype())

    # @timer
    def evolve_population(self):
        self.calculate_fitness()
        self.set_bests()
        self.population = [self.get_best()]
        for mother in self.bests:
            for father in self.bests:
                self.population.append(mother.crossover(father))

    def set_bests(self):
        self.population.sort(key=lambda a: a.score, reverse=False)
        self.bests = self.population[:self.one_tenth]

    # @timer
    def calculate_fitness(self):
        pass
