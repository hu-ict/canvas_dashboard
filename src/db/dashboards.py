import glob
import os

from src.db.course_data import get_course_instance_name
from src.db.db_context import context, close_connection


def find_dashboard_by_student_name(email):
    global cursor, connection
    course_name = get_course_instance_name()

    try:

        cursor, connection = context()

        # Haalt alle studenten op uit de database

        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        print(students)
        for student in students:
            if student[3] == email:
                student_name = student[1] + " " + student[2]
                # Zoekt naar HTML-bestanden in de opgegeven map
                matches = glob.glob(f'./courses/{course_name}/dashboard_{course_name}/students/*.html')
                print(f"Matches found: {matches}")  # Print matches for debugging

                # Zoekt naar de html die overeenkomt met de studentnaam
                student_dashboard = [match for match in matches if
                                     student_name in os.path.basename(match) and match.endswith('index.html')]

                if student_dashboard:
                    return student_dashboard[0]
                else:
                    return print("No dashboard found for this student")

        return print("Student not found in database")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        close_connection(cursor, connection)
