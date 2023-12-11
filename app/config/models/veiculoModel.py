import json


class VeiculoModel:
    def __init__(self, object_instance):
        self.token = object_instance.token
        self.registro_token = object_instance.registro_token
        self.start_time = object_instance.start_time
        self.end_time = object_instance.end_time
        self.tipo = object_instance.tipo
        self.velocidade = object_instance.velocidade

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return self.__dict__
