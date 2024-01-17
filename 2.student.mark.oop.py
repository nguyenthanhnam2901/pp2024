from datetime import datetime

class Student:
    def __init__(self, id, name, dob):
        self.id = id
        self.name = name
        self.dob = dob

class Course:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Mark:
    def __init__(self, student_id, course_id, mark):
        self.student_id = student_id
        self.course_id = course_id
        self.mark = mark

def loop_positive_integer(prompt):
    while True:
        try:
            number = int(input(prompt))
            if number >= 0:
                return number
            else:
                print("Invalid value. Please enter a non-negative number.")
        except ValueError:
            print("Error: value must be an integer. Please try again.")

def add_items(cls, args, info, num):
    number_of_variables = int(input(f"Enter the number of {args} you want to add: "))

    for _ in range(number_of_variables):
        info.append(cls(**input_info(args, 1)))

    if number_of_variables == 1:
        s = ""
    else:
        s = "s"

    print(f"{number_of_variables} {args}{s} added successfully.")
    return num + number_of_variables


def delete_item(args, info):
    list_items(args, info)
    print(f"Enter the {args}'s ID to delete:")
    id_to_delete = loop_positive_integer("ID to delete: ")

    for item in info:
        if item.id == id_to_delete:
            info.remove(item)
            print(f"{args.capitalize()} with ID {id_to_delete} deleted successfully.")
            return

    print(f"Error: No {args} found with ID {id_to_delete}.")
    list_items(args, info)  # Reprint the updated list

def input_info(args, num):
    item = {}
    if not num:
        print(f"Please input {args}(s) you want first.")
    else:
        for _ in range(num):
            print(f"Enter {args}'s ID: ")
            
            while True:
                item["id"] = loop_positive_integer("ID: ")
                item["name"] = input(f"Enter {args}'s name: ")
                
                if args == "student":
                    while True:
                        try:
                            item["dob"] = datetime.strptime(input(f"Enter {args} Date of Birth separate by '-' (YYYY-MM-DD): "), "%Y-%m-%d")
                            break
                        except ValueError:
                            print("Error: Invalid date format. Please enter a valid date separate by '-' (YYYY-MM-DD).")
                break
    return item

def input_mark(student_infos, course_infos, mark):
    if not student_infos or not course_infos:
        print("Please input students and courses first.")
        return

    list_items("student", student_infos)
    student_id = loop_positive_integer("Enter the student's ID for mark input: ")

    list_items("course", course_infos)
    course_id = loop_positive_integer("Enter the course's ID for mark input: ")

    for student in student_infos:
        if student.id == student_id:
            for course in course_infos:
                if course.id == course_id:
                    while True:
                        try:
                            mark_value = float(input(f"Enter the mark for {student.name} in {course.name}: "))
                            mark.append(Mark(student_id, course_id, mark_value))
                            print("Mark added successfully.")
                            return
                        except ValueError:
                            print("Error: Invalid mark. Please enter a valid number.")

    print(f"Error: No student or course found with ID {student_id} or {course_id}.")

def list_items(args, info):
    print(f"List of {args}: ")
    for item in info:
        print(item.__dict__)

def list_marks(marks, student_infos, course_infos):
    if not marks:
        print("No marks available.")
        return

    print("List of Marks:")
    for mark in marks:
        student_name = next((student.name for student in student_infos if student.id == mark.student_id), "Unknown Student")
        course_name = next((course.name for course in course_infos if course.id == mark.course_id), "Unknown Course")
        print(f"Student: {student_name}, Course: {course_name}, Mark: {mark.mark}")

def main():
    number_of_students = 0
    number_of_courses = 0
    student_infos = []
    course_infos = []
    marks = []

    while True:
        try:
            print("""
            0. Exit
            1. Input student(s).
            2. Input course(s).
            3. Delete specific student.
            4. Delete specific course.
            5. Input info of students.
            6. Input info of courses.
            7. Input marks.
            8. List students.
            9. List courses.
            10. List marks.
            """)

            option = int(input("Your choice: "))
            if option == 0:
                break

            elif option == 1:
                number_of_students = add_items(Student, "student", student_infos, number_of_students)

            elif option == 2:
                number_of_courses = add_items(Course, "course", course_infos, number_of_courses)

            elif option == 3:
                delete_item("student", student_infos)

            elif option == 4:
                delete_item("course", course_infos)

            elif option == 5:
                student_infos = input_info("student", number_of_students)

            elif option == 6:
                course_infos = input_info("course", number_of_courses)

            elif option == 7:
                input_mark(student_infos, course_infos, marks)

            elif option == 8:
                list_items("student", student_infos)

            elif option == 9:
                list_items("course", course_infos)

            elif option == 10:
                list_marks(marks, student_infos, course_infos)

            else:
                print("Invalid input. Please try again!")

        except ValueError:
            print("Error: Invalid input format.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
