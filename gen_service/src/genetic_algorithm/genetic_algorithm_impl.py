from data.training_data import create_training_data
from genetic_algorithm.population import Population


class GeneticAlgorithmImpl:
    def __init__(self, data_connector, population_size=100, max_generation=100):
        self.data_connector = data_connector
        self.max_generation = max_generation
        self.population = Population(population_size, self.get_training_data())

    def get_training_data(self, quantity='ALL'):
        data = self.data_connector.get_data(quantity)
        return create_training_data(data)

    def add_training_data(self, quantity=1):
        data = self.data_connector.get_data(quantity)
        self.population.training_data.append(data)

    def run(self):
        if self.max_generation is not None:
            for _ in range(self.max_generation):
                self.population.evolve()
                print(self.population.get_best())
        else:
            while True:
                self.population.evolve()
                print(self.population.get_best())
