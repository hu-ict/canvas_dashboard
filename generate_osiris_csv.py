import sys

from scripts.lib.file_const import ENVIRONMENT_FILE_NAME
from scripts.lib.lib_date import get_actual_date, get_date_time_obj
from scripts.lib.file import read_course, read_results, read_environment

def write_osiris_data_csv(filename, course, student_results, assignment_id):
    print('CSV01 - write_osiris_data_csv', filename)
    with open(filename, 'w', encoding="utf-8") as csvfile:
        csvfile.write('Studentnummer;Naam;Resultaat\n')
        for student_result in student_results:
            student = course.find_student(student_result.id)
            grade_moment = student_result.get_grade_moment(assignment_id)
            # print(opdracht)
            if grade_moment.grade == "0":
                osiris_grade = "NA"
            elif grade_moment.grade == "1":
                osiris_grade = "NN"
            elif grade_moment.grade == "2":
                osiris_grade = "ON"
            elif grade_moment.grade == "3":
                osiris_grade = "BN"
            else:
                osiris_grade = "NA"
            csvfile.write(student.number + ";" + student.sortable_name + ";" + osiris_grade + "\n")


def run_env_4(a_actual_date):
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    execution = environment.get_execution_by_name("env_3")
    for course in environment.courses:
        for course_instance in course.course_instances:
            if course_instance.stage != "SLEEP": #get_date_time_obj(course_instance.period["end_date"]) > a_actual_date and
                print("Instance:", course_instance.name)
                course_instance.execution_source_path = execution.source_path

                generate_osiris_csv(course_instance)


def generate_osiris_csv(course_instance):
    print("GOC02 - Instance:", course_instance.name)
    assignment_id = 366679
    course = read_course(course_instance.get_course_file_name())
    results = read_results(course_instance.get_result_file_name())
    write_osiris_data_csv(course_instance.get_osiris_data_file_name(), course, results.students, assignment_id)

if __name__ == "__main__":
    l_actual_date = get_actual_date()
    sys.stdout.reconfigure(encoding="utf-8")
    run_env_4(l_actual_date)
    total_seconds = (get_actual_date() - l_actual_date).seconds
    seconds = total_seconds % 60
    minutes = total_seconds // 60
    print(f"Time running: {minutes}:{seconds:02d} (m:ss)")
    print("Time running:", total_seconds, "seconds")
    print("Date running:", get_actual_date())
