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
