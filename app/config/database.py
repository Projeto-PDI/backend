import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.models.registerModel import RegisterModel

Base = declarative_base()

# Database Entities
class Registers(Base):
    __tablename__ = 'registers'

    token = Column(String(255), primary_key=True)
    category = Column(String(255))
    points = Column(JSON)
    infractions = Column(JSON)
    average_speed = Column(Float)
    has_helmet = Column(Boolean)
    license_plate = Column(String(255))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

class DatabaseBuilder:
    def __init__(self):
        print("s")
        #engine = create_engine('mysql+mysqlconnector://root:123456@db:3306/pdi_transport', echo=True)
        #Base.metadata.create_all(engine)

        #Session = sessionmaker(bind=engine)
        #self.session = Session()

    def create_register(self):
        new_register = Registers(
            token='EFGH123',
            category='Carro',
            points='{"x": 10, "y": 20}',
            infractions='[]',
            average_speed=60.5,
            has_helmet=True,
            license_plate='XYZ123',
            start_time='2023-10-01 08:00:00',
            end_time='2023-10-01 18:00:00'
        )

        self.session.add(new_register)
        self.session.commit()
    
    def get_all_register(self):
        query = self.session.query(Registers).all()

        registers = [RegisterModel(item).to_dict() for item in query]

        return registers