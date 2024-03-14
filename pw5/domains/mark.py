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