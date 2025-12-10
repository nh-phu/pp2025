from .student import Student
from .course import Course

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

    def add_student(self, student: Student):
        self.__students.append(student)

    def add_course(self, course: Course):
        self.__courses.append(course)

    def get_course_by_id(self, course_id: int):
        for course in self.__courses:
            if course.id == course_id:
                return course
        return None

    def sort_by_gpa(self):
        for student in self.students:
            student.calculate_gpa(self.courses)
        self.students.sort(
            key=lambda x: x.gpa if x.gpa is not None else 0.0, reverse=True
        )
