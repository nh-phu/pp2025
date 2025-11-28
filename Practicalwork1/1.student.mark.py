#!/usr/bin/env python3

students = []
courses = []

def input_students():
    num_students = int(input("Enter number of students: "))
    for _ in range(num_students):
        students.append({
            "name": input(f"Enter name of student: "),
            "id": input(f"Enter ID of student: "),
            "dob": input(f"Enter DoB of student (DD/MM/YYYY): "),
    })

def input_courses():
    num_courses = int(input("Enter number of courses: "))
    for _ in range(num_courses):
        courses.append({
            "name": input(f"Enter name of course: "),
            "id": input(f"Enter ID of course: ")
        })

def print_students():
    print("--------------------------")
    for studetn in students:
        print(f"Name: {studetn['name']}, ID: {studetn['id']}, DoB: {studetn['dob']}")
    print("--------------------------")

def print_course():
    print("--------------------------")
    for course in courses:
        print(f"Name: {course['name']}, ID: {course['id']}")
    print("--------------------------")

def print_marks():
    course_id = input("Enter course ID to print marks: ")
    print("--------------------------")
    for student in students:
        if "marks" in student and course_id in student["marks"]:
            print(f"Student: {student['name']}, ID: {student['id']}, Mark: {student['marks'][course_id]}")
    print("--------------------------")

def input_marks():
    course_id = input("Enter course ID to input marks: ")
    course = None
    for c in courses:
        if c['id'] == course_id:
            course = c
            break
    if course == None:
        print("Course not found.")
        return

    for student in students:
        mark = input(f"Enter mark for student {student['name']} (ID: {student['id']}): ")
        if "marks" not in student:
            student["marks"] = {}
        student["marks"][course_id] = mark

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
    while (1):
        mode = input("Enter action: ")
        if mode == 'help':
            show_help()
        elif mode == 'list students':
            print_students()
        elif mode == 'list courses':
            print_course()
        elif mode == 'list marks':
            print_marks()
        elif mode == 'input marks':
            input_marks()
        elif mode == 'exit' or mode == 'quit':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
