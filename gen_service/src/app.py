import os

from data.data_connector import DataConnectorFactory
from data.data_mapper import DataMapper


def init():
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

    dc_type = os.getenv('DATA_CONNECTOR_TYPE', 'mongodb')
    if dc_type.lower() not in DataConnectorFactory.dc_types:
        dc_type = 'mongodb'

    try:
        dm = DataMapper(DataMapper.get_default_mapping())
        DataConnector = DataConnectorFactory.get_data_connector(dc_type)
        dc_param = DataConnectorFactory.get_dc_param(dc_type)
        dc = DataConnector(dc_param, dm)
        dc.test()
    except (ValueError, ConnectionError) as e:
        print(e)


# @timer
def main():
    init()


if __name__ == '__main__':
    main()
    from time import sleep
    sleep(100)
