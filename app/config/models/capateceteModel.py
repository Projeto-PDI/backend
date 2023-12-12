import json


class CapaceteModel:
    def __init__(self, object_instance):
        self.token = object_instance.token
        self.registro_token = object_instance.registro_token
        self.total_com_capacete = object_instance.total_com_capacete
        self.total_sem_capacete = object_instance.total_sem_capacete

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return self.__dict__
