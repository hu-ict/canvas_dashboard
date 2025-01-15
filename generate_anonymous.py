import json
import sys

import random

from lib.file import read_course_instances, read_course, read_results
from lib.lib_date import get_actual_date

def main(instance_name):

    with open("names.json", mode='r', encoding="utf-8") as file_names:
        names = json.load(file_names)
        lookup = {}
        print(names)
    pointer = 0
    random.shuffle(names)
    g_actual_date = get_actual_date()


    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("GAN02 - Instance:", instance.name)
    course = read_course(instance.get_course_file_name())
    results = read_results(instance.get_result_file_name())
    index = 0
    for student in course.students:
        lookup[student.name] = names[index]
        print(student.name, lookup[student.name])
        index += 1
    for teacher in course.teachers:
        lookup[teacher.name] = names[index]
        print(teacher.name, lookup[teacher.name])
        index += 1
    for teacher in course.teachers:
        alias = lookup[teacher.name]["voornaam"] + " " + lookup[teacher.name]["achternaam"]
        teacher.name = alias
        teacher.initials = ''.join([x[0].upper() for x in alias.split(' ')])
        teacher.email = alias.lower().replace(" ", ".")+"@hu.nl"
    for student in course.students:
        alias = lookup[student.name]["voornaam"] + " " + lookup[student.name]["achternaam"]
        sortable = lookup[student.name]["achternaam"] + ", " + lookup[student.name]["voornaam"]
        student.name = alias
        student.sortable_name = sortable
        student.email = alias.lower().replace(" ", ".")+"@student.hu.nl"
    for group in course.student_groups:
        for student in group.students:
            alias = lookup[student.name]["voornaam"] + " " + lookup[student.name]["achternaam"]
            sortable = lookup[student.name]["achternaam"] + ", " + lookup[student.name]["voornaam"]
            student.name = alias
            student.sortable_name = sortable
    for role in course.role_groups:
        for student in role.students:
            alias = lookup[student.name]["voornaam"] + " " + lookup[student.name]["achternaam"]
            sortable = lookup[student.name]["achternaam"] + ", " + lookup[student.name]["voornaam"]
            student.name = alias
            student.sortable_name = sortable
    for student in results.students:
        alias = lookup[student.name]["voornaam"] + " " + lookup[student.name]["achternaam"]
        sortable = lookup[student.name]["achternaam"] + ", " + lookup[student.name]["voornaam"]
        student.name = alias
        student.sortable_name = sortable
        student.email = alias.lower().replace(" ", ".")+"@student.hu.nl"
        for student_perspective in student.perspectives.values():
            for submission_sequence in student_perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    if submission.grader_name is not None and submission.grader_name != 0:
                        if submission.grader_name in lookup:
                            submission.grader_name = lookup[submission.grader_name]["voornaam"] + " " + lookup[submission.grader_name]["achternaam"]
                        else:
                            print("GAN51 - Not found", submission.grader_name)
                    for comment in submission.comments:
                        if comment.author_name in lookup:
                            comment.author_name = lookup[comment.author_name]["voornaam"] + " " + lookup[comment.author_name]["achternaam"]
                        else:
                            # print("GAN52 - Not found", comment.author_name)
                            pass
        for submission in student.student_level_moments.submissions:
            if submission.grader_name is not None and submission.grader_name != 0:
                if submission.grader_name in lookup:
                    submission.grader_name = lookup[submission.grader_name]["voornaam"] + " " + lookup[submission.grader_name]["achternaam"]
            for comment in submission.comments:
                if comment.author_name in lookup:
                    comment.author_name = lookup[comment.author_name]["voornaam"] + " " + lookup[comment.author_name]["achternaam"]

        for submission in student.student_grade_moments.submissions:
            if submission.grader_name is not None and submission.grader_name != 0:
                if submission.grader_name in lookup:
                    submission.grader_name = lookup[submission.grader_name]["voornaam"] + " " + lookup[submission.grader_name]["achternaam"]
            for comment in submission.comments:
                if comment.author_name in lookup:
                    comment.author_name = lookup[comment.author_name]["voornaam"] + " " + lookup[comment.author_name]["achternaam"]

    result_file_name = instance.get_result_file_name()
    with open(result_file_name, 'w') as f:
        dict_result = results.to_json()
        json.dump(dict_result, f, indent=2)

    course_file_name = instance.get_course_file_name()
    with open(course_file_name, 'w') as f:
        dict_result = course.to_json()
        json.dump(dict_result, f, indent=2)

    print("GAN99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    print("GC01 generate_anonymous.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
