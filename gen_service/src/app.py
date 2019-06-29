import os
import sys
from typing import Optional

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.join(os.path.abspath("."), 'genetic_algorithm'))

from data.data_connector import DataConnectorFactory
from data.data_mapper import DataMapper
from genetic_algorithm.genetic_algorithm_impl import GeneticAlgorithmImpl

from decorators import until_not_none


class App:
    def __init__(self):
        self.population_size = App.get_as_int('POPULATION_SIZE', 300)
        self.crossover_type = os.getenv('CROSSOVER_TYPE', None)
        self.vitality = App.get_as_int('VITALITY', 3)
        self.pass_best = App.get_as_boolean('PASS_BEST', True)
        self.max_generation = App.get_as_int('MAX_GENERATION', None)
        self.time_interval = App.get_as_int('TIME_INTERVAL', 6)  # in hours
        self.time_unit = os.getenv('TIME_UNIT', 'h')

        self.save_interval_types = ('time', 'generation')
        self.save_interval_type = os.getenv('SAVE_INTERVAL_TYPE', 'time')
        if self.save_interval_type.lower() not in self.save_interval_types:
            self.save_interval_type = 'time'

        self.dc = App.get_data_connector()
        self.genetic_algorithm = self.create_genetic_algorithm()

    @staticmethod
    @until_not_none
    def get_data_connector():
        dc_type = os.getenv('DATA_CONNECTOR_TYPE', 'mongodb')
        if dc_type.lower() not in DataConnectorFactory.dc_types:
            dc_type = 'mongodb'

        try:
            dm = DataMapper(DataMapper.get_default_mapping())
            DataConnector = DataConnectorFactory.get_data_connector(dc_type)
            dc_param = DataConnectorFactory.get_dc_param(dc_type)
            dc = DataConnector(dc_param, dm)
            dc.test()
            return dc
        except (ValueError, ConnectionError) as e:
            print(e)

    @staticmethod
    def get_as_int(variable: str, default: Optional[int]) -> Optional[int]:
        var = os.getenv(variable.upper(), default)
        try:
            var = int(var)
        except (ValueError, TypeError):
            var = default
        return var

    @staticmethod
    def get_as_boolean(variable: str, default: Optional[bool]) -> Optional[bool]:
        var = os.getenv(variable.upper(), default)
        try:
            var = bool(var)
        except (ValueError, TypeError):
            var = default
        return var

    def recreate_genetic_algorithm(self):
        self.genetic_algorithm = self.create_genetic_algorithm()

    def create_genetic_algorithm(self) -> GeneticAlgorithmImpl:
        return GeneticAlgorithmImpl(
            data_connector=self.dc,
            population_size=self.population_size,
            max_generation=self.max_generation,
            time_interval=self.time_interval,
            time_unit=self.time_unit,
            vitality=self.vitality,
            pass_best=self.pass_best
        )

    def run(self):
        return self.genetic_algorithm.run()


class Test(App):

    def __init__(self):
        super().__init__()
        self.results = {}

    def test_evolution_types(self):
        types = self.genetic_algorithm.population.get_unique_evolution_types()
        for t in types:
            self.recreate_genetic_algorithm()
            type_name = t.__name__.replace('_', ' ').strip(' ')
            self.genetic_algorithm.population._evolve = t
            best = self.run()
            measurement_error = self.genetic_algorithm.calculate_measurement_error(best)
            best_dict = {'phenotype': best.to_dict(), 'measurement_error': measurement_error}
            self.results[type_name] = best_dict

    def save_results(self, filename='results.json'):
        import json

        with open(filename, 'w+') as f:
            json.dump(self.results, f)


def main():
    app = App()
    best = app.run()
    print(best)


def test():
    test = Test()
    test.time_interval = 6
    test.time_unit = 'h'
    test.test_evolution_types()
    test.save_results()


if __name__ == '__main__':
    # main()
    test()


# OLD


def get_data_connector() -> object:
    dc_type = os.getenv('DATA_CONNECTOR_TYPE', 'mongodb')
    if dc_type.lower() not in DataConnectorFactory.dc_types:
        dc_type = 'mongodb'

    try:
        dm = DataMapper(DataMapper.get_default_mapping())
        DataConnector = DataConnectorFactory.get_data_connector(dc_type)
        dc_param = DataConnectorFactory.get_dc_param(dc_type)
        dc = DataConnector(dc_param, dm)
        dc.test()
        return dc
    except (ValueError, ConnectionError) as e:
        print(e)


def get_as_int(variable: str, default: Optional[int]):
    var = os.getenv(variable.upper(), default)
    try:
        var = int(var)
    except (ValueError, TypeError):
        var = default
    return var


def old_main():
    population_size = get_as_int('POPULATION_SIZE', 300)
    max_generation = get_as_int('MAX_GENERATION', None)
    time_interval = get_as_int('TIME_INTERVAL', 6)  # in hours
    vitality = get_as_int('VITALITY', 3)

    save_interval_types = ('time', 'generation')
    save_interval_type = os.getenv('SAVE_INTERVAL_TYPE', 'time')
    if save_interval_type.lower() not in save_interval_types:
        save_interval_type = 'time'

    dc = get_data_connector()
    while not dc:
        dc = get_data_connector()

    ########
    # MAIN #
    ########
    # g = GeneticAlgorithmImpl(
    #     dc, population_size,
    #     max_generation=max_generation,
    #     time_interval=time_interval,
    #     vitality=vitality
    # )

    ########
    # TEST #
    ########
    g = GeneticAlgorithmImpl(
        dc, population_size,
        max_generation=max_generation,
        time_interval=20,
        time_unit='s',
        vitality=3,
        pass_best=False
    )
    g.run()
