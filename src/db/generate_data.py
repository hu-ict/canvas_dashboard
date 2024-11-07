import os
import json
import sys
from random import Random

import psycopg2
from model.Student import Student

# paths to the JSON files
base_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path_student = os.path.join(base_dir, '..', '..', 'courses', "inno", f"result_inno.json")

# read the JSON files
with open(json_file_path_student) as file:
    data = json.load(file)

# Maak studenten objecten aan
students = []
for student_data in data["students"]:
    first_name, surname = student_data["name"].split(' ', 1)
    student = Student(
        id=student_data["number"],
        first_name=first_name,
        surname=surname,
        email=student_data["email"],
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
