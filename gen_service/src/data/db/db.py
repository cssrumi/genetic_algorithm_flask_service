from interface import implements
from sqlalchemy import create_engine

from data.db.db_param import DBParam
from data.interfaces import ResultInterface, TestCaseInterface, DB


class SQLModel(implements(ResultInterface, TestCaseInterface, DB)):
    def __init__(self, db_param: DBParam):
        self.args = db_param
        self.engine = create_engine(self.get_connection_string())

    def get_connection_string(self):
        return 'sqlite:///:memory:'

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

    def get_connection_string(self):
        db_type = self.__class__.__name__.lower()
        connection_string = '{}+pymysql://{}:{}@{}:{}/{}'.format(
            db_type, self.args.user, self.args.password,
            self.args.ip, self.args.port, self.args.db_name
        )
        return connection_string


class MSSQL(SQLModel):
    pass


class MongoDB(implements(ResultInterface, TestCaseInterface, DB)):
    def __init__(self, db_param: DBParam):
        pass

    def get_connection_string(self):
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
