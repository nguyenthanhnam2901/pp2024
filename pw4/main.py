import curses
from input import loop_positive_integer, add_items, delete_item, delete_mark, input_mark
from output import list_items, list_marks, sort_students_by_gpa
from domains.student import Student, StudentArray
from domains.course import Course, CourseArray
from domains.mark import Mark
import numpy as np
import math

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
