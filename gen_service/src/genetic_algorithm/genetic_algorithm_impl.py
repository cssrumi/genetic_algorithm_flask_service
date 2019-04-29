from data.training_data import create_training_data, TrainingData
from genetic_algorithm.phenotype import Phenotype
from decorators import timer


class GeneticAlgorithmImpl:
    def __init__(self, data_connector, population_size=100, max_generation=100):
        self.data_connector = data_connector
        self.population_size = population_size
        self.max_generation = max_generation
        self.population = []
        self.bests = []
        self.one_tenth = int(population_size / 10)
        self.training_data = None
        self.populate()
        self.set_training_data()

    def set_training_data(self, quantity='ALL'):
        data = self.data_connector.get_data(quantity)
        self.training_data = create_training_data(data)

    def run(self):
        if self.max_generation is not None:
            for _ in range(self.max_generation):
                self.evolve_population()
        else:
            while True:
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
        self.population.sort(key=lambda a: a.fitness, reverse=False)
        self.bests = self.population[:self.one_tenth]

    @timer
    def calculate_fitness(self):
        for individual in self.population:
            fitness = 0
            for td in self.training_data:
                fitness += abs(individual.calculate_fitness(td))
            individual.fitness = fitness

    @staticmethod
    def _calc(args):
        individual, td = args
        individual.fitness = sum((abs(individual.calculate_fitness(t)) for t in td))

    @timer
    def calculate_fitness_in_parallel(self):
        from multiprocessing import Pool
        import itertools

        with Pool() as executor:
            executor.map(
                self._calc,
                itertools.zip_longest(
                    self.population,
                    [self.training_data],
                    fillvalue=self.training_data
                )
            )

