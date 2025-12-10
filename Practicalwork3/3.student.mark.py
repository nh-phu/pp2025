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
        self.__credits: int = credits

    @property
    def credits(self) -> int:
        return self.__credits

    @credits.setter
    def credits(self, credits: int):
        self.__credits = credits

    def __str__(self):
        return f"Name: {self._name}, ID: {self._id}, Credits: {self.__credits}"


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


class UI:
    def __init__(self, system: System):
        self.system: System = system
        self.stdscr: curses.window
        self.options = [
            ("Add Student", self.add_student),
            ("Add Course", self.add_course),
            ("List Students", self.list_students),
            ("List Courses", self.list_courses),
            ("Input Marks", self.input_marks),
            ("List Marks", self.list_marks),
            ("Sort by GPA", self.sort_by_gpa),
            ("Exit", None),
        ]

    def print_menu(self):
        """Print simple menu"""
        self.stdscr.clear()
        y = 0
        for i, (option, _) in enumerate(self.options):
            self.stdscr.addstr(y, 0, f"{i + 1}. {option}")
            y += 1
        y += 1
        self.stdscr.addstr(y, 0, "Enter option: ")
        self.stdscr.refresh()

    def print_lines(self, lines):
        """Print multiple lines"""
        self.stdscr.clear()
        for idx, line in enumerate(lines):
            try:
                self.stdscr.addstr(idx, 0, line)
            except ValueError:
                pass
        self.stdscr.refresh()
        self.stdscr.getch()

    def get_input(self, prompt):
        """Get text input from user"""
        curses.echo()
        curses.curs_set(1)
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, prompt)
        self.stdscr.refresh()
        input_str = self.stdscr.getstr(1, 0, 60).decode('utf-8')
        curses.noecho()
        curses.curs_set(0)
        return input_str

    def add_student(self):
        """Add a new student"""
        name = self.get_input("Enter student name:")
        if not name:
            return

        id_str = self.get_input("Enter student ID:")
        try:
            student_id = int(id_str)
        except ValueError:
            self.print_lines(["Invalid ID format!", "Press any key..."])
            return

        dob = self.get_input("Enter date of birth (DD/MM/YYYY):")
        if not dob:
            return

        student = Student(name, student_id, dob)
        self.system.add_student(student)
        self.print_lines([f"Student '{name}' added successfully!", "Press any key..."])

    def add_course(self):
        """Add a new course"""
        name = self.get_input("Enter course name:")
        if not name:
            return

        id_str = self.get_input("Enter course ID:")
        try:
            course_id = int(id_str)
        except ValueError:
            self.print_lines(["Invalid ID format!", "Press any key..."])
            return

        credits_str = self.get_input("Enter course credits:")
        try:
            credits = int(credits_str)
        except ValueError:
            self.print_lines(["Invalid credits format!", "Press any key..."])
            return

        course = Course(name, course_id, credits)
        self.system.add_course(course)
        self.print_lines([f"Course '{name}' added successfully!", "Press any key..."])

    def list_students(self):
        """Display all students"""
        if not self.system.students:
            self.print_lines(["No students in the system.", "Press any key..."])
            return

        lines = []
        for student in self.system.students:
            lines.append(str(student))
        lines.append("")
        lines.append("Press any key...")
        self.print_lines(lines)

    def list_courses(self):
        """Display all courses"""
        if not self.system.courses:
            self.print_lines(["No courses in the system.", "Press any key..."])
            return

        lines = []
        for course in self.system.courses:
            lines.append(str(course))
        lines.append("")
        lines.append("Press any key...")
        self.print_lines(lines)

    def input_marks(self):
        """Input marks for a course"""
        if not self.system.courses:
            self.print_lines(["No courses available. Add courses first.", "Press any key..."])
            return

        if not self.system.students:
            self.print_lines(["No students available. Add students first.", "Press any key..."])
            return

        course_id_str = self.get_input("Enter course ID:")
        try:
            course_id = int(course_id_str)
        except ValueError:
            self.print_lines(["Invalid course ID format!", "Press any key..."])
            return

        course = self.system.get_course_by_id(course_id)
        if not course:
            self.print_lines(["Course not found!", "Press any key..."])
            return

        for student in self.system.students:
            mark_str = self.get_input(f"Enter mark for {student.name} (ID: {student.id}) [0-20]:")
            try:
                mark = int(mark_str)
                student.add_mark(course_id, mark)
            except ValueError as e:
                self.print_lines([f"Error: {str(e)}", "Press any key..."])
                continue

        self.print_lines([f"Marks entered for course '{course.name}'", "Press any key..."])

    def list_marks(self):
        """Display marks for a course"""
        if not self.system.courses:
            self.print_lines(["No courses available.", "Press any key..."])
            return

        course_id_str = self.get_input("Enter course ID:")
        try:
            course_id = int(course_id_str)
        except ValueError:
            self.print_lines(["Invalid course ID format!", "Press any key..."])
            return

        course = self.system.get_course_by_id(course_id)
        if not course:
            self.print_lines(["Course not found!", "Press any key..."])
            return

        lines = [f"Marks for course: {course.name}", ""]
        found_any = False
        for student in self.system.students:
            if student.has_mark(course_id):
                mark = student.get_mark(course_id)
                lines.append(f"{student.name} (ID: {student.id}): {mark}")
                found_any = True

        if not found_any:
            lines.append("No marks entered for this course yet.")

        lines.append("")
        lines.append("Press any key...")
        self.print_lines(lines)

    def sort_by_gpa(self):
        """Sort and display students by GPA"""
        if not self.system.students:
            self.print_lines(["No students in the system.", "Press any key..."])
            return

        self.system.sort_by_gpa()

        lines = ["Students sorted by GPA:", ""]
        for student in self.system.students:
            gpa_str = f"{student.gpa:.2f}" if student.gpa is not None else "N/A"
            lines.append(f"{student.name} (ID: {student.id}) - GPA: {gpa_str}")

        lines.append("")
        lines.append("Press any key...")
        self.print_lines(lines)

    def run(self, stdscr: curses.window):
        """Main run loop"""
        self.stdscr = stdscr
        curses.curs_set(0)
        curses.echo()

        while True:
            self.print_menu()

            try:
                choice_str = self.stdscr.getstr(len(self.options) + 1, 15, 10).decode('utf-8')
                choice = int(choice_str)

                if choice < 1 or choice > len(self.options):
                    continue

                if choice == len(self.options):
                    break

                _, func = self.options[choice - 1]
                if func:
                    func()
            except ValueError:
                continue


def main():
    school_system = System()
    ui = UI(school_system)
    curses.wrapper(ui.run)


if __name__ == "__main__":
    main()