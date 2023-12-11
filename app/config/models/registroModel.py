import json


class RegistroModel:
    def __init__(self, object_instance):
        self.token = object_instance.token
        self.nome = object_instance.nome

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return self.__dict__
