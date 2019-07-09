import os
import sys
from typing import Optional

sys.path.append(os.path.abspath("."))
sys.path.append(os.path.join(os.path.abspath("."), 'genetic_algorithm'))

from data.data_connector import DataConnectorFactory
from data.data_mapper import DataMapper
from genetic_algorithm.genetic_algorithm_impl import GeneticAlgorithmImpl

from decorators import until_not_none, logger


class App:
    def __init__(self):
        self.population_size = App.get_as_int('POPULATION_SIZE', 300)
        self.crossover_type = os.getenv('CROSSOVER_TYPE', None)
        self.vitality = App.get_as_int('VITALITY', 3)
        self.pass_best = App.get_as_boolean('PASS_BEST', True)
        self.max_generation = App.get_as_int('MAX_GENERATION', None)
        self.time_interval = App.get_as_int('TIME_INTERVAL', 6)  # in hours
        self.time_unit = os.getenv('TIME_UNIT', 'h')
        self._bootstrap = App.get_as_boolean('BOOTSTRAP', False)

        self._save_interval_types = ('time', 'generation')
        self.save_interval_type = os.getenv('SAVE_INTERVAL_TYPE', 'time')
        if self.save_interval_type.lower() not in self._save_interval_types:
            self.save_interval_type = 'time'

        self.dc = App.get_data_connector()
        self.genetic_algorithm = self.create_genetic_algorithm()

        if self._bootstrap:
            self.bootstrap()

    def bootstrap(self, filename='gdansk_2018.csv') -> None:
        from data.bootstrap.bootstrap import export_data_from_csv, get_abs_path
        export_data_from_csv(get_abs_path(filename), self.dc)

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
        self.results = []

    def get_params(self):
        params = {}
        for key, value in vars(self).items():
            if key[0] != '_' and isinstance(value, (bool, str, int, float)):
                params[key] = value
        return params

    # @logger
    def get_result(self, evolution_type: str) -> dict:
        self.recreate_genetic_algorithm()
        type_name = evolution_type
        self.genetic_algorithm.change_evolution_type(evolution_type)
        best = self.run()
        measurement_error = self.genetic_algorithm.calculate_measurement_error(best)
        result = {'evolution_type': type_name, 'phenotype': best.to_dict(), 'measurement_error': measurement_error,
                  'params': self.get_params()}
        return result

    def test_evolution_types(self):
        types = self.genetic_algorithm.population.get_unique_evolution_types()

        self.pass_best = True
        for t in types:
            result = self.get_result(t)
            self.results.append(result)

        self.pass_best = False
        for t in types:
            result = self.get_result(t)
            self.results.append(result)

    def sort_results(self, reverse=False):
        self.results.sort(key=lambda result: result.get('measurement_error', None), reverse=reverse)

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
    test.time_interval = 4
    test.time_unit = 's'
    test.test_evolution_types()
    test.sort_results()
    test.save_results()


def bootstrap():
    app = App()
    app.bootstrap()


if __name__ == '__main__':
    # main()
    test()
    # bootstrap()
