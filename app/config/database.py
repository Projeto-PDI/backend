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
    registro_token = Column(String(255))
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

    def create_trajectories(self, data, name):
        registro_token = str(uuid.uuid4())

        registro_db = Registros(token=registro_token, nome=name)

        veiculos_db = []
        trajetorias_db = []
        for veiculo in data:
            veiculo_token = str(uuid.uuid4())

            veiculo_db = Veiculos(
                token=veiculo_token,
                registro_token=registro_token,
                velocidade=veiculo["velocidade"],
                tipo=veiculo["tipo"],
                start_time=veiculo["start_time"],
                end_time=veiculo["end_time"],
            )

            veiculos_db.append(veiculo_db)

            for trajetoria in veiculo["trajetorias"]:
                trajetoria_token = str(uuid.uuid4())

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

        return registro_token

    def create_helmet(self, data, registro_token):
        capacete_token = str(uuid.uuid4())

        capacete_db = Capacetes(
            token=capacete_token,
            registro_token=registro_token,
            total_com_capacete=data["total_com_capacete"],
            total_sem_capacete=data["total_sem_capacete"],
        )

        self.session.add(capacete_db)

        self.session.commit()

    def get_register(self, name):
        registro_query = self.session.query(Registros).filter_by(nome=name).first()

        if registro_query:
            registro_data = RegistroModel(registro_query).to_dict()

            veiculos_query = (
                self.session.query(Veiculos)
                .filter_by(registro_token=registro_data["token"])
                .all()
            )

            veiculos = [VeiculoModel(vei).to_dict() for vei in veiculos_query]

            result = {
                "registro_token": registro_data["token"],
                "nome_registro": registro_data["nome"],
                "veiculos": [],
                "capacetes": [],
            }

            for veiculo in veiculos:
                trajetorias_query = (
                    self.session.query(Trajetorias)
                    .filter_by(veiculo_token=veiculo["token"])
                    .all()
                )

                trajetorias_data = [
                    TrajetoriaModel(traj).to_dict() for traj in trajetorias_query
                ]

                veiculo_result = {
                    "veiculo": veiculo,
                    "trajetorias": trajetorias_data,
                }

                result["veiculos"].append(veiculo_result)

            capacetes_query = (
                self.session.query(Capacetes)
                .filter_by(registro_token=registro_data["token"])
                .all()
            )

            capacetes_data = [
                CapaceteModel(capacete).to_dict() for capacete in capacetes_query
            ]

            result["capacetes"] = capacetes_data

            return result
        else:
            return None
