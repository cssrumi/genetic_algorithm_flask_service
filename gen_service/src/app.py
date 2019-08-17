import os
import sys
from typing import Optional
#
# sys.path.append(os.path.abspath("."))
# sys.path.append(os.path.join(os.path.abspath("."), 'genetic_algorithm'))
from config import Config
from data.data_connector import DataConnectorFactory
from data.data_mapper import DataMapper
from decorators import until_not_none, logger
from genetic_algorithm.genetic_algorithm_impl import GeneticAlgorithmImpl


class App:
    def __init__(self, cfg: Optional[Config] = None, data_connector=None):
        if cfg:
            self.cfg = cfg
        else:
            self.cfg = Config()

        if data_connector:
            self.dc = data_connector
        else:
            self.dc = App.get_data_connector()
        self.genetic_algorithm = self.create_genetic_algorithm()

        if self.cfg.bootstrap:
            self.bootstrap()

    def bootstrap(self, filename='gdansk_2018.csv', key_dict=None) -> None:
        from data.bootstrap.bootstrap import export_data_from_csv, get_abs_path
        if key_dict:
            export_data_from_csv(get_abs_path(filename), self.dc, key_dict=key_dict)
        else:
            export_data_from_csv(get_abs_path(filename), self.dc)

    @staticmethod
    @until_not_none
    def get_data_connector(data_mapper: DataMapper = None):
        dc_type = os.getenv('DATA_CONNECTOR_TYPE', 'mongodb')
        if dc_type.lower() not in DataConnectorFactory.dc_types:
            dc_type = 'mongodb'

        try:
            if data_mapper:
                dm = data_mapper
            else:
                dm = DataMapper(DataMapper.get_default_mapping())
            DataConnector = DataConnectorFactory.get_data_connector(dc_type)
            dc_param = DataConnectorFactory.get_dc_param(dc_type)
            dc = DataConnector(dc_param, dm)
            dc.test()
            return dc
        except (ValueError, ConnectionError) as e:
            print(e)

    def recreate_genetic_algorithm(self):
        self.genetic_algorithm = self.create_genetic_algorithm()

    def create_genetic_algorithm(self) -> GeneticAlgorithmImpl:
        return GeneticAlgorithmImpl(
            data_connector=self.dc,
            cfg=self.cfg
        )

    def run(self):
        return self.genetic_algorithm.run()


class Test(App):

    def __init__(self, cfg: Optional[Config] = None, data_connector=None):
        super().__init__(cfg, data_connector)
        self.results = []

    def get_params(self):
        params = {}
        for key, value in vars(self.cfg).items():
            if key[0] != '_' and isinstance(value, (bool, str, int, float)):
                params[key] = value
        return params

    @logger
    def get_result(self, evolution_type: str = 'default') -> dict:
        self.recreate_genetic_algorithm()
        type_name = evolution_type
        self.genetic_algorithm.change_evolution_type(evolution_type)
        best = self.run()
        average_relative_error = self.genetic_algorithm.calculate_average_relative_error(best)
        average_error = self.genetic_algorithm.calculate_average_error(best)
        result = {'evolution_type': type_name, 'individual': best.to_dict(),
                  'average_relative_error': average_relative_error, 'average_error': average_error,
                  'params': self.get_params()}
        return result

    def test_evolution_types(self):
        types = self.genetic_algorithm.population.get_unique_evolution_types()

        self.cfg.pass_best = True
        for t in types:
            result = self.get_result(t)
            self.results.append(result)

        self.cfg.pass_best = False
        for t in types:
            result = self.get_result(t)
            self.results.append(result)

    def test_default(self):
        result = self.get_result()
        self.results.append(result)

    def sort_results(self, reverse=False):
        self.results.sort(key=lambda result: result.get('average_relative_error', None), reverse=reverse)

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
    test.time_interval = 10
    test.time_unit = 's'
    test.test_evolution_types()
    test.sort_results()
    test.save_results()


def test_default():
    test = Test()
    test.cfg.max_generation = 400
    test.cfg.mutation_chance = 1
    test.cfg.crossover_chance = 1
    test.test_default()
    test.save_results()


def bootstrap():
    app = App()
    app.bootstrap()


def bootstrap_a():
    key_dict = {
        'date': 'date_time',
        'pm10': 'pm10',
        'wind direction': 'wind_direction',
        'wind strength': 'wind',
        'temp': 'temperature',
        'humidity': 'humidity',
        'dew point': 'dew_point',
        'air pres.': 'pressure'
    }
    data_connector = App.get_data_connector(key_dict)
    app = App(data_connector=data_connector)
    app.bootstrap(filename='daneArka.csv', key_dict=key_dict)


if __name__ == '__main__':
    # main()
    # test()
    test_default()
    # test_a()
    # bootstrap()
    # bootstrap_a()
