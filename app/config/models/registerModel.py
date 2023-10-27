import json

class RegisterModel:
    def __init__(self, object_instance):
        self.token = object_instance.token
        self.category = object_instance.category
        self.points = object_instance.points
        self.infractions = object_instance.infractions
        self.average_speed = object_instance.average_speed
        self.has_helmet = object_instance.has_helmet
        self.license_plate = object_instance.license_plate
        self.start_time = object_instance.start_time
        self.end_time = object_instance.end_time

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return self.__dict__