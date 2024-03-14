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