import json
import os

from src.db.db_context import context, close_connection


def get_course_instance_name(course_id=None):
    # this function is used to get the course directory name based on the course_id
    # if no course_id is given, it will return the current course instance name
    if course_id:
        cursor, connection = context()
        try:
            cursor.execute("SELECT directory_name FROM courses WHERE id = %s", (course_id,))
            result = cursor.fetchone()
            if result:
                return result[0]  # directory_name
            else:
                print(f"Course ID {course_id} niet gevonden.")
                return None
        except Exception as e:
            print(f"Fout bij ophalen van course directory voor course ID {course_id}: {e}")
            return None
        finally:
            close_connection(cursor, connection)
    else:
        # check the current course instances
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_courses = os.path.join(base_dir, '..', '..', 'courses', 'course_instances.json')

        with open(json_courses) as file:
            data = json.load(file)

        return data["current_instance"]


def get_students(course_instance_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, '..', '..', 'courses', course_instance_name, f"result_{course_instance_name}.json")


def get_student_courses(student_email):
    cursor, connection = context()
    try:
        cursor.execute("""
            SELECT courses.id, courses.name, courses.directory_name 
            FROM courses 
            JOIN student_courses ON courses.id = student_courses.course_id 
            JOIN students ON students.id = student_courses.student_id 
            WHERE students.email = %s
        """, (student_email,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Fout bij ophalen van cursussen voor student {student_email}: {e}")
        return []
    finally:
        close_connection(cursor, connection)


def get_teacher_courses(teacher_email):
    cursor, connection = context()
    try:
        cursor.execute("""
            SELECT courses.id, courses.name, courses.directory_name 
            FROM courses 
            JOIN teacher_courses ON courses.id = teacher_courses.course_id 
            JOIN teachers ON teachers.id = teacher_courses.teacher_id 
            WHERE teachers.email = %s
        """, (teacher_email,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Fout bij ophalen van cursussen voor docent {teacher_email}: {e}")
        return []
    finally:
        close_connection(cursor, connection)
