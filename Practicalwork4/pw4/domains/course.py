from .object import Object

class Course(Object):
    def __init__(self, name: str, id: int, credits: int):
        super().__init__(name, id)
        self.__credits: int = credits

    @property
    def credits(self) -> int:
        return self.__credits

    @credits.setter
    def credits(self, credits: int):
        self.__credits = credits

    def __str__(self):
        return f"Name: {self._name}, ID: {self._id}, Credits: {self.__credits}"
