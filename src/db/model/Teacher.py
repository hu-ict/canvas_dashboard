class Teacher:
    def __init__(self, id, first_name, surname, email):
        self.id = id
        self.first_name = first_name
        self.surname = surname
        self.email = email

    def __str__(self):
        return f"{self.first_name} {self.surname} - {self.email}"
