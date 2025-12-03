import json
import sys

from canvasapi import Canvas

import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.datavalidation import DataValidation

from generate_students import get_groups
from lib.file import read_course_instances, read_start, read_config_from_canvas, read_course, read_environment, \
    read_secret_api_key
from lib.lib_date import get_actual_date, API_URL
from model.AssignmentGroup import AssignmentGroup
from model.environment.Environment import ENVIRONMENT_FILE_NAME
from model.environment.SecretApiKey import SECRET_API_KEY_FILE_NAME
from model.teacher.AssignmentGroupNameId import AssignmentGroupNameId
from model.teacher.Responsibility import Responsibility
from model.teacher.ResponsibilityMatrix import ResponsibilityMatrix
from model.teacher.Teacher import Teacher

columns = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def clean_up_responsibilities(teachers):
    for teacher in teachers:
        teacher.responsibilities = []


def read_trm(course_code, instance_name):
    print("GCF01 - generate_config.py")
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    if len(instance_name) > 0:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        with open(ENVIRONMENT_FILE_NAME, 'w') as f:
            dict_result = environment.to_json()
            json.dump(dict_result, f, indent=2)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    print("Instance:", course_instance.name)

    course = read_course(course_instance.get_config_file_name())
    clean_up_responsibilities(course.teachers)

    # Open het Excel-bestand
    wb = load_workbook(course_instance.get_trm_file_name())
    ws = wb["Projects"]
    assignment_groups = {}
    for header in ws[1][1:]:
        assignment_groups[header.column] = header.value
        print("RRM11 -", header.column, header.value)
    for row in ws.iter_rows(min_row=2):
        student_group_name = ""
        for cell in row:
            if cell.column in assignment_groups:
                print("RRM12 -", student_group_name, assignment_groups[cell.column], cell.value)
                assignment_group = course.find_assignment_group_by_name(assignment_groups[cell.column])
                # group = course.find_project_group_by_name(student_group_name)
                teacher = course.find_teacher_by_name(cell.value)
                if teacher:
                    print("RRM13 -", assignment_group)
                    print("RRM14 -", student_group_name)
                    print("RRM15 -", teacher)
                    teacher.put_responsibility("project_groups", student_group_name, assignment_group.id)
            else:
                student_group_name = cell.value
                print("RRM17 - student_group_name", student_group_name)

    ws = wb["Guilds"]
    assignment_groups = {}
    for header in ws[1][1:]:
        assignment_groups[header.column] = header.value
        print("RRM21 -", header.column, header.value)
    for row in ws.iter_rows(min_row=2):
        student_group_name = ""
        for cell in row:
            if cell.column in assignment_groups:
                print("RRM22 -", student_group_name, assignment_groups[cell.column], cell.value)
                assignment_group = course.find_assignment_group_by_name(assignment_groups[cell.column])
                # group = course.find_guild_group_by_name(student_group_name)
                teacher = course.find_teacher_by_name(cell.value)
                if teacher:
                    # print("RRM23 -", assignment_group)
                    # print("RRM24 -", student_group_name)
                    # print("RRM25 -", teacher)
                    teacher.put_responsibility("guild_groups", student_group_name, assignment_group.id)
            else:
                student_group_name = cell.value
                print("RRM27 - group_name", student_group_name)

    # opschonen van teachers zonder "responsibilities"
    for teacher in course.teachers[:]:  # kopie met slicing
        if len(teacher.responsibilities) == 0:
            print("RRM31 - Verwijder teacher", teacher.name)
            course.teachers.remove(teacher)
    print(f"Excel-bestand '{course_instance.get_trm_file_name()}' is succesvol gelezen!")
    print("RRM98 - ConfigFileName:", course_instance.get_config_file_name())
    with open(course_instance.get_config_file_name(), 'w') as f:
        dict_result = course.to_json()
        json.dump(dict_result, f, indent=2)

    print("RRM99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        read_trm(sys.argv[1], sys.argv[1])
    else:
        read_trm("", "")