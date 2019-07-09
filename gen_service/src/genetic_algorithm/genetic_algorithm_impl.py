import datetime

from data.training_data import create_training_data
from genetic_algorithm.population import Population


class GeneticAlgorithmImpl:
    def __init__(self, data_connector, population_size=100, max_generation=None, time_interval=None, time_unit='h',
                 vitality=3, pass_best=True):
        self.population_size = population_size
        self.data_connector = data_connector
        self.max_generation = max_generation
        self.time_interval = time_interval
        self.pass_best = pass_best
        self.vitality = vitality
        self.time_unit = str(time_unit).lower()
        self.training_data = self.get_training_data()
        self.population = Population(self.population_size, self.training_data, vitality=self.vitality,
                                     pass_best=self.pass_best)

    def recreate_population(self):
        self.population.clear()
        self.population.populate()

    def create_new_population(self):
        self.population = Population(self.population_size, self.training_data, vitality=self.vitality,
                                     pass_best=self.pass_best)

    def change_evolution_type(self, evolution_type: str):
        self.population._evolve = self.population.get_evolution_type(evolution_type)

    def get_training_data(self, quantity='ALL'):
        data = self.data_connector.get_data(quantity)
        return create_training_data(data)

    def add_training_data(self, quantity=1):
        data = self.data_connector.get_data(quantity)
        self.population.training_data.append(data)

    @staticmethod
    def calculate_relative_error(phenotype, td):
        return (td.pm10_after_24h - phenotype.calculate_pm10(td)) / td.pm10_after_24h

    def calculate_measurement_error(self, phenotype) -> float:
        relative_errors = (
            __class__.calculate_relative_error(phenotype, td)
            for td in self.training_data
        )
        sum_of_relative_errors = sum((abs(re) for re in relative_errors))

        measurement_error = (1 / len(self.training_data)) * sum_of_relative_errors

        return measurement_error

    def get_timer(self):
        now = datetime.datetime.now()
        if not self.time_interval:
            self.time_interval = 60
            self.time_unit = 's'

        time_units = {
            'h': now + datetime.timedelta(hours=self.time_interval),
            'min': now + datetime.timedelta(minutes=self.time_interval),
            's': now + datetime.timedelta(seconds=self.time_interval),
        }

        return time_units.get(self.time_unit.lower())

    def run(self):
        if not self.population:
            self.recreate_population()
        if self.max_generation:
            for _ in range(self.max_generation):
                self.population.evolve()
            return self.population.get_best()
        elif self.time_interval:
            now = datetime.datetime.now()
            timer = self.get_timer()
            while now < timer:
                self.population.evolve()
                now = datetime.datetime.now()
            return self.population.get_best()
        else:
            while True:
                self.population.evolve()
