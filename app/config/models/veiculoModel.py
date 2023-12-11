import json


class VeiculoModel:
    def __init__(self, object_instance):
        self.token = object_instance.token
        self.registro_token = object_instance.registro_token
        self.initial_date = object_instance.initial_date
        self.end_date = object_instance.end_date
        self.tipo = object_instance.tipo

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return self.__dict__
