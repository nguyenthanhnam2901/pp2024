from datetime import datetime

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