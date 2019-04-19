from sqlalchemy import Column, Integer, DECIMAL, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping
class Data(Base):
    __tablename__ = ''

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<Data(id={}>".format(self.id)
