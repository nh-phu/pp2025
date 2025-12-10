import curses
from domains.student import Student
from domains.course import Course


class InputHandler:
    def __init__(self, ui):
        self.ui = ui
    
    def get_input(self, prompt):
        """Get text input from user"""
        curses.echo()
        curses.curs_set(1)
        self.ui.stdscr.clear()
        self.ui.stdscr.addstr(0, 0, prompt)
        self.ui.stdscr.refresh()
        input_str = self.ui.stdscr.getstr(1, 0, 60).decode('utf-8')
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
            self.ui.output.print_lines(["Invalid ID format!", "Press any key..."])
            return

        dob = self.get_input("Enter date of birth (DD/MM/YYYY):")
        if not dob:
            return

        student = Student(name, student_id, dob)
        self.ui.system.add_student(student)
        self.ui.output.print_lines([f"Student '{name}' added successfully!", "Press any key..."])
    
    def add_course(self):
        """Add a new course"""
        name = self.get_input("Enter course name:")
        if not name:
            return

        id_str = self.get_input("Enter course ID:")
        try:
            course_id = int(id_str)
        except ValueError:
            self.ui.output.print_lines(["Invalid ID format!", "Press any key..."])
            return

        credits_str = self.get_input("Enter course credits:")
        try:
            credits = int(credits_str)
        except ValueError:
            self.ui.output.print_lines(["Invalid credits format!", "Press any key..."])
            return

        course = Course(name, course_id, credits)
        self.ui.system.add_course(course)
        self.ui.output.print_lines([f"Course '{name}' added successfully!", "Press any key..."])
    
    def input_marks(self):
        """Input marks for a course"""
        if not self.ui.system.courses:
            self.ui.output.print_lines(["No courses available. Add courses first.", "Press any key..."])
            return

        if not self.ui.system.students:
            self.ui.output.print_lines(["No students available. Add students first.", "Press any key..."])
            return

        course_id_str = self.get_input("Enter course ID:")
        try:
            course_id = int(course_id_str)
        except ValueError:
            self.ui.output.print_lines(["Invalid course ID format!", "Press any key..."])
            return

        course = self.ui.system.get_course_by_id(course_id)
        if not course:
            self.ui.output.print_lines(["Course not found!", "Press any key..."])
            return

        for student in self.ui.system.students:
            mark_str = self.get_input(f"Enter mark for {student.name} (ID: {student.id}) [0-20]:")
            try:
                mark = int(mark_str)
                student.add_mark(course_id, mark)
            except ValueError as e:
                self.ui.output.print_lines([f"Error: {str(e)}", "Press any key..."])
                continue

        self.ui.output.print_lines([f"Marks entered for course '{course.name}'", "Press any key..."])