import os
from test_cases import TestCases

key_dict = {
    'Czas Pomiaru': 'date_time',
    'PmGdaPoWie01-PM10-1g': 'pm10',
    'Predkosc wiatru': 'wind',
    'Temperatura powietrza': 'temperature',
    'Wilgotnosc': 'humidity',
}

mongo_ip = os.getenv('MONGO_IP', 'localhost')
mongo_port = os.getenv('MONGO_PORT', '27017')
mongo_user = os.getenv('MONGO_USER', 'root')
mongo_password = os.getenv('MONGO_PASSWORD', 'example')

t = TestCases(
    ip=mongo_ip,
    port=mongo_port,
    user=mongo_user,
    password=mongo_password
)

t.load()

# t.save_from_csv('data.csv')
t.save_from_csv(
    filename='gdansk_2018.csv',
    key_dict=key_dict,
    # delimiter=',',
)
