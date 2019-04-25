from data.data import Data
from decorators import timer
import datetime


@timer
def create_training_data(data):
    def dtfts(date):
        return datetime.datetime.fromtimestamp(date)

    def min_date(date):
        date = datetime.datetime.fromtimestamp(date)
        date += datetime.timedelta(hours=23, minutes=30)
        return date.timestamp()

    def max_date(date):
        date = datetime.datetime.fromtimestamp(date)
        date += datetime.timedelta(days=1, minutes=30)
        return date.timestamp()

    def nearest(items, pivot):
        if items:
            return min(items, key=lambda x: abs(x.date_time - pivot))

    def equal_date(date):
        date = datetime.datetime.fromtimestamp(date)
        date += datetime.timedelta(days=1)
        return date.timestamp()

    td = []
    data_size = len(data)
    if data_size > 1:
        data.sort(key=lambda x: x.date_time)
    for i in range(data_size):
        d = data[i]
        dt = d.date_time
        max_dt = max_date(dt)
        min_dt = min_date(dt)
        j = 0 + i
        temp = data[j]
        items = []
        while temp.date_time < max_dt and j < data_size:
            temp = data[j]
            if temp.date_time > min_dt:
                items.append(temp)
            j += 1
        d_after_24h = nearest(items, equal_date(dt))
        if d_after_24h:
            td.append(TrainingData(d, d_after_24h.pm10))
    return td


class TrainingData(Data):
    def __init__(self, data, pm10_after_24h):
        self.__dict__.update(data.__dict__)
        self.pm10_after_24h = pm10_after_24h

    def __repr__(self):
        return '<TrainingData(' + \
               ','.join([key + '=' + str(value) for key, value in self.__dict__.items()]) + \
               ')>'
