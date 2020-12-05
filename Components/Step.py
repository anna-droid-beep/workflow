import json

class Step:
    def __init__(self, status_name, index=None):
        self._status = status_name
        self._index = index

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status_name):
        self._status = status_name

    def __str__(self):
        return json.dumps(self, default=lambda x: x.__dict__)

