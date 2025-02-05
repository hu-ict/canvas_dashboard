import sys
import json

from canvasapi import Canvas

from lib.file import read_start, read_course, read_progress, read_results, read_course_instances, \
    read_levels_from_canvas
from lib.lib_date import get_actual_date, API_URL
from lib.lib_progress import get_overall_progress
from model.ProgressDay import ProgressDay
from model.perspective.Perspectives import Perspectives
from model.perspective.StudentPerspective import StudentPerspective
from model.perspective.StudentPerspectives import StudentPerspectives


def main(instance_name):
    print("GD01 - generate_check_and_results.py")
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
    level_serie_collection = read_levels_from_canvas(canvas_course)
    problems = []
    for student in results.students:
        teacher = course.find_teacher(student.coach)
        # print(student.name, student.get_judgement("overall"))
        perspectives = StudentPerspectives()
        grade_perspectives = []
        for perspective in student.perspectives.values():
            # print(perspective.name, "eind", student.get_judgement(perspective.name), "calc", perspective.progress)

            perspectives.perspectives[perspective.name] = StudentPerspective(perspective.name,
                                                                             student.get_grade_moment_submission_by_query(
                                                                                 [perspective.name, "Beoordeling"]), 0,
                                                                             0, 0)
            grade_determined = int(student.get_grade_moment_submission_by_query(perspective.name).grade)
            grade_perspectives.append(grade_determined)
            if grade_determined is None:
                grade_determined = 0
            grade_determined_label = level_serie_collection.level_series[course.grade_moments.levels].grades[str(grade_determined)].label.upper()
            grade_flow_calculated_label = level_serie_collection.level_series[course.grade_moments.levels].grades[str(perspective.progress)].label.upper()

            if grade_determined != int(perspective.progress):
                problems.append({"problem": 1,
                                 "teacher": teacher.name,
                                 "message": f"{student.name} {perspective.name.upper()} perspectief, bepaalde beoordeling {grade_determined_label} inconsistent met berekende beoordeling {grade_flow_calculated_label}"})

        overall_grade_calculated = get_overall_progress(grade_perspectives)
        overall_grade_determined = student.get_grade_moment_submission_by_query(["overall", "Beoordeling"]).grade
        if overall_grade_determined is None:
            overall_grade_determined = 0
        overall_grade_determined_label = level_serie_collection.level_series[course.grade_moments.levels].grades[str(overall_grade_determined)].label.upper()
        overall_grade_calculated_label = level_serie_collection.level_series[course.grade_moments.levels].grades[str(overall_grade_calculated)].label.upper()
        overall_grade_flow_calculated_label = level_serie_collection.level_series[course.grade_moments.levels].grades[str(student.progress)].label.upper()
        if teacher is None:
            teacher_name = "Berend Wilkens"
        else:
            teacher_name = teacher.name
        if int(overall_grade_determined) != int(overall_grade_calculated):
            problems.append({"problem": 3,
                             "teacher": teacher_name,
                             "message": f"FOUT {student.name} OVERALL, bepaalde beoordeling {overall_grade_determined_label} inconsistent met regels voor berekende beoordeling {overall_grade_calculated_label}"})
        elif int(overall_grade_determined) != int(student.progress):
            problems.append({"problem": 2,
                             "teacher": teacher_name,
                             "message": f"{student.name} OVERALL, bepaalde beoordeling {overall_grade_determined_label} inconsistent met de flow_berekende {overall_grade_flow_calculated_label} beoordeling"})
        elif int(overall_grade_calculated) != int(student.progress):
            problems.append({"problem": 4,
                             "teacher": teacher_name,
                             "message": f"{student.name} OVERALL, berekende beoordeling {overall_grade_calculated_label} inconsistent met de flow_berekende {overall_grade_flow_calculated_label} beoordeling"})
        else:
            pass
    problems = sorted(problems, key=lambda s: s["teacher"])
    for item in problems:
        if item["problem"] == 3:
            print("Issue:", item["problem"], item["teacher"], item["message"])

    print("GC99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
