import json


class TrajetoriaModel:
    def __init__(self, object_instance):
        self.token = object_instance.token
        self.veiculo_token = object_instance.veiculo_token
        self.x = object_instance.x
        self.y = object_instance.y

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return self.__dict__
