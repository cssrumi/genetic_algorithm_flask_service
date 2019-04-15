from interface import implements

from db.db_param import DBParam
from db.interfaces import ResultInterface, TestCaseInterface, DB


class SQLModel(implements(DB, ResultInterface, TestCaseInterface)):
    def __init__(self, db_param: DBParam):
        pass

    def connect(self):
        pass

    def test(self):
        if not self.connect():
            raise ConnectionError

    def save_result(self, result):
        pass

    def get_last_results(self, how_many):
        pass

    def get_test_cases(self, how_many):
        pass

    def get_test_cases_by_time(self, how_long, unit):
        pass


class MySql(SQLModel):
    pass


class MSSQL(SQLModel):
    pass


class MongoDB(implements(DB, ResultInterface, TestCaseInterface)):
    def __init__(self, db_param: DBParam):
        pass

    def connect(self):
        pass

    def test(self):
        if not self.connect():
            raise ConnectionError

    def save_result(self, result):
        pass

    def get_last_results(self, how_many):
        pass

    def get_test_cases(self, how_many):
        pass

    def get_test_cases_by_time(self, how_long, unit):
        pass


class DBFactory:
    __db_classes = {
        MySql.__name__: MySql,
        MSSQL.__name__: MSSQL,
        MongoDB.__name__: MongoDB,
    }
    db_types = __db_classes.keys()

    @staticmethod
    def get_db(db_type):
        if db_type not in DBFactory.db_types:
            raise ValueError
        else:
            return DBFactory.__db_classes.get(db_type)
