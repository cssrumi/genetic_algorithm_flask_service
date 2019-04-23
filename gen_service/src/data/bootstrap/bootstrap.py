import csv
import os
from datetime import datetime

d_key_dict = {
    'Czas Pomiaru': 'date_time',
    'PmGdaPoWie01-PM10-1g': 'pm10',
    'Kierunek wiatru': 'wind_direction',
    'Predkosc wiatru': 'wind',
    'Temperatura powietrza': 'temperature',
    'Wilgotnosc': 'humidity',
    'Temperatura punktu rosy': 'dew_point',
    'Cisnienie': 'pressure'

}


def get_abs_path(file_path):
    file = os.path.abspath(__file__)
    f_dir = os.path.dirname(file)
    csv_file = os.path.join(f_dir, file_path)
    return os.path.abspath(csv_file)


def export_data_from_csv(filename, db, key_dict=d_key_dict, delimiter=',', dt_format="%Y-%m-%d %H:%M"):
    result = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for r in reader:
            temp_dict = {}
            if '' in r.values():
                continue
            for k, v in key_dict.items():
                if v == 'date_time':
                    temp_dict[v] = int(datetime.strptime(r.get(k).strip(), dt_format).timestamp())
                else:
                    temp_dict[v] = r.get(k).strip()

            result.append(temp_dict)
    db.save_data(result)
