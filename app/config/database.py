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
            "mysql+mysqlconnector://root:123456@localhost:3306/pdi_transport", echo=True
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

        print("Criou token")
        print(data)
        capacete_db = Capacetes(
            token=capacete_token,
            registro_token=registro_token,
            total_com_capacete=data["total_com_capacete"],
            total_sem_capacete=data["total_sem_capacete"],
        )
        print("Criou Capacete")

        self.session.add(capacete_db)

        self.session.commit()

    def get_all_registers(self):
        registros = self.session.query(Registros).all()
        result = []
        for registro in registros:
            result.append({"id": registro.token, "name": registro.nome})
        return result

    def get_registro_by_token(self, token):
        registro = (
            self.session.query(Registros)
            .filter(Registros.token == token)
            .first()
        )
        if not registro:
            return None

        veiculos = (
            self.session.query(Veiculos)
            .filter_by(registro_token=token)
            .all()
        )

        veiculos_data = []
        for veiculo in veiculos:
            trajetorias = (
                self.session.query(Trajetorias)
                .filter(Trajetorias.veiculo_token == veiculo.token)
                .all()
            )
            veiculo_data = {
                "id": veiculo.token,
                "velocity": veiculo.velocidade,
                "type": veiculo.tipo,
                "start_time": veiculo.start_time,
                "end_time": veiculo.end_time,
                "trajectories": [
                    {"x": trajetoria.x, "y": trajetoria.y}
                    for trajetoria in trajetorias
                ],
            }
            veiculos_data.append(veiculo_data)

        capacete = (
            self.session.query(Capacetes)
            .filter(Capacetes.registro_token == token)
            .first()
        )

        capacete_data = {}
        if not capacete: 
            capacete_data = {
                "total_com_capacete": 0,
                "total_sem_capacete": 0,
            }
        else:
            capacete_data = {
                "total_com_capacete": capacete.total_com_capacete,
                "total_sem_capacete": capacete.total_sem_capacete,
            }

        result = {
            "id": registro.token,
            "name": registro.nome,
            "veiculos": veiculos_data,
            "capacete": capacete_data,
        }

        return result
