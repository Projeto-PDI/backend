from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.models.registroModel import RegistroModel
from app.config.models.trajetoriaModel import TrajetoriaModel
from app.config.models.veiculoModel import VeiculoModel
from app.config.models.capateceteModel import CapaceteModel
import uuid

Base = declarative_base()


class Registros(Base):
    __tablename__ = "registros"

    token = Column(String(255), primary_key=True)
    nome = Column(String(255))


class Veiculos(Base):
    __tablename__ = "veiculos"

    token = Column(String(255), primary_key=True)
    velocidade = Column(Float)
    tipo = Column(String(255))
    start_time = Column(DateTime)
    end_time = Column(DateTime)


class Trajetorias(Base):
    __tablename__ = "trajetorias"

    token = Column(String(255), primary_key=True)
    veiculo_token = Column(String(255))
    x = Column(Float)
    y = Column(Float)


class Capacetes(Base):
    __tablename__ = "capacetes"

    token = Column(String(255), primary_key=True)
    registro_token = Column(String(255))
    total_com_capacete = Column(Float)
    total_sem_capacete = Column(Float)


class DatabaseBuilder:
    def __init__(self):
        engine = create_engine(
            "mysql+mysqlconnector://root:123456@db:3306/pdi_transport", echo=True
        )
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_trajectories(self, data):
        registro_token = uuid.uuid4()

        registro_db = Registros(token=registro_token, nome=data["nome"])

        veiculos_db = []
        trajetorias_db = []
        for veiculo in data["veiculos"]:
            veiculo_token = uuid.uuid4()

            veiculo_db = Veiculos(
                token=veiculo_token,
                velocidade=veiculo["velocidade"],
                tipo=veiculo["tipo"],
                start_time=veiculo["start_time"],
                end_time=veiculo["end_time"],
            )

            veiculos_db.append(veiculo_db)

            for trajetoria in veiculo["trajetorias"]:
                trajetoria_token = uuid.uuid4()

                trajetoria_db = Trajetorias(
                    token=trajetoria_token,
                    veiculo_token=veiculo_token,
                    x=trajetoria["x"],
                    y=trajetoria["y"],
                )

                trajetorias_db.append(trajetoria_db)

        self.session.add(registro_db)

        for veiculo in veiculos_db:
            self.session.add(veiculo)

        for trajetoria in trajetorias_db:
            self.session.add(trajetoria)

        self.session.commit()

    def create_helmet(self, data):
        registro_token = uuid.uuid4()

        registro_db = Registros(token=registro_token, nome=data["nome"])

        capacetes_db = []
        for capacetes in data["capacetes"]:
            capacete_token = uuid.uuid4()

            capacete_db = capacetes(
                token=capacete_token,
                registro_token=data["registro_token"],
                total_com_capacete=data["total_com_capacete"],
                total_sem_capacete=data["total_sem_capacete"],
            )

            capacetes_db.append(capacete_db)

        self.session.add(registro_db)

        for capacete in capacetes_db:
            self.session.add(capacete)

        self.session.commit()

    def get_trajectories(self, video_name):
        registro_query = (
            self.session.query(Registros).filter_by(nome=video_name).first()
        )

        if registro_query:
            registro_data = RegistroModel(registro_query).to_dict()

            veiculos_query = (
                self.session.query(Veiculos)
                .filter_by(token=registro_data["token"])
                .all()
            )
            veiculos_data = []

            for veiculo in veiculos_query:
                veiculo_dict = VeiculoModel(veiculo).to_dict()

                trajetorias_query = (
                    self.session.query(Trajetorias)
                    .filter_by(veiculo_token=veiculo_dict["token"])
                    .all()
                )
                trajetorias_data = [
                    TrajetoriaModel(trajetoria).to_dict()
                    for trajetoria in trajetorias_query
                ]

                veiculo_dict["trajetorias"] = trajetorias_data
                veiculos_data.append(veiculo_dict)

            registro_data["veiculos"] = veiculos_data

            return registro_data
        else:
            return None

    def get_helmet(self, video_name):
        registro_query = (
            self.session.query(Registros).filter_by(nome=video_name).first()
        )

        if registro_query:
            registro_data = RegistroModel(registro_query).to_dict()

            capacetes_query = (
                self.session.query(Capacetes)
                .filter_by(registro_token=registro_data["token"])
                .all()
            )
            capacetes_data = [
                CapaceteModel(capacete).to_dict() for capacete in capacetes_query
            ]

            registro_data["capacetes"] = capacetes_data

            return registro_data
        else:
            return None
