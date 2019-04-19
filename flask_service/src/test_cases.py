import csv
from datetime import datetime
import pymongo
from bson import json_util

test_list = ['temperature', 'humidity', 'wind', 'pm10']
default_key_dict = {
    'Czas Pomiaru': 'date_time',
    'PmGdaPoWie01-PM10-1g': 'pm10',
    'Predkosc wiatru': 'wind',
    'Temperatura powietrza': 'temperature',
    'Wilgotnosc': 'humidity',
}

test_values = {'temperature', 'humidity', 'wind'}
test_types = [
    {'a': 'temperature', 'b': 'humidity', 'c': 'wind', 'res': 'pm10'},
    {'a': 'temperature', 'b': 'wind', 'c': 'humidity', 'res': 'pm10'},
    {'a': 'humidity', 'b': 'temperature', 'c': 'wind', 'res': 'pm10'},
    {'a': 'wind', 'b': 'temperature', 'c': 'humidity', 'res': 'pm10'},
    {'a': 'humidity', 'b': 'wind', 'c': 'temperature', 'res': 'pm10'},
    {'a': 'wind', 'b': 'humidity', 'c': 'temperature', 'res': 'pm10'}
]

_test_cases = [
    {'temperature': 5, 'humidity': 0.1, 'wind': 10, 'pm10': 245},
    {'temperature': 5, 'humidity': 0.1, 'wind': 10, 'pm10': 245},
    {'temperature': 5, 'humidity': 0.1, 'wind': 10, 'pm10': 245},
    {'temperature': 5, 'humidity': 0.1, 'wind': 10, 'pm10': 245},
]


class TestCases:
    def __init__(self, ip, port, user, password):
        self.test_cases_collection = None
        self.test_cases = None
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

    def get_tests(self):
        if self.test_cases is None:
            return _test_cases
        return self.test_cases

    def load(self):
        connection_string = 'mongodb://{}:{}@{}:{}'.format(
            self.user,
            self.password,
            self.ip,
            self.port,
        )

        test = False
        while not test:
            try:
                db_client = pymongo.MongoClient(connection_string)
                db = db_client.test_cases
                self.test_cases_collection = db.test_cases
                test = True
            except Exception as e:
                print(e)
                test = False

    def set_test_cases(self, how_many):
        test = False
        while not test:
            try:
                if how_many != TestCases.HOW_MANY.ALL:
                    test_cases = self.test_cases_collection.find().sort([('date_time', -1)]).limit(how_many)
                else:
                    test_cases = self.test_cases_collection.find().sort([('date_time', -1)])
                if test_cases is not None:
                    self.test_cases = []
                    for test_case in test_cases:
                        temp = {}
                        for k in test_list:
                            temp[k] = float(test_case.get(k))
                        self.test_cases.append(temp)

                test = True
            except Exception as e:
                print(e)
                self.load()

    def get_all(self):
        test = False
        while not test:
            try:
                return json_util.dumps(list(self.test_cases_collection.find()))
            except Exception as e:
                print(e)
                self.load()

    def save_from_csv(self, filename, delimiter=',', dt_format="%Y-%m-%d %H:%M", key_dict=default_key_dict):
        result = []
        with open(filename, 'r') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for r in reader:
                temp_dict = {}
                for k, v in default_key_dict.items():
                    if v == 'date_time':
                        temp_dict[v] = int(datetime.strptime(r.get(k).strip(), dt_format).timestamp())
                    else:
                        temp_dict[v] = r.get(k).strip()

                result.append(temp_dict)
        for r in result:
            self.save(r)

    def save(self, test_case):
        try:
            if not test_case.get('date_time', None):
                test_case['date_time'] = datetime.now()
            self.test_cases_collection.insert_one(test_case)
        except Exception as e:
            print(e)

    class _Const:

        @property
        def ALL(self):
            return 'ALL'

        @property
        def LAST(self):
            return 1

        @property
        def LAST_5(self):
            return 5

        @property
        def LAST_10(self):
            return 10

        @property
        def LAST_DAY(self):
            return 24

        @property
        def LAST_30DAYS(self):
            return 24 * 30

    HOW_MANY = _Const()
