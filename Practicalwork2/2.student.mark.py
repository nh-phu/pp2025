#!/usr/bin/env python3


class obj:
    def __init__(self, name: str, id: int):
        self._name: str = name
        self._id: int = id

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id


class student(obj):
    def __init__(self, name: str, id: int, dob: int):
        super().__init__(name, id)
        self.__dob = dob
        self.__marks: dict[int, int] = {}

    @property
    def dob(self):
        return self.__dob

    @property
    def marks(self):
        return self.__marks

    def add_mark(self, course_id: int, mark: int):
        if (0 > mark or mark > 20):
            raise ValueError("Mark must be between 0 and 20.")
        self.__marks[course_id] = mark

    def get_mark(self, course_id: int):
        return self.__marks.get(course_id, None)

    def has_mark(self, course_id: int):
        return course_id in self.__marks

    def __str__(self):
        return (
            "--------------------------\n"
            + f"Name: {self._name}, ID: {self._id}, DoB: {self.__dob}.\n"
            + "--------------------------"
        )


class course(obj):
    def __str__(self):
        return (
            "--------------------------\n"
            + f"Name: {self._name}, ID: {self._id}.\n"
            + "--------------------------"
        )


students: list[student] = []
courses: list[course] = []


def input_students():
    num_students = int(input("Enter number of students: "))
    print("--------------------------")
    for _ in range(num_students):
        students.append(
            student(
                input("Enter name of student: "),
                int(input("Enter ID of student: ")),
                int(input("Enter DoB of student (DD/MM/YYYY): ")),
            )
        )
        print("--------------------------")


def input_courses():
    num_courses = int(input("Enter number of courses: "))
    print("--------------------------")
    for _ in range(num_courses):
        courses.append(
            course(
                input("Enter name of course: "),
                int(input("Enter ID of course: ")),
            )
        )
        print("--------------------------")


def print_students():
    print("--------------------------")
    for studetn in students:
        print(studetn)
    print("--------------------------")


def print_course():
    print("--------------------------")
    for course in courses:
        print(course)
    print("--------------------------")


def print_marks():
    course_id = int(input("Enter course ID to print marks: "))
    print("--------------------------")
    for stu in students:
        if stu.has_mark(course_id):
            print(f"Student: {stu.name}, ID: {stu.id}, Mark: {stu.get_mark}")
    print("--------------------------")


def input_marks():
    course_id = int(input("Enter course ID to input marks: "))
    course = None
    for c in courses:
        if c.id == course_id:
            course = c
            break
    if course is None:
        print("Course not found.")
        return

    for student in students:
        mark = int(input(f"Enter mark for student {student.name} (ID: {student.id}): "))
        student.add_mark(course_id, mark)


def show_help():
    print("--------------------------")
    print("Options:")
    print("  - help")
    print("  - list students")
    print("  - list courses")
    print("  - list marks")
    print("  - input marks")
    print("  - exit or quit")
    print("--------------------------")


def main():
    input_students()
    input_courses()
    while 1:
        mode = input("Enter action: ")
        if mode == "help":
            show_help()
        elif mode == "list students":
            print_students()
        elif mode == "list courses":
            print_course()
        elif mode == "list marks":
            print_marks()
        elif mode == "input marks":
            input_marks()
        elif mode == "exit" or mode == "quit":
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
