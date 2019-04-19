from interface import Interface

from data.data_mapper import DataMapper
from data.db.db_param import DBParam
from data.web_services.web_service_param import WebServiceParam


class ResultInterface(Interface):

    def save_result(self, result):
        pass

    def get_last_results(self, how_many):
        pass


class TestCaseInterface(Interface):

    def get_data(self, how_many):
        pass

    def get_data_by_time(self, how_long, unit):
        pass


class Connector(Interface):

    def connect(self):
        pass

    def test(self):
        pass


class DB(Connector):

    def __init__(self, db_param: DBParam, mapper: DataMapper):
        pass

    def get_connection_string(self):
        pass


class WebService(Connector):

    def __init__(self, ws_param: WebServiceParam, mapper: DataMapper):
        pass
