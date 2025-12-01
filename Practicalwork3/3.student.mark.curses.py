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

    def calculate_gpa(self, courses: list['Course']):
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

    def __str__(self):
        gpa_str = f", GPA: {self.__gpa:.2f}" if self.__gpa is not None else ""
        return f"Name: {self._name}, ID: {self._id}, DoB: {self.__dob}{gpa_str}"


class CursesUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)

    def draw_border(self, win, title=""):
        win.box()
        if title:
            win.addstr(0, 2, f" {title} ", curses.color_pair(3) | curses.A_BOLD)

    def draw_header(self):
        header = "╔══════════════════════════════════════════════════════════════╗"
        title =  "║         STUDENT MANAGEMENT SYSTEM - CURSES UI                ║"
        footer = "╚══════════════════════════════════════════════════════════════╝"
        
        # Center the header
        header_width = len(header)
        start_x = (self.width - header_width) // 2

        self.stdscr.addstr(0, start_x, header, curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(1, start_x, title, curses.color_pair(2) | curses.A_BOLD)
        self.stdscr.addstr(2, start_x, footer, curses.color_pair(2) | curses.A_BOLD)

    def show_menu(self, options, selected_idx, title="Menu"):
        menu_height = len(options) + 4
        menu_width = 50
        menu_start_y = 4
        start_x = (self.width - menu_width) // 2

        # Draw border around menu first
        for i in range(menu_height):
            y = menu_start_y + i
            if i == 0 or i == menu_height - 1:
                self.stdscr.addstr(y, start_x, "+" + "-" * (menu_width - 2) + "+", curses.color_pair(2))
            else:
                self.stdscr.addstr(y, start_x, "|", curses.color_pair(2))
                self.stdscr.addstr(y, start_x + menu_width - 1, "|", curses.color_pair(2))

        if title:
            self.stdscr.addstr(menu_start_y, start_x + 2, f" {title} ", curses.color_pair(3) | curses.A_BOLD)

        # Draw menu options
        for idx, option in enumerate(options):
            y = menu_start_y + idx + 2
            if idx == selected_idx:
                self.stdscr.addstr(y, start_x + 2, f"> {option}".ljust(menu_width - 4), curses.color_pair(1) | curses.A_BOLD)
            else:
                self.stdscr.addstr(y, start_x + 2, f"  {option}".ljust(menu_width - 4), curses.color_pair(4))

        self.stdscr.refresh()

    def get_input(self, prompt, y_pos=None):
        if y_pos is None:
            y_pos = self.height - 3

        curses.curs_set(1)
        self.stdscr.addstr(y_pos, 2, " " * (self.width - 4))
        self.stdscr.addstr(y_pos, 2, prompt, curses.color_pair(3))
        self.stdscr.refresh()

        curses.echo()
        input_str = self.stdscr.getstr(y_pos, 2 + len(prompt), 50).decode('utf-8')
        curses.noecho()
        curses.curs_set(0)

        return input_str

    def show_message(self, message, color_pair=4):
        msg_win = curses.newwin(5, 60, self.height // 2 - 2, (self.width - 60) // 2)
        msg_win.clear()
        self.draw_border(msg_win, "Message")
        msg_win.addstr(2, 2, message[:56], curses.color_pair(color_pair))
        msg_win.addstr(3, 2, "Press any key to continue...", curses.color_pair(2))
        msg_win.refresh()
        msg_win.getch()

    def display_list(self, items, title):
        list_win = curses.newwin(self.height - 6, self.width - 4, 4, 2)
        list_win.clear()
        self.draw_border(list_win, title)

        y = 2
        for idx, item in enumerate(items):
            if y < self.height - 8:
                list_win.addstr(y, 2, f"{idx + 1}. {str(item)[:self.width - 10]}", curses.color_pair(4))
                y += 1

        list_win.addstr(y + 1, 2, "Press any key to continue...", curses.color_pair(2))
        list_win.refresh()
        list_win.getch()


class System:
    def __init__(self, ui):
        self.__students: list[Student] = []
        self.__courses: list[Course] = []
        self.ui = ui

    @property
    def students(self):
        return self.__students

    @property
    def courses(self):
        return self.__courses

    def input_students(self):
        try:
            num = self.ui.get_input("Enter number of students: ")
            num_students = int(num)

            for i in range(num_students):
                self.ui.stdscr.clear()
                self.ui.draw_header()
                self.ui.stdscr.addstr(4, 2, f"Student {i + 1}/{num_students}", curses.color_pair(3) | curses.A_BOLD)

                name = self.ui.get_input("Name: ", 6)
                id_str = self.ui.get_input("ID: ", 7)
                dob_str = self.ui.get_input("DoB (DDMMYYYY): ", 8)

                self.students.append(Student(name, int(id_str), int(dob_str)))

            self.ui.show_message(f"Successfully added {num_students} students!", 4)
        except Exception as e:
            self.ui.show_message(f"Error: {str(e)}", 5)

    def input_courses(self):
        try:
            num = self.ui.get_input("Enter number of courses: ")
            num_courses = int(num)

            for i in range(num_courses):
                self.ui.stdscr.clear()
                self.ui.draw_header()
                self.ui.stdscr.addstr(4, 2, f"Course {i + 1}/{num_courses}", curses.color_pair(3) | curses.A_BOLD)

                name = self.ui.get_input("Name: ", 6)
                id_str = self.ui.get_input("ID: ", 7)
                credits_str = self.ui.get_input("Credits: ", 8)

                self.courses.append(Course(name, int(id_str), int(credits_str)))

            self.ui.show_message(f"Successfully added {num_courses} courses!", 4)
        except Exception as e:
            self.ui.show_message(f"Error: {str(e)}", 5)

    def print_students(self):
        if not self.students:
            self.ui.show_message("No students to display!", 5)
            return
        self.ui.display_list(self.students, "Students List")

    def print_courses(self):
        if not self.courses:
            self.ui.show_message("No courses to display!", 5)
            return
        self.ui.display_list(self.courses, "Courses List")

    def print_marks(self):
        if not self.students:
            self.ui.show_message("No students available!", 5)
            return

        try:
            course_id_str = self.ui.get_input("Enter course ID: ")
            course_id = int(course_id_str)

            marks_list = []
            for student in self.students:
                if student.has_mark(course_id):
                    mark = student.get_mark(course_id)
                    marks_list.append(f"{student.name} (ID: {student.id}) - Mark: {mark}")

            if marks_list:
                self.ui.display_list(marks_list, f"Marks for Course {course_id}")
            else:
                self.ui.show_message("No marks found for this course!", 5)
        except Exception as e:
            self.ui.show_message(f"Error: {str(e)}", 5)

    def input_marks(self):
        if not self.courses or not self.students:
            self.ui.show_message("Need courses and students first!", 5)
            return

        try:
            course_id_str = self.ui.get_input("Enter course ID: ")
            course_id = int(course_id_str)

            course_obj = None
            for course in self.courses:
                if course.id == course_id:
                    course_obj = course
                    break

            if course_obj is None:
                self.ui.show_message("Course not found!", 5)
                return

            for idx, student in enumerate(self.students):
                self.ui.stdscr.clear()
                self.ui.draw_header()
                self.ui.stdscr.addstr(4, 2, f"Entering marks for: {course_obj.name}", curses.color_pair(3) | curses.A_BOLD)
                self.ui.stdscr.addstr(5, 2, f"Student {idx + 1}/{len(self.students)}: {student.name}", curses.color_pair(4))

                mark_str = self.ui.get_input("Mark (0-20): ", 7)
                student.add_mark(course_id, int(mark_str))

            self.ui.show_message("Marks entered successfully!", 4)
        except Exception as e:
            self.ui.show_message(f"Error: {str(e)}", 5)

    def sort_by_gpas(self):
        if not self.students:
            self.ui.show_message("No students to sort!", 5)
            return

        for student in self.students:
            student.calculate_gpa(self.courses)

        self.students.sort(key=lambda x: x.gpa if x.gpa is not None else 0.0, reverse=True)

        sorted_list = []
        for student in self.students:
            gpa_str = f"{student.gpa:.2f}" if student.gpa is not None else "N/A"
            sorted_list.append(f"{student.name} (ID: {student.id}) - GPA: {gpa_str}")

        self.ui.display_list(sorted_list, "Students Sorted by GPA (Descending)")


def main(stdscr):
    ui = CursesUI(stdscr)
    system = System(ui)

    menu_options = [
        "Input Students",
        "Input Courses",
        "List Students",
        "List Courses",
        "Input Marks",
        "List Marks",
        "Sort by GPA",
        "Exit"
    ]

    selected = 0

    while True:
        stdscr.clear()
        ui.draw_header()

        # Draw footer
        stdscr.addstr(ui.height - 2, 2, "Use ↑/↓ arrows to navigate, ENTER to select, Q to quit", curses.color_pair(2))

        ui.show_menu(menu_options, selected, "Main Menu")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(menu_options) - 1:
            selected += 1
        elif key == ord('\n') or key == ord(' '):
            stdscr.clear()
            ui.draw_header()
            stdscr.refresh()

            match selected:
                case 0:
                    system.input_students()
                case 1:
                    system.input_courses()
                case 2:
                    system.print_students()
                case 3:
                    system.print_courses()
                case 4:
                    system.input_marks()
                case 5:
                    system.print_marks()
                case 6:
                    system.sort_by_gpas()
                case 7:
                    break
        elif key == ord('q') or key == ord('Q'):
            break


if __name__ == "__main__":
    curses.wrapper(main)