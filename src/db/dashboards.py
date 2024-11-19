import os
import glob
from src.db.course_data import get_course_instance_name
from src.db.db_context import context, close_connection


def find_dashboard_by_student_name(email, course_id):
    # get the course name based on the course_id
    course_name = get_course_instance_name(course_id)

    if not course_name:
        print(f"Geen directory naam gevonden voor course ID {course_id}")
        return None

    try:
        cursor, connection = context()
        cursor.execute("SELECT first_name, surname FROM students WHERE email = %s", (email,))
        student = cursor.fetchone()
        if not student:
            print(f"Geen student gevonden met email {email}")
            return None

        # Name of the student
        student_name = f"{student[0]} {student[1]}"

        # Path to the students directory
        students_path = f'./courses/{course_name}/dashboard_{course_name}/students/'

        # Search for the student dashboard in the students directory
        student_dashboard = glob.glob(f"{students_path}/{student_name} index.html")

        if student_dashboard:
            return student_dashboard[0]
        else:
            print(f"Geen dashboard gevonden voor student: {student_name}")
            return None
    except Exception as e:
        print(f"Fout bij het zoeken naar het dashboard van de student {email}: {e}")
        return None
    finally:
        close_connection(cursor, connection)
