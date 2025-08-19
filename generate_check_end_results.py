import sys
import json

from canvasapi import Canvas

from lib.file import read_start, read_course, read_progress, read_results, read_course_instances, \
    read_dashboard_from_canvas
from lib.lib_date import get_actual_date, API_URL
from lib.lib_progress import get_overall_progress
from model.ProgressDay import ProgressDay
from model.perspective.Perspectives import Perspectives
from model.perspective.StudentPerspective import StudentPerspective
from model.perspective.StudentPerspectives import StudentPerspectives

def check_level(instance_name, level_moment):
    print("CL01 - generate_check_and_results.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    start = read_start(instance.get_start_file_name())
    course = read_course(instance.get_course_file_name())
    results = read_results(instance.get_result_file_name())
    canvas = Canvas(API_URL, start.api_key)
    canvas_course = canvas.get_course(course.canvas_id)
    level_serie_collection = read_dashboard_from_canvas(canvas_course)
    problems = []
    for student_results in results.students:
        student = course.find_student(student_results.id)
        if len(student.project_teachers) == 0:
            print("GCR30 - Heeft geen project_teacher:", student)
            teacher_name = "Berend Wilkens"
        else:
            teacher = course.find_teacher(student.project_teachers[0])
            if teacher is None:
                teacher_name = "Berend Wilkens"
            else:
                teacher_name = teacher.name
        # print(student.name, student_results.get_grade_moment_submissions_by_query(["beoordeling", "student"])[0].grade)
        perspectives = StudentPerspectives()
        level_perspectives = []
        for perspective in student_results.perspectives.values():
            # print(perspective.name, "eind", student.get_judgement(perspective.name), "calc", perspective.progress)

            perspectives.perspectives[perspective.name] = StudentPerspective(perspective.name,
                                                                             student_results.get_level_moment_submission_by_query(
                                                                                 [perspective.name, level_moment]), 0,
                                                                             0, 0)
            level_moment_submission = student_results.get_level_moment_submission_by_query(perspective.name)
            if level_moment_submission is None:
                level_determined = 0
            else:
                grade = level_moment_submission.grade
                if grade is None:
                    level_determined = 0;
                else:
                    level_determined = int(grade)
            level_perspectives.append(level_determined)
            if level_determined is None:
                level_determined = 0
            level_determined_label = level_serie_collection.level_series[course.level_moments.levels].grades[str(level_determined)].label.upper()
            level_flow_calculated_label = level_serie_collection.level_series[course.level_moments.levels].grades[str(perspective.progress)].label.upper()

            if level_determined != int(perspective.progress):
                problems.append({"problem": 1,
                                 "teacher": teacher_name,
                                 "message": f"{student_results.name} {perspective.name.upper()} perspectief, bepaalde beoordeling {level_determined_label} inconsistent met berekende beoordeling {level_flow_calculated_label}"})

        overall_level_calculated = get_overall_progress(level_perspectives)
        overall_level_determined = student_results.get_level_moment_submission_by_query(["student", level_moment]).grade
        if overall_level_determined is None:
            overall_level_determined = 0
        overall_level_determined_label = level_serie_collection.level_series[course.level_moments.levels].grades[str(overall_level_determined)].label.upper()
        overall_level_calculated_label = level_serie_collection.level_series[course.level_moments.levels].grades[str(overall_level_calculated)].label.upper()
        overall_level_flow_calculated_label = level_serie_collection.level_series[course.level_moments.levels].grades[str(student_results.progress)].label.upper()

        if int(overall_level_determined) != int(overall_level_calculated):
            problems.append({"problem": 3,
                             "teacher": teacher_name,
                             "message": f"FOUT {student_results.name} OVERALL, bepaalde beoordeling {overall_level_determined_label} inconsistent met regels voor berekende beoordeling {overall_level_calculated_label}"})
        elif int(overall_level_determined) != int(student_results.progress):
            problems.append({"problem": 2,
                             "teacher": teacher_name,
                             "message": f"{student.name} OVERALL, bepaalde beoordeling {overall_level_determined_label} inconsistent met de flow_berekende {overall_level_flow_calculated_label} beoordeling"})
        elif int(overall_level_calculated) != int(student_results.progress):
            problems.append({"problem": 4,
                             "teacher": teacher_name,
                             "message": f"{student.name} OVERALL, berekende beoordeling {overall_level_calculated_label} inconsistent met de flow_berekende {overall_level_flow_calculated_label} beoordeling"})
        else:
            pass
    problems = sorted(problems, key=lambda s: s["teacher"])
    for item in problems:
        if item["problem"] == 3:
            print("Issue:", item["problem"], item["teacher"], item["message"])

    print("GCR99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")

def check_beoordeling(instance_name):
    print("GCR01 - generate_check_and_results.py")
    fase = "Beoordeling"
    print("CL01 - generate_check_and_results.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    start = read_start(instance.get_start_file_name())
    course = read_course(instance.get_course_file_name())
    results = read_results(instance.get_result_file_name())
    canvas = Canvas(API_URL, start.api_key)
    canvas_course = canvas.get_course(course.canvas_id)
    dashboard = read_dashboard_from_canvas(canvas_course)
    problems = []
    for student_results in results.students:
        student = course.find_student(student_results.id)
        if len(student.project_teachers) == 0:
            print("GCR30 - Heeft geen project_teacher:", student)
            teacher_name = "Berend Wilkens"
        else:
            teacher = course.find_teacher(student.project_teachers[0])
            if teacher is None:
                teacher_name = "Berend Wilkens"
            else:
                teacher_name = teacher.name
        # print(student.name, student_results.get_grade_moment_submissions_by_query(["beoordeling", "student"])[0].grade)
        perspectives = StudentPerspectives()
        grade_perspectives = []
        for perspective in student_results.perspectives.values():
            # print(perspective.name, "eind", student.get_judgement(perspective.name), "calc", perspective.progress)

            perspectives.perspectives[perspective.name] = StudentPerspective(perspective.name,
                                                                             student_results.get_grade_moment_submission_by_query(
                                                                                 [perspective.name, fase]), 0,
                                                                             0, 0)
            grade = student_results.get_grade_moment_submission_by_query([perspective.name]).grade
            if grade is None:
                grade_determined = 0
            else:
                grade_determined = int(grade)
            grade_perspectives.append(grade_determined)
            grade_determined_label = dashboard.level_serie_collection.level_series[course.grade_moments.levels].grades[str(grade_determined)].label.upper()
            grade_flow_calculated_label = dashboard.level_serie_collection.level_series[course.grade_moments.levels].grades[str(perspective.progress)].label.upper()
            # print("GCR11 -", student.name, perspective.name, grade_determined != int(perspective.progress), grade_determined, perspective.progress)
            # print("GCR12 -", grade_determined, perspective.progress, grade_determined != int(perspective.progress))
            submission_grade_verantwoordingsdocument = 0
            submission_grade_deep_dive = 0
            if perspective.name.upper() == "GILDE":
                # deep dive
                submission = perspective.get_submission_by_assignment(344730)
                if submission is not None:
                    if submission.grade is not None:
                        submission_grade_deep_dive = int(submission.grade)
                # verantwoordingsdocument
                submission = perspective.get_submission_by_assignment(344731)
                if submission is not None:
                    if submission.grade is not None:
                        submission_grade_verantwoordingsdocument = int(submission.grade)
            if perspective.name.upper() == "GILDE" and (grade_determined >= 2 and submission_grade_verantwoordingsdocument < 3):
                grade_flow_calculated_label = dashboard.level_serie_collection.level_series[course.perspectives[perspective.name].levels].grades[str(submission_grade_verantwoordingsdocument)].label.upper()
                problems.append({"problem": 7,
                                 "teacher": teacher_name,
                                 "message": f"{student.name} {perspective.name.upper()} perspectief, bepaalde beoordeling {grade_determined_label} inconsistent met verantwoordingsdocument {grade_flow_calculated_label}"})
            elif perspective.name.upper() == "GILDE" and (grade_determined >= 2 and submission_grade_deep_dive < 3):
                grade_flow_calculated_label = dashboard.level_serie_collection.level_series[course.perspectives[perspective.name].levels].grades[str(submission_grade_deep_dive)].label.upper()
                problems.append({"problem": 8,
                                 "teacher": teacher_name,
                                 "message": f"{student.name} {perspective.name.upper()} perspectief, bepaalde beoordeling {grade_determined_label} inconsistent met deep dive {grade_flow_calculated_label}"})
            elif perspective.name.upper() == "GILDE" and grade_determined != int(perspective.progress) and (grade_determined < 2 and submission_grade_deep_dive < 3):
                pass
            elif perspective.name.upper() == "GILDE" and grade_determined != int(perspective.progress) and (grade_determined < 2 and submission_grade_verantwoordingsdocument < 3):
                pass
            elif grade_determined != int(perspective.progress) and grade_determined > 0:
                problems.append({"problem": 1,
                                 "teacher": teacher_name,
                                 "message": f"{student.name} {perspective.name.upper()} perspectief, bepaalde beoordeling {grade_determined_label} inconsistent met berekende beoordeling {grade_flow_calculated_label}"})
            else:
                pass
        overall_grade_calculated = get_overall_progress(grade_perspectives)
        overall_grade_determined = student_results.get_grade_moment_submission_by_query(["student", fase]).grade
        if overall_grade_determined is None:
            overall_grade_determined = 0
        overall_grade_determined_label = dashboard.level_serie_collection.level_series[course.grade_moments.levels].grades[str(overall_grade_determined)].label.upper()
        overall_grade_calculated_label = dashboard.level_serie_collection.level_series[course.grade_moments.levels].grades[str(overall_grade_calculated)].label.upper()
        overall_grade_flow_calculated_label = dashboard.level_serie_collection.level_series[course.grade_moments.levels].grades[str(student_results.progress)].label.upper()
        if int(overall_grade_determined) != int(overall_grade_calculated) and int(overall_grade_determined) > 0:
            problems.append({"problem": 2,
                             "teacher": teacher_name,
                             "message": f"FOUT {student.name} OVERALL, bepaalde beoordeling {overall_grade_determined_label} inconsistent met regels voor berekende beoordeling {overall_grade_calculated_label}"})
        elif int(overall_grade_determined) != int(student_results.progress) and int(overall_grade_determined) > 0:
            problems.append({"problem": 3,
                             "teacher": teacher_name,
                             "message": f"{student.name} OVERALL, bepaalde beoordeling {overall_grade_determined_label} inconsistent met de flow_berekende {overall_grade_flow_calculated_label} beoordeling"})
        elif int(overall_grade_calculated) != int(student_results.progress) and int(overall_grade_determined) > 0:
            problems.append({"problem": 4,
                             "teacher": teacher_name,
                             "message": f"{student.name} OVERALL, berekende beoordeling {overall_grade_calculated_label} inconsistent met de flow_berekende {overall_grade_flow_calculated_label} beoordeling"})
        else:
            pass
    problems = sorted(problems, key=lambda s: s["teacher"])
    for item in problems:
        print("Issue:", item["problem"], item["teacher"], item["message"])

    print("GCR98 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # check_level(sys.argv[1], "Sprint 4")
        check_beoordeling("")
    else:
        # check_level("", "Sprint 4")
        check_beoordeling("")
