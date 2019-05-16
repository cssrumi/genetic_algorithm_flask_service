# import cython

# @cython.auto_pickle(True)
# @cython.final
cdef class CyData:
    cdef long double _date_time
    cdef long double _pm10
    cdef long double _wind_direction
    cdef long double _wind
    cdef long double _temperature
    cdef long double _humidity
    cdef long double _dew_point
    cdef long double _pressure
    cdef list _KEYS

    def __cinit__(self, date_time, pm10, wind_direction, wind,
                  temperature, humidity, dew_point, pressure):
        self._date_time = <long double> date_time
        self._pm10 = <long double> pm10
        self._wind_direction = <long double> wind_direction
        self._wind = <long double> wind
        self._temperature = <long double> temperature
        self._humidity = <long double> humidity
        self._dew_point = <long double> dew_point
        self._pressure = <long double> pressure
        self._KEYS = ['date_time', 'pm10', 'wind_direction', 'wind',
                      'temperature', 'humidity', 'dew_point', 'pressure']

    property date_time:
        def __get__(self):
            return self._date_time

    property pm10:
        def __get__(self):
            return self._pm10

    property wind_direction:
        def __get__(self):
            return self._wind_direction

    property wind:
        def __get__(self):
            return self._wind

    property temperature:
        def __get__(self):
            return self._temperature

    property humidity:
        def __get__(self):
            return self._humidity

    property dew_point:
        def __get__(self):
            return self._dew_point

    property pressure:
        def __get__(self):
            return self._pressure

    property KEYS:
        def __get__(self):
            return self._KEYS

    def __reduce__(self):
        return (self.__class__, (self.date_time, self.pm10, self.wind_direction, self.wind,
                                 self.temperature, self.humidity, self.dew_point, self.pressure))

    def __repr__(self):
        return '<' + self.__class__.__name__ + '(' + \
               ','.join([key + '=' + str(getattr(self, key)) for key in self._KEYS]) + \
               ')>'

cdef class Data:
    cdef long double date_time
    cdef long double pm10
    cdef long double wind_direction
    cdef long double wind
    cdef long double temperature
    cdef long double humidity
    cdef long double dew_point
    cdef long double pressure
    cdef list KEYS

    def __init__(self, date_time, pm10, wind_direction, wind,
                 temperature, humidity, dew_point, pressure):
        self.date_time = <long double> date_time
        self.pm10 = <long double> pm10
        self.wind_direction = <long double> wind_direction
        self.wind = <long double> wind
        self.temperature = <long double> temperature
        self.humidity = <long double> humidity
        self.dew_point = <long double> dew_point
        self.pressure = <long double> pressure
        self.KEYS = ['date_time', 'pm10', 'wind_direction', 'wind',
                     'temperature', 'humidity', 'dew_point', 'pressure']

    def __reduce__(self):
        return (self.__class__, (self.date_time, self.pm10, self.wind_direction, self.wind,
                                 self.temperature, self.humidity, self.dew_point, self.pressure))

    def __repr__(self):
        return '<' + self.__class__.__name__ + '(' + \
               ','.join([key + '=' + str(getattr(self, key)) for key in self.KEYS]) + \
               ')>'
