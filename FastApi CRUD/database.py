from sqlalchemy import Column, Integer, create_engine, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///animal_register.db")

Base = declarative_base()


class Animal(Base):

    __tablename__ = "animals"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer())
    breed = Column(String(100))
    species = Column(String(100))
