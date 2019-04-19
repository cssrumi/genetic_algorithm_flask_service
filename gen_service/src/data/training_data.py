from data.data import Data


class TrainingData(Data):
    def __init__(self, data, pm10_after_24h):
        self.__dict__.update(data.__dict__)
        self.pm10_after_24h = pm10_after_24h

    def __repr__(self):
        return '<TrainingData(' + \
               ','.join([key+'='+str(value) for key, value in self.__dict__.items()]) + \
               ')>'
