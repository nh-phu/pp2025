#!/usr/bin/env python3

import curses
from math import floor

import numpy as np


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

class Course(Object):
    def __init__(self, name: str, id: int, credits: int):
        super().__init__(name, id)
        self.__credits: int= credits

    @property
    def credits(self) -> int:
        return self.__credits

    @credits.setter
    def credits(self, credits: int):
        self.__credits = credits

    def __str__(self):
        return (
            "--------------------------\n"
            + f"Name: {self._name}, ID: {self._id}, Credits: {self.__credits}.\n"
            + "--------------------------"
        )


class Student(Object):
    def __init__(self, name: str, id: int, dob: int):
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
    def dob(self, dob: int):
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

        marks_list: list[int] = []
        credits_list: list[int] = []

        for course in courses:
            if course.id in self.__marks:
                marks_list.append(self.__marks[course.id])
                credits_list.append(course.credits)

        marks_array = np.array(marks_list)
        credits_array = np.array(credits_list)

        self.__gpa = np.average(marks_array, weights=credits_array)

    def __str__(self):
        gpa_str = f", GPA: {self.__gpa:.2f}" if self.__gpa is not None else ""
        return (
            "--------------------------\n"
            + f"Name: {self._name}, ID: {self._id}, DoB: {self.__dob}{gpa_str}.\n"
            + "--------------------------"
        )

class System:
    def __init__(self):
        self.__students: list[Student] = []
        self.__courses: list[Course] = []

    @property
    def students(self):
        return self.__students
    @property
    def courses(self):
        return self.__courses

    def input_students(self):
        num_students = int(input("Enter number of students: "))
        print("--------------------------")
        for student in range(num_students):
            self.students.append(
                Student(
                    input("Enter name of student: "),
                    int(input("Enter ID of student: ")),
                    int(input("Enter DoB of student (DD/MM/YYYY): ")),
                )
            )
            print("--------------------------")


    def input_courses(self):
        num_courses = int(input("Enter number of courses: "))
        print("--------------------------")
        for course in range(num_courses):
            self.courses.append(
                Course(
                    input("Enter name of course: "),
                    int(input("Enter ID of course: ")),
                    int(input("Enter credits for course: ")),
                )
            )
            print("--------------------------")


    def print_students(self):
        print("--------------------------")
        for studetn in self.students:
            print(studetn)
        print("--------------------------")


    def print_course(self):
        print("--------------------------")
        for course in self.courses:
            print(course)
        print("--------------------------")


    def print_marks(self):
        course_id = int(input("Enter course ID to print marks: "))
        print("--------------------------")
        for student in self.students:
            if student.has_mark(course_id):
                print(f"Student: {student.name}, ID: {student.id}, Mark: {student.get_mark(course_id)}")
        print("--------------------------")


    def input_marks(self):
        course_id = int(input("Enter course ID to input marks: "))
        course = None
        for course in self.courses:
            if course.id == course_id:
                course = course
                break
        if course is None:
            print("Course not found.")
            return

        for _student in self.students:
            mark = int(input(f"Enter mark for student {_student.name} (ID: {_student.id}): "))
            _student.add_mark(course_id, mark)


    def sort_by_gpas(self):
        for student in self.students:
            student.calculate_gpa(self.courses)
        self.students.sort(key=lambda x: x.gpa if x.gpa is not None else 0.0, reverse=True)

        print("--------------------------")
        print("Students sorted by GPA (descending):")
        for student in self.students:
            gpa_str = f"{student.gpa}" if student.gpa is not None else "N/A"
            print(f"{student.name} (ID: {student.id}) - GPA: {gpa_str}")
        print("--------------------------")


    def show_help(self):
        print("--------------------------")
        print("Options:")
        print("  - help")
        print("  - list students")
        print("  - list courses")
        print("  - list marks")
        print("  - input marks")
        print("  - sort by gpa")
        print("  - exit or quit")
        print("--------------------------")


def main():
    school_system = System()
    school_system.input_students()
    school_system.input_courses()
    while 1:
        option = input("Enter action: ")
        match option:
            case "help":
                school_system.show_help()
            case "list students":
                school_system.print_students()
            case "list courses":
                school_system.print_course()
            case "list marks":
                school_system.print_marks()
            case "input marks":
                school_system.input_marks()
            case "sort by gpa":
                school_system.sort_by_gpas()
            case "exit" | "quit":
                break
            case _:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
