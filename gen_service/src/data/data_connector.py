import os

from data.db.db import DBFactory
from data.db.db_param import DBParam
from data.web_services.web_service import WebServiceFactory
from data.web_services.web_service_param import WebServiceParam


class DataConnectorFactory:
    dc_types = list(DBFactory.db_types) + list(WebServiceFactory.ws_types)

    @staticmethod
    def get_data_connector(dc_type):
        if dc_type in DBFactory.db_types:
            return DBFactory.get_db(dc_type)
        elif dc_type in WebServiceFactory.ws_types:
            return WebServiceFactory.get_ws(dc_type)
        else:
            raise ValueError

    @staticmethod
    def get_dc_param(dc_type):
        if dc_type in DBFactory.db_types:
            return DBParam(
                ip=os.getenv('DATA_CONNECTOR_IP', 'localhost'),
                port=os.getenv('DATA_CONNECTOR_PORT', '27017'),
                user=os.getenv('DATA_CONNECTOR_USER', 'root'),
                password=os.getenv('DATA_CONNECTOR_PASSWORD', 'root'),
                db_name=os.getenv('DATABASE_NAME', 'root'),
            )
        elif dc_type in WebServiceFactory.ws_types:
            return WebServiceParam(
                ip=os.getenv('DATA_CONNECTOR_IP', 'localhost'),
                port=os.getenv('DATA_CONNECTOR_PORT', '27017'),
                user=os.getenv('DATA_CONNECTOR_USER', ''),
                password=os.getenv('DATA_CONNECTOR_PASSWORD', '')
            )
        else:
            raise ValueError
