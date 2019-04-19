class Data:
    def __init__(self, date_time, pm10, wind_direction, wind, temperature, humidity, dew_point, pressure):
        self.date_time = date_time
        self.pm10 = pm10
        self.wind_direction = wind_direction
        self.wind = wind
        self.temperature = temperature
        self.humidity = humidity
        self.dew_point = dew_point
        self.pressure = pressure

    def __repr__(self):
        return '<Data(' +\
               ','.join([key+'='+str(value) for key, value in self.__dict__.items()]) + \
               ')>'
