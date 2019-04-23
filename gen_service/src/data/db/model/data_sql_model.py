import os
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping
class SQLData(Base):
    __tablename__ = os.getenv('TABLE_NAME', 'data')

    id = Column(Integer, primary_key=True)
    date_time = Column(Integer)
    pm10 = Column(Float)
    wind_direction = Column(Float)
    wind = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    dew_point = Column(Float)
    pressure = Column(Float)

    def __repr__(self):
        return '<' + self.__class__.__name__ + '(' + \
               ','.join([key + '=' + str(value) for key, value in self.__dict__.items()]) + \
               ')>'
