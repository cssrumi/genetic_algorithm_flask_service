from enum import Enum


class SaveIntervalTypes(Enum):
    TIME = 1
    GENERATION = 2
    GENERATIONS = GENERATION


class TimeUnitTypes(Enum):
    S = 1
    SEC = S
    M = 2
    MIN = M
    H = 3
    HOUR = H
    HOURS = H
    D = 4
    DAYS = 4


class CrossingOverTypes(Enum):
    pass
