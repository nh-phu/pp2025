class OutputHandler:
    def __init__(self, ui):
        self.ui = ui
    
    def print_menu(self):
        """Print simple menu"""
        self.ui.stdscr.clear()
        y = 0
        for i, (option, _) in enumerate(self.ui.options):
            self.ui.stdscr.addstr(y, 0, f"{i + 1}. {option}")
            y += 1
        y += 1
        self.ui.stdscr.addstr(y, 0, "Enter option: ")
        self.ui.stdscr.refresh()

    def print_lines(self, lines):
        """Print multiple lines"""
        self.ui.stdscr.clear()
        for idx, line in enumerate(lines):
            try:
                self.ui.stdscr.addstr(idx, 0, line)
            except ValueError:
                pass
        self.ui.stdscr.refresh()
        self.ui.stdscr.getch()

    def list_students(self):
        """Display all students"""
        if not self.ui.system.students:
            self.print_lines(["No students in the system.", "Press any key..."])
            return

        lines = []
        for student in self.ui.system.students:
            lines.append(str(student))
        lines.append("")
        lines.append("Press any key...")
        self.print_lines(lines)

    def list_courses(self):
        """Display all courses"""
        if not self.ui.system.courses:
            self.print_lines(["No courses in the system.", "Press any key..."])
            return

        lines = []
        for course in self.ui.system.courses:
            lines.append(str(course))
        lines.append("")
        lines.append("Press any key...")
        self.print_lines(lines)

    def list_marks(self):
        """Display marks for a course"""
        if not self.ui.system.courses:
            self.print_lines(["No courses available.", "Press any key..."])
            return

        course_id_str = self.ui.input.get_input("Enter course ID:")
        try:
            course_id = int(course_id_str)
        except ValueError:
            self.print_lines(["Invalid course ID format!", "Press any key..."])
            return

        course = self.ui.system.get_course_by_id(course_id)
        if not course:
            self.print_lines(["Course not found!", "Press any key..."])
            return

        lines = [f"Marks for course: {course.name}", ""]
        found_any = False
        for student in self.ui.system.students:
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
        if not self.ui.system.students:
            self.print_lines(["No students in the system.", "Press any key..."])
            return

        self.ui.system.sort_by_gpa()

        lines = ["Students sorted by GPA:", ""]
        for student in self.ui.system.students:
            gpa_str = f"{student.gpa:.2f}" if student.gpa is not None else "N/A"
            lines.append(f"{student.name} (ID: {student.id}) - GPA: {gpa_str}")

        lines.append("")
        lines.append("Press any key...")
        self.print_lines(lines)