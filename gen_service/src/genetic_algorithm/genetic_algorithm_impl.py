import datetime

from config import Config
from data.data_mapper import DataMapper
from data.training_data import create_training_data
from genetic_algorithm.individual import Individual
from genetic_algorithm.population import Population


class GeneticAlgorithmImpl:
    def __init__(self, data_connector, cfg: Config):
        self.data_connector = data_connector
        self.cfg = cfg
        self.training_data = self.get_training_data()
        self.init_individual()
        self.population = Population(self.cfg, self.training_data)

    @staticmethod
    def init_individual():
        dm = DataMapper.get_default_mapping()
        keys = list(dm.keys())
        Individual.set_gen_list(keys)

    def recreate_population(self):
        self.population.clear()
        self.population.populate()

    def create_new_population(self):
        self.population = Population(self.cfg, self.training_data)

    def change_evolution_type(self, evolution_type: str):
        self.population._evolve = self.population.get_evolution_type(evolution_type)

    def get_training_data(self, quantity='ALL'):
        data = self.data_connector.get_data(quantity)
        return create_training_data(data)

    def add_training_data(self, quantity=1):
        data = self.data_connector.get_data(quantity)
        self.population.training_data.append(data)

    def set_mutation_rate(self, individual: Individual):
        mutation_chance = self.calculate_mutation_chance(individual)
        Individual.set_mutation_chance(mutation_chance)

    def calculate_mutation_chance(self, individual: Individual) -> (float, int):
        measurement_error = self.calculate_measurement_error(individual)
        mutation_chance = measurement_error / 10
        return mutation_chance

    @staticmethod
    def calculate_relative_error(individual: Individual, td):
        return (td.pm10_after_24h - individual.calculate_pm10(td)) / td.pm10_after_24h

    def calculate_measurement_error(self, individual: Individual) -> float:
        relative_errors = (
            __class__.calculate_relative_error(individual, td)
            for td in self.training_data
        )
        sum_of_relative_errors = sum((abs(re) for re in relative_errors))

        measurement_error = (1 / len(self.training_data)) * sum_of_relative_errors

        return measurement_error

    def get_timer(self):
        now = datetime.datetime.now()
        if not self.cfg.time_interval:
            self.cfg.time_interval = 60
            self.cfg.time_unit = 's'

        time_units = {
            'h': now + datetime.timedelta(hours=self.cfg.time_interval),
            'min': now + datetime.timedelta(minutes=self.cfg.time_interval),
            's': now + datetime.timedelta(seconds=self.cfg.time_interval),
        }

        if self.cfg.time_unit not in list(time_units.keys()):
            self.cfg.time_unit = 'h'

        return time_units.get(self.cfg.time_unit.lower())

    def run(self):
        if not self.population:
            self.recreate_population()
        if self.cfg.max_generation:
            for _ in range(self.cfg.max_generation):
                self.population.evolve()
                self.set_mutation_rate(self.population.get_current_best())
            return self.population.get_best()
        elif self.cfg.time_interval:
            now = datetime.datetime.now()
            timer = self.get_timer()
            while now < timer:
                self.population.evolve()
                self.set_mutation_rate(self.population.get_current_best())
                now = datetime.datetime.now()
            return self.population.get_best()
        else:
            while True:
                self.population.evolve()
                self.set_mutation_rate(self.population.get_current_best())
