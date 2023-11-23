import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.models.registerModel import RegisterModel
import random
from datetime import datetime, timedelta
import json

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
        engine = create_engine('mysql+mysqlconnector://root:123456@db:3306/pdi_transport', echo=True)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

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
    
    def seed_registers(self, num_entries=10):
        categories = ['Carro', 'Moto', 'Bicicleta']
        for _ in range(num_entries):
            start_time = datetime.now() - timedelta(days=random.randint(0, 365))
            end_time = start_time + timedelta(hours=random.randint(1, 12))
            
            new_register = Registers(
                token=''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8)),
                category=random.choice(categories),
                points=json.dumps({"x": random.randint(0, 100), "y": random.randint(0, 100)}),
                infractions=json.dumps([random.choice(['Speeding', 'Red Light', 'Stop Sign']) for _ in range(random.randint(0, 5))]),
                average_speed=random.uniform(20.0, 120.0),
                has_helmet=random.choice([True, False]),
                license_plate=''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=7)),
                start_time=start_time,
                end_time=end_time
            )

            self.session.add(new_register)
        self.session.commit()

