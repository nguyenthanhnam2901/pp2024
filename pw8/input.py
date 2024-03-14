import curses
import math
import numpy as np
from datetime import datetime
from output import list_items, list_marks, sort_students_by_gpa
from domains.student import Student, StudentArray
from domains.course import Course, CourseArray
from domains.mark import Mark

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
            items.append(cls(id, name, dob_datetime))

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
