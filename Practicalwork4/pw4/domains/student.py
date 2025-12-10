from math import floor
import numpy as np
from .object import Object
from .course import Course

class Student(Object):
    def __init__(self, name: str, id: int, dob: str):
        super().__init__(name, id)
        self.__dob = dob
        self.__marks: dict[int, int] = {}
        self.__gpa = None

    @property
    def dob(self):
        return self.__dob

    @property
    def marks(self):
        return self.__marks

    @property
    def gpa(self):
        return self.__gpa

    @dob.setter
    def dob(self, dob: str):
        self.__dob = dob

    def add_mark(self, course_id: int, mark: int):
        if 0 > mark or mark > 20:
            raise ValueError("Mark must be between 0 and 20.")
        self.__marks[course_id] = floor(mark)
        self.__gpa = None

    def get_mark(self, course_id: int):
        return self.__marks.get(course_id, None)

    def has_mark(self, course_id: int):
        return course_id in self.__marks

    def calculate_gpa(self, courses: list[Course]):
        if not self.__marks:
            self.__gpa = 0.0
            return

        marks_list: list[int] = []
        credits_list: list[int] = []

        for course in courses:
            if course.id in self.__marks:
                marks_list.append(self.__marks[course.id])
                credits_list.append(course.credits)

        if marks_list:
            marks_array = np.array(marks_list)
            credits_array = np.array(credits_list)
            self.__gpa = np.average(marks_array, weights=credits_array)
        else:
            self.__gpa = 0.0

    def __str__(self):
        gpa_str = f", GPA: {self.__gpa:.2f}" if self.__gpa is not None else ""
        return f"Name: {self._name}, ID: {self._id}, DoB: {self.__dob}{gpa_str}"
