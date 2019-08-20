import logging
import threading
import os
from enum import Enum
from typing import Optional

import enums

module_logger = logging.getLogger('genetic_algorithm.config')


class Config:
    __instance = None
    __lock = threading.Lock()
    __props = {
        'save_interval_type': {'type': enums.SaveIntervalTypes, 'default': enums.SaveIntervalTypes.TIME},
        'population_size': {'type': int, 'default': 200},
        'crossover_type': {'type': str, 'default': None},
        'vitality': {'type': int, 'default': 7},
        'pass_best': {'type': bool, 'default': True},
        'max_generation': {'type': int, 'default': None},
        'max_crossover': {'type': int, 'default': 50},
        'time_interval': {'type': int, 'default': 1},
        'time_unit': {'type': enums.TimeUnitTypes, 'default': enums.TimeUnitTypes.H},
        'crossover_chance': {'type': float, 'default': 0.8},
        'mutation_chance': {'type': float, 'default': 0.9},
        'bootstrap': {'type': bool, 'default': False},
    }

    @staticmethod
    def get_instance():
        return Config()

    def __new__(cls):
        with Config.__lock:
            if not Config.__instance:
                Config.__instance = object.__new__(cls)
                Config.__instance.logger = logging.getLogger('genetic_algorithm.config.Config')
                Config.__instance._load()
        return Config.__instance

    def _load(self):
        self._load_from_env()
        self.logger.info('Config loaded')

    def reload(self):
        with self.__lock:
            self._load()

    def _load_from_yaml(self):
        pass

    def _load_from_env(self):
        for key, key_dict in self.__props.items():
            r_type = key_dict.get('type')
            default = key_dict.get('default')
            value = self.getenv(key, r_type, default)
            setattr(self, key, value)

    def getenv(self, key, r_type, default):
        var = None
        try:
            if issubclass(r_type, Enum):
                var = self.env_as_enum(key, r_type)
            else:
                var = self.env_of_type(key, r_type)
        except (TypeError, ValueError) as e:
            self.logger.warning('Key: {}, Value: {}, Error: {}'.format(key, os.getenv(key), e), exc_info=False)
            if self.check_default(default, r_type):
                var = default

        self.logger.info('Config variable {} is set to {}'.format(key, var))
        return var

    def check_default(self, default, r_type, none=True):
        if isinstance(default, r_type) or issubclass(type(default), r_type):
            return True
        if none and default is None:
            return True
        raise TypeError('Default value: {} isn\'t instance or child of type: '.format(default, r_type))

    def env_of_type(self, variable, r_type):
        str_var = os.getenv(variable.upper())
        if str_var:
            str_var.upper()
        return r_type(str_var)

    def env_as_enum(self, variable, enum):
        var = os.getenv(variable.upper()).upper()
        enum_values = [e.name for e in enum]
        if var in enum_values:
            return enum[var]
        else:
            raise TypeError(
                'Invalid enum type: "{}" for {} \n'
                '\tValid types: {}'.format(var, variable, enum_values)
            )
