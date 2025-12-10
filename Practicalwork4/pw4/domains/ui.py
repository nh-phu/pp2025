import curses
from domains.system import System
from input import InputHandler
from output import OutputHandler


class UI:
    def __init__(self, system: System):
        self.system = system
        self.stdscr = None
        self.input = InputHandler(self)
        self.output = OutputHandler(self)
        self.options = [
            ("Add Student", self.input.add_student),
            ("Add Course", self.input.add_course),
            ("List Students", self.output.list_students),
            ("List Courses", self.output.list_courses),
            ("Input Marks", self.input.input_marks),
            ("List Marks", self.output.list_marks),
            ("Sort by GPA", self.output.sort_by_gpa),
            ("Exit", None),
        ]

    def run(self, stdscr: curses.window):
        """Main run loop"""
        self.stdscr = stdscr
        curses.curs_set(0)
        curses.echo()

        while True:
            self.output.print_menu()

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