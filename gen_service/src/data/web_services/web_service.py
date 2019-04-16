from interface import implements

from data.interfaces import ResultInterface, TestCaseInterface, WebService
from data.web_services.web_service_param import WebServiceParam


class WebServiceImpl(implements(ResultInterface, TestCaseInterface, WebService)):
    def __init__(self, ws_param: WebServiceParam):
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


class WebServiceFactory:
    __web_service_classes = {
        WebServiceImpl.__name__: WebServiceImpl,
    }
    ws_types = __web_service_classes.keys()

    @staticmethod
    def get_ws(ws_type):
        if ws_type not in WebServiceFactory.ws_types:
            raise ValueError
        else:
            return WebServiceFactory.__web_service_classes.get(ws_type)
