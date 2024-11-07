import os
import json
import sys
from random import Random
from src.db.course_data import get_course_instance_name, get_students

import psycopg2
from model.Student import Student

# course name
course_name = get_course_instance_name()


# Path to students
path_to_students = get_students(course_name)

# read the JSON files
with open(path_to_students) as file:
    student_data = json.load(file)

# Maak studenten objecten aan
students = []
for data in student_data["students"]:
    first_name, surname = data["name"].split(' ', 1)
    student = Student(
        id=data["number"],
        first_name=first_name,
        surname=surname,
        email=data["email"],
    )
    students.append(student)

# Verbinding maken met PostgreSQL
try:
    connection = psycopg2.connect(
        dbname="canvas_dashboard",
        user="innovation",
        password="admin",
        host="localhost",
        port="25432"
    )
    cursor = connection.cursor()

    # Tabel aanmaken voor de studenten als hij nog niet bestaat
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                student_id INTEGER,
                first_name VARCHAR(100),
                surname VARCHAR(100),
                email VARCHAR(100)
            )
        """)
    connection.commit()

    # Studenten toevoegen aan de database
    for student in students:
        cursor.execute("""
                INSERT INTO students (student_id, first_name, surname, email)
                VALUES (%s, %s, %s, %s)
            """, (student.id, student.first_name, student.surname, student.email))

    connection.commit()
    print("Data succesfully inserted")
except Exception as e:
    print("Error: ", e)

finally:
    if connection:
        cursor.close()
        connection.close()
