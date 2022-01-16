import json
from json import JSONDecodeError


class ReceivedDataSerializer:
    def __init__(self, json_obj):
        self._json = json_obj
        self.errors = None
        self.data = self.__serialize()


    def __serialize(self):
        try:
            json_to_dict = json.loads(self._json)
        except JSONDecodeError:
            self.errors = {"detail": "JSON decode error"}
            return
        return json_to_dict

