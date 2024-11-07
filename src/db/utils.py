import os
import glob
import json
import psycopg2

base_dir = os.path.dirname(os.path.abspath(__file__))
json_courses = os.path.join(base_dir, '..', '..' ,'courses', 'course_instances.json')
# read the JSON files
with open(json_courses) as file:
    data = json.load(file)

course_name = data["current_instance"]

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
            if student[4] == email:
                student_name = student[2] + " " + student[3]
                # Zoek naar HTML-bestanden in de opgegeven map
                matches = glob.glob(f'./courses/{course_name}/dashboard_INNO/students/*.html')
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
