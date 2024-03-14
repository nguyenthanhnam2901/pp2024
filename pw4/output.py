import curses
import numpy as np
import math
from domains.student import Student
from domains.course import Course
from domains.mark import Mark

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

def calculate_gpa(student_marks, course_credits):
    marks_array = np.array([mark.show_mark() for mark in student_marks])
    credits_array = np.array([course.show_credit() for course in course_credits])

    weighted_sum = np.sum(marks_array * credits_array)
    total_credits = np.sum(credits_array)
    gpa = weighted_sum / total_credits

    return gpa
