class Object:
    def __init__(self, name: str, id: int):
        self._name: str = name
        self._id: int = id

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @name.setter
    def name(self, value: str):
        self._name = value

    @id.setter
    def id(self, id: int):
        self._id = id