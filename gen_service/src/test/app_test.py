class TestDataObject:
    def __init__(self):
        self.Czas_Pomiaru = 123
        self.PmGdaPoWie01_PM10_1g = 5123
        self.Kierunek_wiatru = 666
        self.Predkosc_wiatru = 23
        self.Temperatura_powietrza = 654
        self.Wilgotnosc = 879
        self.Temperatura_punktu_rosy = 1
        self.Cisnienie = 2


map_object = TestDataObject()

default_key_dict = {
    'date_time': 'Czas_Pomiaru',
    'pm10': 'PmGdaPoWie01_PM10_1g',
    'wind_direction': 'Kierunek_wiatru',
    'wind': 'Predkosc_wiatru',
    'temperature': 'Temperatura_powietrza',
    'humidity': 'Wilgotnosc',
    'dew_point': 'Temperatura_punktu_rosy',
    'pressure': 'Cisnienie',
}


def data_mapper_test():
    from data.data_mapper import DataMapper

    try:
        dm = DataMapper(default_key_dict)
        data = dm.get_data_object(map_object)
        print(data)
    except Exception as e:
        print(e)
    print('DataMapper test completed')


def training_data_test():
    from data.data_mapper import DataMapper
    from data.training_data import TrainingData

    try:
        dm = DataMapper(default_key_dict)
        data = dm.get_data_object(map_object)

        td = TrainingData(data, pm10_after_24h=1111)
        print(td)
    except Exception as e:
        print(e)
    print('TrainingData test completed')


def mongodb_test():
    from data.data_connector import DataConnectorFactory
    from data.data_mapper import DataMapper

    db_type = 'mongodb'
    dm = DataMapper(DataMapper.get_default_mapping())
    print(DataMapper.get_default_mapping())
    MongoDB = DataConnectorFactory.get_data_connector(db_type)
    mongodb_param = DataConnectorFactory.get_dc_param(db_type)
    mongo = MongoDB(mongodb_param, dm)
    mongo.connect()
    data = mongo.get_data(1)
    print(data)
    print('MongoDB test completed')


if __name__ == '__main__':
    data_mapper_test()
    training_data_test()
    mongodb_test()
