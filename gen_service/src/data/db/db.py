from interface import implements
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymongo

from data.data_mapper import DataMapper
from data.db.db_param import DBParam
from data.db.model.data_sql_model import SQLData
from data.interfaces import ResultInterface, DataInterface, DB


class SQLModel(implements(ResultInterface, DataInterface, DB)):
    def __init__(self, db_param: DBParam, mapper: DataMapper):
        self.args = db_param
        self.engine = create_engine(self.get_connection_string(), echo=False)
        self._Session = sessionmaker(bind=self.engine)
        self.session = None
        self.mapper = mapper
        # Data.set_table_name(Data, self.args.table_name)

    def get_connection_string(self):
        return 'sqlite:///:memory:'

    def connect(self):
        try:
            self.session = self._Session()
            self._create_table()
            return True
        except Exception as e:
            print(e)

    def test(self):
        if not self.connect():
            raise ConnectionError

    def _create_table(self):
        if not self.engine.dialect.has_table(self.engine, self.args.table_name):
            SQLData.metadata.create_all(self.engine)

    def save_result(self, result):
        pass

    def get_last_results(self, quantity):
        pass

    def save_data(self, data):
        if isinstance(data, dict):
            sql_data = SQLData(**data)
            self.session.add(sql_data)
            self.session.commit()
        elif isinstance(data, list) and isinstance(data[0], dict):
            for d in data:
                sql_data = SQLData(**d)
                self.session.add(sql_data)
            self.session.commit()
        else:
            raise ValueError

    def get_data(self, quantity):
        data_list = []
        if str(quantity).upper() == 'ALL':
            data = self.session \
                .query(SQLData) \
                .order_by(SQLData.date_time) \
                .all()
        else:
            quantity = int(quantity)
            data = self.session \
                .query(SQLData) \
                .order_by(SQLData.date_time) \
                .limit(quantity) \
                .all()
        for d in data:
            data_list.append(self.mapper.get_data_object(d))
        return data_list

    def get_data_by_time(self, how_long, unit):
        pass


class MySql(SQLModel):

    def get_connection_string(self):
        db_type = self.__class__.__name__.lower()
        connection_string = '{}+pymysql://{}:{}@{}:{}/{}'.format(
            db_type, self.args.user, self.args.password,
            self.args.ip, self.args.port, self.args.db_name
        )
        return connection_string


# class MSSQL(SQLModel):
#
#     def __init__(self, db_param: DBParam, mapper: DataMapper):
#         super().__init__(db_param, mapper)
#         self.engine.dialect.default_schema_name = self.args.db_name
#
#     # https://github.com/pymssql/pymssql/pull/309
#     # https://docs.sqlalchemy.org/en/13/dialects/mssql.html#module-sqlalchemy.dialects.mssql.mxodbc
#     def get_connection_string(self):
#         db_type = self.__class__.__name__.lower()
#         connection_string = '{}+pymssql://{}:{}@{}:{}/{}'.format(
#             db_type, self.args.user, self.args.password,
#             self.args.ip, self.args.port, self.args.db_name
#         )
#         return connection_string


class MongoDB(implements(ResultInterface, DataInterface, DB)):
    def __init__(self, db_param: DBParam, mapper: DataMapper):
        self.args = db_param
        self.data_collection = None
        self.results_collection = None
        self.mapper = mapper

    def get_connection_string(self):
        return 'mongodb://{}:{}@{}:{}'.format(
            self.args.user,
            self.args.password,
            self.args.ip,
            self.args.port
        )

    def connect(self):
        try:
            db_client = pymongo.MongoClient(self.get_connection_string())
            data_db = db_client.get_database(self.args.db_name)
            result_db = db_client.get_database(self.args.db_name)
            self.data_collection = data_db[self.args.table_name]  # collection_name
            self.results_collection = result_db.results
        except Exception as e:
            print(e)
            return False
        return True

    def test(self):
        if not self.connect():
            raise ConnectionError

    def save_result(self, result):
        pass

    def get_last_results(self, quantity):
        pass

    def save_data(self, data):
        if isinstance(data, dict):
            self.data_collection.insert_one(data)
        elif isinstance(data, list) and isinstance(data[0], dict):
            for d in data:
                self.data_collection.insert_one(d)
        else:
            raise ValueError

    def get_data(self, quantity):
        data_list = []
        test = False
        while not test:
            try:
                if str(quantity).upper() == 'ALL':
                    data = self.data_collection.find().sort([('date_time', -1)])
                else:
                    quantity = int(quantity)
                    data = self.data_collection.find().sort([('date_time', -1)]).limit(quantity)
                if data is not None:
                    for d in data:
                        data_object = self.mapper.get_data_object(d)
                        data_list.append(data_object)

                test = True
            except Exception as e:
                print(e)
                self.connect()
        return data_list

    def get_data_by_time(self, how_long, unit):
        pass


class DBFactory:
    __db_classes = {
        MySql.__name__.lower(): MySql,
        # MSSQL.__name__.lower(): MSSQL,
        MongoDB.__name__.lower(): MongoDB,
    }
    db_types = __db_classes.keys()

    @staticmethod
    def get_db(db_type):
        db_type = db_type.lower()
        if db_type not in DBFactory.db_types:
            raise ValueError
        else:
            return DBFactory.__db_classes.get(db_type)
