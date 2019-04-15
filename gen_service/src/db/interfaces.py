from interface import Interface

from db.db_param import DBParam


class ResultInterface(Interface):

    def save_result(self, result):
        pass

    def get_last_results(self, how_many):
        pass


class TestCaseInterface(Interface):

    def get_test_cases(self, how_many):
        pass

    def get_test_cases_by_time(self, how_long, unit):
        pass


class DB(Interface):
    def __init__(self, db_param: DBParam):
        pass

    def connect(self):
        pass

    def test(self):
        pass
