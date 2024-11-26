import json
import os

from src.db.db_context import context, close_connection
from src.db.model.Student import Student
from src.db.model.Teacher import Teacher

COURSES_PATH = os.path.abspath(os.path.join(os.getcwd(), "courses"))


def initialize_db(cursor, connection):
    try:
        print("Start database-initialisatie")

        print("Aanmaken van tabellen...")

        # Create the 'students' table with 'email' as unique
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                first_name VARCHAR(100),
                surname VARCHAR(100),
                email VARCHAR(100) UNIQUE
            );
        """)

        # Create the 'courses' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                directory_name VARCHAR(100) NOT NULL
            );
        """)

        # Create the 'teachers' table with 'email' as unique
        cursor.execute("""
                  CREATE TABLE IF NOT EXISTS teachers (
                      id INTEGER PRIMARY KEY,
                      first_name VARCHAR(100),
                      surname VARCHAR(100),
                      email VARCHAR(100) UNIQUE
                  );
              """)
        # Create the 'teacher_courses' table with a composite primary key
        cursor.execute("""
                   CREATE TABLE IF NOT EXISTS teacher_courses (
                       teacher_id INTEGER REFERENCES teachers(id),
                       course_id INTEGER REFERENCES courses(id),
                       PRIMARY KEY (teacher_id, course_id)
                   );
               """)

        # Create the 'student_courses' table with a composite primary key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_courses (
                student_id INTEGER REFERENCES students(id),
                course_id INTEGER REFERENCES courses(id),
                PRIMARY KEY (student_id, course_id)
            );
        """)
        print("Tabellen zijn succesvol aangemaakt.")
        connection.commit()
    except Exception as e:
        print(f"Fout bij initialisatie van de database: {e}")


def insert_student(cursor, student):
    # Checks if student already exists in the database
    cursor.execute("SELECT id FROM students WHERE email = %s", (student.email,))
    result = cursor.fetchone()

    if result:
        # Student already exists, return existing ID
        print(f"Student met e-mail {student.email} bestaat al in de database.")
        return result[0]
    else:
        # Student does not exist, insert student and return new ID
        cursor.execute("""
            INSERT INTO students (id, first_name, surname, email)
            VALUES (%s, %s, %s, %s)
        """, (student.id, student.first_name, student.surname, student.email))
        print(f"Student {student.first_name} {student.surname} toegevoegd aan de database.")
        return student.id


def insert_teacher(cursor, teacher):
    # Checks if teacher already exists in the database
    cursor.execute("SELECT id FROM teachers WHERE email = %s", (teacher.email,))
    result = cursor.fetchone()
    if result:
        # Teacher already exists, return existing ID
        print(f"Teacher with email {teacher.email} already exists in the database.")
        return result[0]
    else:
        # Teacher does not exist, insert teacher and return new ID
        cursor.execute("""
            INSERT INTO teachers (id, first_name, surname, email)
            VALUES (%s, %s, %s, %s)
        """, (teacher.id, teacher.first_name, teacher.surname, teacher.email))
        print(f"Teacher {teacher.first_name} {teacher.surname} added to the database.")
        return teacher.id


def insert_course(cursor, course_id, course_name, directory_name):
    cursor.execute("""
        INSERT INTO courses (id, name, directory_name)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (course_id, course_name, directory_name))


def insert_student_course_relation(cursor, student_id, course_id):
    # Insert student-course relation if it does not exist yet
    cursor.execute("""
        INSERT INTO student_courses (student_id, course_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (student_id, course_id))


def insert_teacher_course_relation(cursor, teacher_id, course_id):
    # Insert student-course relation if it does not exist yet
    cursor.execute("""
        INSERT INTO teacher_courses (teacher_id, course_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (teacher_id, course_id))


def read_and_import_courses(cursor, connection):
    try:
        print("Start importeren van cursussen en studenten...")

        # Check if the 'courses' directory exists
        if not os.path.exists(COURSES_PATH):
            print(f"De 'courses' map bestaat niet op {COURSES_PATH}. Zorg ervoor dat deze map correct is ingesteld.")
            return

        # Connect to the database
        cursor, connection = context()

        # Loop through all directories in the 'courses' directory
        for course_dir in os.listdir(COURSES_PATH):
            course_path = os.path.join(COURSES_PATH, course_dir, f'result_{course_dir}.json')
            config_path = os.path.join(COURSES_PATH, course_dir, f'config_{course_dir}.json')

            # Check if the course file exists
            if os.path.isfile(course_path):
                with open(course_path, 'r') as file:
                    course_data = json.load(file)

                    # Get the course ID and name
                    course_id = course_data.get("id")
                    course_name = course_data.get("name")
                    print(f"Importeer cursus: {course_name} met ID {course_id}")

                    # Add course to the database
                    insert_course(cursor, course_id, course_name, course_dir)

                    # Add students from the course to the database
                    students = course_data.get("students", [])
                    for data in students:
                        first_name, surname = data["name"].split(' ', 1)
                        student = Student(
                            id=data["number"],  # Number = student ID
                            first_name=first_name,
                            surname=surname,
                            email=data["email"]
                        )

                        # Add the student to the database or get the existing student ID
                        student_id = insert_student(cursor, student)

                        # Map the student to the course
                        insert_student_course_relation(cursor, student_id, course_id)
                if os.path.isfile(config_path):
                    with open(config_path, 'r') as file:
                        config_data = json.load(file)
                        # Add teachers from the course to the database
                        teachers = config_data.get("teachers", [])
                        for data in teachers:
                            first_name, surname = data["name"].split(' ', 1)
                            teacher = Teacher(
                                id=data["id"],  # Number = student ID
                                first_name=first_name,
                                surname=surname,
                                email=data["email"]
                            )
                            # Add the student to the database or get the existing teacher ID
                            teacher_id = insert_teacher(cursor, teacher)
                            # Map the teacher to the course
                            insert_teacher_course_relation(cursor, teacher_id, course_id)

        # Save changes to the database and close the connection
        connection.commit()
        print("Cursus- en studentgegevens succesvol geïmporteerd in de database.")
    except Exception as e:
        print(f"Fout bij het importeren van cursussen en studenten: {e}")


if __name__ == "__main__":
    initialize_db()
    read_and_import_courses()
