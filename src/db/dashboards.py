import os
import glob
import json
import psycopg2
from src.db.course_data import get_course_instance_name


course_name = get_course_instance_name()

try:
    connection = psycopg2.connect(
        dbname="canvas_dashboard",
        user="innovation",
        password="admin",
        host="database",
        port="5432"
    )

    cursor = connection.cursor()

    # Haal alle studenten op uit de database
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()


    def find_dashboard_by_student_name(email):
        print(students)
        for student in students:
            if student[3] == email:
                student_name = student[1] + " " + student[2]
                # Zoek naar HTML-bestanden in de opgegeven map
                matches = glob.glob(f'./courses/{course_name}/dashboard_{course_name}/students/*.html')
                print(f"Matches found: {matches}")  # Print matches for debugging

                # Filter de matches op basis van de studentnaam
                student_dashboard = [match for match in matches if student_name in os.path.basename(match)]

                if student_dashboard:
                    return student_dashboard[1]  # Return the eerste match
                else:
                    return print("No dashboard found for this student")

        return print("Student not found in database")


except Exception as e:
    print(f"An error occurred: {e}")
