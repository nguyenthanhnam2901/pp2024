import curses
from datetime import datetime
import math
import numpy as np

class Student:
    def __init__(self, id, name, dob):
        self.__id = id
        self.__name = name
        self.__dob = dob

    def show_student_id(self):
        return self.__id
    
    def show_student_name(self):
        return self.__name
    
    def show_dob(self):
        return self.__dob

class StudentArray:
    def __init__(self):
        self.__info = []
        
    def show_student_info(self):
        return self.__info

class Course:
    def __init__(self, id, name, credit):
        self.__id = id
        self.__name = name
        self.__credit = credit

    def show_course_id(self):
        return self.__id
    
    def show_course_name(self):
        return self.__name

    def show_credit(self):
        return self.__credit   

class CourseArray:
    def __init__(self):
        self.__info = []
        
    def show_course_info(self):
        return self.__info

class Mark:
    def __init__(self, student_id, course_id, mark):
        self.__student_id = student_id
        self.__course_id = course_id
        self.__mark = mark

    def show_mark_student_id(self):
        return self.__student_id
    
    def show_mark_course_id(self):
        return self.__course_id
    
    def show_mark(self):
        return self.__mark
    
def loop_positive_integer(stdscr, prompt):
    curses.echo()
    while True:
        stdscr.addstr(prompt)
        stdscr.refresh()
        try:
            number = int(stdscr.getstr().decode())
            if number >= 0:
                curses.noecho()
                return number
            else:
                stdscr.addstr("Invalid value. Please enter a non-negative number.\n")
        except ValueError:
            stdscr.addstr("Error: value must be an integer. Please try again.\n")

def add_items(stdscr, args, cls, info_array):
    stdscr.clear()
    stdscr.addstr(f"Enter the number of {args} you want to add: ")
    stdscr.refresh()
    number_of_variables = loop_positive_integer(stdscr, "")

    items = []
    for _ in range(number_of_variables):
        stdscr.addstr(f"Enter {args}'s ID: ")
        stdscr.refresh()
        id = loop_positive_integer(stdscr, "")
        stdscr.addstr(f"Enter {args}'s name: ")
        stdscr.refresh()
        curses.echo()
        name = stdscr.getstr().decode()
        curses.noecho()
        while not name.strip():
            try:
                stdscr.addstr("Error: Name cannot be empty. Please try again.\n")
                curses.echo()
                name = stdscr.getstr().decode()
                curses.noecho()
                stdscr.refresh()
            except ValueError:
                stdscr.addstr("Error: Invalid name. Please try again.\n")

        if args == "student":
            while True:
                try:
                    curses.echo()
                    stdscr.addstr(f"Enter {args} Date of Birth separate by '-' (YYYY-MM-DD): ")
                    stdscr.refresh()
                    dob_input = stdscr.getstr().decode()
                    dob_datetime = datetime.strptime(dob_input, "%Y-%m-%d")
                    break
                except ValueError:
                    stdscr.addstr("Error: Invalid date format. Please enter a valid date separate by '-' (YYYY-MM-DD).\n")
            items.append(cls(id, name, dob_datetime))  # Store dob_datetime in Student object

        else:
            while True:
                stdscr.addstr(f"Please enter the number of {args}'s credit: ")
                stdscr.refresh()
                credit = loop_positive_integer(stdscr, "")
                if credit >= 0:
                    items.append(cls(id, name, credit))
                    break
                else:
                    stdscr.addstr("Invalid credit value. Please enter a non-negative integer.\n")
                    stdscr.refresh()

    curses.noecho()
    info_array.show_student_info().extend(items) if args == "student" else info_array.show_course_info().extend(items)
    if number_of_variables == 1:
        s = ""
    else:
        s = "s"
    stdscr.addstr(f"{number_of_variables} {args}{s} added successfully.\n")
    stdscr.refresh()
    return info_array

def delete_item(stdscr, args, info):
    stdscr.clear()
    list_items(stdscr, args, info)
    stdscr.addstr(f"Enter the {args}'s ID to delete:\n")
    stdscr.refresh()
    id_to_delete = loop_positive_integer(stdscr, "ID to delete: ")

    info_copy = info.copy()

    for item in info_copy:
        if isinstance(item, Student) and item.show_student_id() == id_to_delete:
            info.remove(item)
            stdscr.addstr(f"{args.capitalize()} with ID {id_to_delete} deleted successfully.\n")
            return
        elif isinstance(item, Course) and item.show_course_id() == id_to_delete:
            info.remove(item)
            stdscr.addstr(f"{args.capitalize()} with ID {id_to_delete} deleted successfully.\n")
            return

    stdscr.addstr(f"Error: No {args} found with ID {id_to_delete}.\n")


def delete_mark(stdscr, marks):
    stdscr.clear()
    if not marks:
        stdscr.addstr("No marks available to delete.\n")
        stdscr.refresh()
        return

    stdscr.addstr("List of Marks:\n")
    for index, mark in enumerate(marks, start=1):
        student_id = mark.show_mark_student_id()
        course_id = mark.show_mark_course_id()
        mark_value = mark.show_mark()
        stdscr.addstr(f"{index}. Student ID: {student_id}, Course ID: {course_id}, Mark: {mark_value}\n")
    stdscr.refresh()

    while True:
        mark_index = loop_positive_integer(stdscr, "Enter the number of the mark you want to delete (0 to cancel): ")
        if mark_index == 0:
            stdscr.addstr("Operation canceled.\n")
            return
        elif 1 <= mark_index <= len(marks):
            deleted_mark = marks.pop(mark_index - 1)
            stdscr.addstr(f"Mark for Student ID: {deleted_mark.show_mark_student_id()}, Course ID: {deleted_mark.show_mark_course_id()} deleted successfully.\n")
            stdscr.refresh()
            return
        else:
            stdscr.addstr("Invalid input. Please enter a valid mark number.\n")


def input_mark(stdscr, student_infos, course_infos, marks):
    stdscr.clear()
    if not student_infos or not course_infos:
        stdscr.addstr("Please input students and courses first.\n")
        stdscr.refresh()
        return

    list_items(stdscr, "student", student_infos)
    stdscr.addstr("Enter the student's ID for mark input: ")
    stdscr.refresh()
    student_id = loop_positive_integer(stdscr, "")

    list_items(stdscr, "course", course_infos)
    stdscr.addstr("Enter the course's ID for mark input: ")
    stdscr.refresh()
    course_id = loop_positive_integer(stdscr, "")

    for student in student_infos:
        if student.show_student_id() == student_id:
            for course in course_infos:
                if course.show_course_id() == course_id:
                    while True:
                        stdscr.addstr(f"Enter the mark for {student.show_student_name()} in {course.show_course_name()}: ")
                        stdscr.refresh()
                        try:
                            curses.echo()
                            mark_value = float(stdscr.getstr().decode())
                            mark_value = math.floor(mark_value * 10) / 10
                            marks.append(Mark(student_id, course_id, mark_value))
                            stdscr.addstr("Mark added successfully.\n")
                            stdscr.refresh()
                            curses.noecho()
                            return
                        except ValueError:
                            stdscr.addstr("Error: Invalid mark. Please enter a valid number.\n")
                            stdscr.refresh()

    stdscr.addstr(f"Error: No student or course found with ID {student_id} or {course_id}.\n")

def list_items(stdscr, args, info):
    stdscr.clear()
    if args == "student":
        num_lines_per_item = 4
    elif args == "course":
        num_lines_per_item = 4
    else:
        num_lines_per_item = 1

    stdscr.addstr(f"List of {args}: \n")
    stdscr.addstr(" *** \n") 
    for item in info:
        if args == "student":
            stdscr.addstr(f"ID: {item.show_student_id()}\n")
            stdscr.addstr(f"Name: {item.show_student_name()}\n")
            stdscr.addstr(f"Date of Birth: {item.show_dob().strftime('%Y-%m-%d')}\n")

        elif args == "course":
            stdscr.addstr(f"ID: {item.show_course_id()}\n")
            stdscr.addstr(f"Name: {item.show_course_name().encode('utf-8').decode('utf-8')}\n")
            stdscr.addstr(f"Credit: {item.show_credit()}\n")

    stdscr.refresh()



def list_marks(stdscr, marks, student_infos, course_infos):
    stdscr.clear() 
    if not marks:
        stdscr.addstr("No marks available.\n")
        stdscr.refresh()
        return

    stdscr.addstr("List of Marks:\n")
    for mark in marks:
        student_name = next((student.show_student_name() for student in student_infos if student.show_student_id() == mark.show_mark_student_id()), "Unknown Student")
        course_name = next((course.show_course_name() for course in course_infos if course.show_course_id() == mark.show_mark_course_id()), "Unknown Course")
        mark_info = f"Student: {student_name}, Course: {course_name}, Mark: {mark.show_mark()}"
        stdscr.addstr(mark_info + "\n")
    stdscr.refresh()


def calculate_gpa(student_marks, course_credits):
    marks_array = np.array([mark.show_mark() for mark in student_marks])
    credits_array = np.array([course.show_credit() for course in course_credits])

    weighted_sum = np.sum(marks_array * credits_array)
    total_credits = np.sum(credits_array)
    gpa = weighted_sum / total_credits

    return gpa

def sort_students_by_gpa(stdscr, student_infos, course_infos, marks):
    stdscr.clear() 
    student_gpa_dict = {}

    for student in student_infos:
        student_id = student.show_student_id()
        student_marks = [mark for mark in marks if mark.show_mark_student_id() == student_id]
        gpa = calculate_gpa(student_marks, course_infos)
        student_gpa_dict[student_id] = gpa

    sorted_student_ids = sorted(student_gpa_dict, key=student_gpa_dict.get, reverse=True)

    stdscr.addstr("List of Students Sorted by GPA:\n")
    stdscr.addstr("-" * 50 + "\n")
    for student_id in sorted_student_ids:
        student_name = next((student.show_student_name() for student in student_infos if student.show_student_id() == student_id), "Unknown Student")
        gpa = student_gpa_dict[student_id]
        stdscr.addstr(f"ID: {student_id}, Name: {student_name}, GPA: {gpa:.2f}\n")
    stdscr.addstr("-" * 50 + "\n")

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    student_array = StudentArray()
    course_array = CourseArray()
    marks = []

    while True:
        stdscr.clear()
        stdscr.addstr("""
        0. Exit
        1. Input student(s).
        2. Input course(s).
        3. Delete specific student.
        4. Delete specific course.
        5. Delete specific mark.
        6. Input marks.
        7. List students.
        8. List courses.
        9. List marks.
        10. Sort students by GPA descending.
        """)

        stdscr.addstr("Your choice: ")
        stdscr.refresh()
        option = loop_positive_integer(stdscr, "")

        if option == 0:
            stdscr.addstr("Exiting...\n")
            stdscr.refresh()
            break

        elif option == 1:
            student_array = add_items(stdscr, "student", Student, student_array)

        elif option == 2:
            course_array = add_items(stdscr, "course", Course, course_array)

        elif option == 3:
            delete_item(stdscr, "student", student_array.show_student_info())

        elif option == 4:
            delete_item(stdscr, "course", course_array.show_course_info())

        elif option == 5:
            delete_mark(stdscr, marks)

        elif option == 6:
            input_mark(stdscr, student_array.show_student_info(), course_array.show_course_info(), marks)

        elif option == 7:
            list_items(stdscr, "student", student_array.show_student_info())

        elif option == 8:
            list_items(stdscr, "course", course_array.show_course_info())

        elif option == 9:
            list_marks(stdscr, marks, student_array.show_student_info(), course_array.show_course_info())

        elif option == 10:
            sort_students_by_gpa(stdscr, student_array.show_student_info(), course_array.show_course_info(), marks)

        else:
            stdscr.addstr("Invalid input. Please try again!\n")

        stdscr.getch()

curses.wrapper(main)