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
        type_dict = {
            str: self.env_as_str,
            int: self.env_as_int,
            float: self.env_as_float,
            bool: self.env_as_boolean,
        }
        if issubclass(r_type, Enum):
            var = self.env_as_enum(key, r_type, default)
        else:
            f = type_dict.get(r_type)
            var = f(key, default)
        self.logger.debug('Config variable {} is set to {}'.format(key, var))
        return var

    def env_as_enum(self, variable, enum, default):
        var = os.getenv(variable.upper()).upper()
        enum_values = [e.name for e in enum]
        if var in enum_values:
            return enum[var]
        else:
            self.logger.error(
                'Invalid enum type: "{}" for {} \n'
                '\tValid types: {}'.format(var, variable, enum_values)
            )
            self.logger.warning('{} value set to default: {}'.format(variable, default))
            return default

    def env_as_int(self, variable: str, default: Optional[int]) -> Optional[int]:
        var = os.getenv(variable.upper(), default)
        try:
            var = int(var)
        except (ValueError, TypeError) as e:
            self.logger.exception(e, exc_info=True)
            var = default
            self.logger.warning('{} value set to default: {}'.format(variable, default))
        return var

    def env_as_float(self, variable: str, default: Optional[float]) -> Optional[float]:
        var = os.getenv(variable.upper())
        try:
            if '%' in var:
                var = float(var.replace('%', '').strip()) / 100
            else:
                var = float(var)
        except (ValueError, TypeError) as e:
            self.logger.exception(e, exc_info=True)
            var = default
            self.logger.warning('{} value set to default: {}'.format(variable, default))
        return var

    def env_as_str(self, variable: str, default: Optional[str]) -> Optional[str]:
        var = os.getenv(variable.upper(), default)
        try:
            var = str(var)
        except (ValueError, TypeError) as e:
            self.logger.exception(e, exc_info=True)
            var = default
            self.logger.warning('{} value set to default: {}'.format(variable, default.lower()))
        finally:
            var.lower()
        return var

    def env_as_boolean(self, variable: str, default: Optional[bool]) -> Optional[bool]:
        var = os.getenv(variable.upper(), default)
        try:
            var = bool(var)
        except (ValueError, TypeError) as e:
            self.logger.exception(e, exc_info=True)
            var = default
            self.logger.warning('{} value set to default: {}'.format(variable, default))
        return var
