
class Instance:

    def __init__(self, id, start_date, end_date, students):
        self.Id = id
        self.start_date = start_date
        self.end_date = end_date
        self.students = students

    def __str__(self):
        return f"{self.start_date} - {self.end_date} - {self.students}"

    def add_student(self, student):
        self.students.append(student)


