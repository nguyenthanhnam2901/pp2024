import os
import pickle
import zipfile
from domains.student import Student, StudentArray
from domains.course import Course, CourseArray
from domains.mark import Mark

def write_to_txt(filename, data):
    with open(filename, 'w') as file:
        if isinstance(data[0], Course):
            for item in data:
                file.write(f"ID: {item.show_course_id()}\n")
                file.write(f"Name: {item.show_course_name()}\n")
                file.write(f"Credit: {item.show_credit()}\n")
                file.write("-" * 20 + "\n")
        elif isinstance(data[0], Student):
            for item in data:
                file.write(f"ID: {item.show_student_id()}\n")
                file.write(f"Name: {item.show_student_name()}\n")
                file.write(f"Date of Birth: {item.show_dob().strftime('%Y-%m-%d')}\n")
                file.write("-" * 20 + "\n")
        elif isinstance(data[0], Mark):
            for item in data:
                file.write(f"Student ID: {item.show_mark_student_id()}\n")
                file.write(f"Course ID: {item.show_mark_course_id()}\n")
                file.write(f"Mark: {item.show_mark()}\n")
                file.write("-" * 20 + "\n")
        else:
            for item in data:
                file.write(str(item) + '\n')

def save_data_to_txt(student_array, course_array, marks):
    write_to_txt('students.txt', student_array.show_student_info())
    write_to_txt('courses.txt', course_array.show_course_info())
    write_to_txt('marks.txt', marks)

def compress_files(student_array, course_array, marks):
    if not marks:
        print("Error: No marks data to compress.")
        return

    with open("data.dat", "wb") as f:
        pickle.dump((student_array.show_student_info(), course_array.show_course_info(), marks), f)

    print("Data compressed successfully.")

def decompress_files():
    if os.path.exists("data.dat"):
        with open("data.dat", "rb") as f:
            student_info, course_info, marks = pickle.load(f)
    else:
        print("Error: 'data.dat' file not found.")
        return [], [], []

    return student_info, course_info, marks