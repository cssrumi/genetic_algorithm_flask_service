import os

from data.data_connector import DataConnectorFactory
from data.data_mapper import DataMapper
from genetic_algorithm.genetic_algorithm_impl import GeneticAlgorithmImpl


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


def main():
    population_size = int(os.getenv('POPULATION_SIZE', '100'))
    max_generation = int(os.getenv('MAX_GENERATION', '10'))
    time_interval = os.getenv('TIME_INTERVAL', '60')  # in minutes

    save_interval_types = ('time', 'generation')
    save_interval_type = os.getenv('SAVE_INTERVAL_TYPE', 'time')
    if save_interval_type.lower() not in save_interval_types:
        save_interval_type = 'time'
    try:
        time_interval = int(time_interval)
    except (ValueError, TypeError):
        time_interval = 60

    dc = get_data_connector()
    while not dc:
        dc = get_data_connector()

    g = GeneticAlgorithmImpl(dc, 100, 100)
    g.run()


if __name__ == '__main__':
    main()
