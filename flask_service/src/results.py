from datetime import datetime

import pymongo
from bson import json_util


class Results:
    def __init__(self, ip, port, user, password):
        self.results_collection = None
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

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
                db = db_client.results
                self.results_collection = db.results
                test = True
            except Exception as e:
                print(e)

    def save(self, result):
        try:
            result['date_time'] = datetime.now().timestamp()
            self.results_collection.insert_one(result)
        except Exception as e:
            print(e)

    def get_last(self):
        test = False
        found = {}
        while not test:
            try:
                if self.results_collection.find_one() is not None:
                    found = self.results_collection.find().sort([('date_time', -1)]).limit(1)
                test = True
            except Exception as e:
                print(e)
                self.load()
        return json_util.dumps(found)

    def get_all(self):
        test = False
        while not test:
            try:
                return json_util.dumps(list(self.results_collection.find()))
            except Exception as e:
                print(e)
                self.load()
