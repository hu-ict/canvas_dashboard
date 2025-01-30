import csv
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


def read_osiris(file_name):
    print("CO11 - read_osiris", file_name)
    osiris_results = [] #, encoding="utf-8"
    with open(file_name, mode='r') as osiris_results_file:
        dict_reader_obj = csv.DictReader(osiris_results_file, delimiter=";")
        for item in dict_reader_obj:
            # print(item)
            osiris_result = {"number": item["Studentnummer"],
                             "name": item["Naam"],
                             "result": item["Resultaat"]
                             }
            osiris_results.append(osiris_result)
    return osiris_results


def get_student_by_number(osiris_results, number):
    for osiris_result in osiris_results:
        if osiris_result["number"] == number:
            return osiris_result
    return None


def main(instance_name):
    print("CO01 - check_osiris.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name("sep24_inno")
    start = read_start(instance.get_start_file_name())
    course = read_course(instance.get_course_file_name())
    results = read_results(instance.get_result_file_name())
    osiris_results = read_osiris("Osiris-Sep24.csv")
    problems = []
    for student in results.students:
        overall_grade_determined = student.get_grade_moment_submission_by_query(["overall", "Beoordeling"]).grade
        osiris_result = get_student_by_number(osiris_results, student.number)
        if osiris_result is None:
            print("1 Wel Canvas", overall_grade_determined, "niet in Osiris", student.name)

    for student in results.students:
        overall_grade_determined = student.get_grade_moment_submission_by_query(["overall", "Beoordeling"]).grade
        osiris_result = get_student_by_number(osiris_results, student.number)
        if osiris_result is None:
            continue
        # print("Canvas:", overall_grade_determined, "Osiris", osiris_result["result"])
        if overall_grade_determined == "1" and osiris_result["result"] == "NN":
            continue
        elif overall_grade_determined == "2" and osiris_result["result"] == "ON":
            continue
        elif overall_grade_determined == "3" and osiris_result["result"] == "BN":
            continue
        else:
            print("2 Canvas:", overall_grade_determined, "Osiris", osiris_result["result"], osiris_result["name"])

    for osiris_result in osiris_results:
        student = results.find_student_by_number(osiris_result["number"])
        if student is None and osiris_result["result"] != "NA":
            print("3 Canvas:", "niet aanwezig,", "Osiris", osiris_result["result"], osiris_result["name"])

    for osiris_result in osiris_results:
        student = results.find_student_by_number(osiris_result["number"])
        if student is None:
            continue
        else:
            overall_grade_determined = student.get_grade_moment_submission_by_query(["overall", "Beoordeling"]).grade
            if overall_grade_determined == "1" and osiris_result["result"] == "NN":
                continue
            elif overall_grade_determined == "2" and osiris_result["result"] == "ON":
                continue
            elif overall_grade_determined == "3" and osiris_result["result"] == "BN":
                continue
            else:
                print("4 Canvas:", overall_grade_determined, "Osiris", osiris_result["result"], osiris_result["name"])
    # problems = sorted(problems, key=lambda s: s["teacher"])
    # for item in problems:
    #     print("Issue:", item["problem"], item["teacher"], item["message"])

    print("GC99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
