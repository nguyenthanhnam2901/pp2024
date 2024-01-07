from datetime import datetime

#Loop until input is positive integer:
def loop_positive_integer(agrs):
    while True:
        try:
            number = int(input(agrs))
            if number >= 0:
                return number
            else:
                print("Invalid value. Please enter a non-negative number.")
        except ValueError:
            print("Error: value must be an integer. Please try again.")

#Input number of student or course:
def number_of_items(args):
    print("Enter the number of " + args + " in this class: ")
    return loop_positive_integer("")

#Add extra student or course:
def add_items(args, info, num):
    number_of_variables = int(input("Enter the number of "+ args +" you want to add: "))     
    
    for _ in range(number_of_variables):
        info.append(input_info(args,1))

    if number_of_variables == 1:
        s = "" 
    else: 
        s = "s"

    print(f"{number_of_variables} {args}{s} added successfully.")
    return num + number_of_variables

#Delete a specific item:
def delete_item(args, info):
    list_items(args, info)
    print(f"Enter the {args}'s ID to delete:")
    id_to_delete = loop_positive_integer("ID to delete: ")

    for item in info:
        if item["id"] == id_to_delete:
            info.remove(item)
            print(f"{args.capitalize()} with ID {id_to_delete} deleted successfully.")
            return

    print(f"Error: No {args} found with ID {id_to_delete}.")
    list_items(args, info)  # Reprint the updated list

#Basic input info: (no choose for update yet~)
def input_info(args, num):
    item = {}
    if not num: 
            print("Please input student(s) you want first.")
    
    else:
        for _ in range(num):                 
            print("Enter " + args + "'s ID: ")
            
            while True:
                item["id"] = loop_positive_integer("ID: ")
                item["name"] = input("Enter " + args + "'s name: ")
                
                if args == "student":
                    while True:
                        try:
                            item["DoB"] = datetime.strptime(input(f"Enter " + args + " Date of Birth seperate by '-' (YYYY-MM-DD): "), "%Y-%m-%d")
                            break  
                        except ValueError:
                            print("Error: Invalid date format. Please enter a valid date seperate by '-' (YYYY-MM-DD).")
                break
    return item

#Input mark for a specific student with a specific course:
def input_mark(student_infos, course_infos, mark):
    if not student_infos or not course_infos:
        print("Please input students and courses first.")
        return

    list_items("student", student_infos)
    student_id = loop_positive_integer("Enter the student's ID for mark input: ")

    list_items("course", course_infos)
    course_id = loop_positive_integer("Enter the course's ID for mark input: ")

    for student in student_infos:
        if student["id"] == student_id:
            for course in course_infos:
                if course["id"] == course_id:
                    while True:
                        try:
                            mark_value = float(input(f"Enter the mark for {student['name']} in {course['name']}: "))
                            mark.append({
                                "student_id": student_id,
                                "course_id": course_id,
                                "mark": mark_value
                            })
                            print("Mark added successfully.")
                            return
                        except ValueError:
                            print("Error: Invalid mark. Please enter a valid number.")
    
    print(f"Error: No student or course found with ID {student_id} or {course_id}.")

#List student or course
def list_items(args, info):
    print(f"List of {args}: ")
    for item in info:
        print(item)

#List mark
def list_marks(marks, student_infos, course_infos):
    if not marks:
        print("No marks available.")
        return

    print("List of Marks:")
    for mark in marks:
        student_name = next((student["name"] for student in student_infos if student["id"] == mark["student_id"]), "Unknown Student")
        course_name = next((course["name"] for course in course_infos if course["id"] == mark["course_id"]), "Unknown Course")
        print(f"Student: {student_name}, Course: {course_name}, Mark: {mark['mark']}")



def main():
    number_of_students = 0
    number_of_courses = 0
    student_infos = []
    coure_infos = []
    mark = []

    while True:
        print("""
        0. Exit
        1. Input number of students.
        2. Input number of courses.
        3. Add extra student(s).     
        4. Add extra course(s).
        5. Delete specific student.
        6. Delete specific course.
        7. Input info of students.
        8. Input info of courses.
        9. Input marks.
        10. List students.
        11. List courses.
        12. List all information.
        """)

        option = int(input("Your choice: "))
        if option == 0:
            break
        
        elif option == 1:
            number_of_students = number_of_items("students")

        elif option == 2:
            number_of_courses = number_of_items("courses")

        elif option == 3:
            add_items("student", student_infos, number_of_students)

        elif option == 4:
            add_items("course", coure_infos, number_of_courses)

        elif option == 5:
            delete_item("student", student_infos)

        elif option == 6:
            delete_item("course", coure_infos)

        elif option == 7:
            student_infos = input_info("student", number_of_students)

        elif option == 8:
            coure_infos = input_info("course", number_of_courses)

        elif option == 9:
            input_mark(student_infos, coure_infos, mark)

        elif option == 10:
            list_items("student", student_infos, number_of_students)

        elif option == 11:
            list_items("course", coure_infos, number_of_courses)

        elif option == 12:
            list_marks(mark, student_infos, coure_infos)

        else:
            print("Invalid input. Please try again!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"exiting...")
        exit(0)