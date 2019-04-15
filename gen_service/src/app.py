import os
from db.db import DBFactory
from db.db_param import DBParam


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

    db_type = os.getenv('DB_TYPE', 'mongodb')
    if db_type.lower() not in DBFactory.db_types:
        db_type = 'mongodb'

    try:
        db = DBFactory.get_db(db_type)
        db_param = DBParam(
            ip=os.getenv('DB_IP', 'localhost'),
            port=os.getenv('DB_PORT', '27017'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'root')
        )
        db(db_param)
        db.test()
    except (ValueError, ConnectionError) as e:
        print(e)


# @timer
def main():
    init()


if __name__ == '__main__':
    main()
