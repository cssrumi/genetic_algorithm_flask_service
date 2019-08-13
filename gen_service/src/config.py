import os
from typing import Optional


class Config:
    def __init__(self):
        self.save_interval_types = ('time', 'generation')
        self.population_size = None
        self.crossover_type = None
        self.max_vitality = None
        self.pass_best = None
        self.max_generation = None
        self.children_max = None
        self.time_interval = None
        self.time_unit = None
        self.crossover_chance = None
        self.mutation_chance = None
        self.bootstrap = None
        self.save_interval_type = None

        self.reload()

    @staticmethod
    def get_as_int(variable: str, default: Optional[int]) -> Optional[int]:
        var = os.getenv(variable.upper(), default)
        try:
            var = int(var)
        except (ValueError, TypeError):
            var = default
        return var

    @staticmethod
    def get_as_float(variable: str, default: Optional[float]) -> Optional[float]:
        var = os.getenv(variable.upper(), default)
        try:
            if '%' in var:
                var = float(var.replace('%', '').strip()) / 100
            else:
                var = float(var)
        except (ValueError, TypeError):
            var = default
        return var

    @staticmethod
    def get_as_str(variable: str, default: Optional[str]) -> Optional[str]:
        var = os.getenv(variable.upper(), default)
        try:
            var = str(var)
        except (ValueError, TypeError):
            var = default
        finally:
            var.lower()
        return var

    @staticmethod
    def get_as_boolean(variable: str, default: Optional[bool]) -> Optional[bool]:
        var = os.getenv(variable.upper(), default)
        try:
            var = bool(var)
        except (ValueError, TypeError):
            var = default
        return var

    def reload(self):
        self.population_size = Config.get_as_int('POPULATION_SIZE', 200)
        self.crossover_type = Config.get_as_str('CROSSOVER_TYPE', None)
        self.max_vitality = Config.get_as_int('MAX_VITALITY', 7)
        self.pass_best = Config.get_as_boolean('PASS_BEST', True)
        self.max_generation = Config.get_as_int('MAX_GENERATION', None)
        self.children_max = Config.get_as_int('CHILDREN_MAX', 50)
        self.crossover_chance = Config.get_as_float('CROSSOVER_CHANCE', 0.8)
        self.mutation_chance = Config.get_as_float('MUTATION_CHANCE', 0.9)
        self.time_interval = Config.get_as_int('TIME_INTERVAL', 6)  # in hours
        self.time_unit = Config.get_as_str('TIME_UNIT', 'h')
        self.bootstrap = Config.get_as_boolean('BOOTSTRAP', False)

        self.save_interval_type = Config.get_as_str('SAVE_INTERVAL_TYPE', 'time')
        if self.save_interval_type not in self.save_interval_types:
            self.save_interval_type = 'time'
