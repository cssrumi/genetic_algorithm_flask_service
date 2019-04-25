from interface import implements

from data.data_mapper import DataMapper
from data.interfaces import ResultInterface, DataInterface, WebService
from data.web_services.web_service_param import WebServiceParam


class WebServiceImpl(implements(ResultInterface, DataInterface, WebService)):
    def __init__(self, ws_param: WebServiceParam, mapper: DataMapper):
        pass

    def connect(self):
        pass

    def test(self):
        if not self.connect():
            raise ConnectionError

    def save_result(self, result):
        pass

    def get_last_results(self, quantity):
        pass

    def save_data(self, data):
        pass

    def get_data(self, quantity):
        pass

    def get_data_by_time(self, how_long, unit):
        pass


class WebServiceFactory:
    __web_service_classes = {
        WebServiceImpl.__name__.lower(): WebServiceImpl,
    }
    ws_types = __web_service_classes.keys()

    @staticmethod
    def get_ws(ws_type):
        ws_type = ws_type.lower()
        if ws_type not in WebServiceFactory.ws_types:
            raise ValueError
        else:
            return WebServiceFactory.__web_service_classes.get(ws_type)
