import json
import sys

import random

from lib.file import read_course_instance, read_course, read_results
from lib.lib_date import get_actual_date

def main(instance_name):

    with open("names.json", mode='r', encoding="utf-8") as file_names:
        names = json.load(file_names)
        lookup = {}
        print(names)
    pointer = 0
    random.shuffle(names)
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GP02 - Instance:", instances.current_instance)
    course = read_course(instances.get_course_file_name(instances.current_instance))
    results = read_results(instances.get_result_file_name(instances.current_instance))
    index = 0
    for student in course.students:
        lookup[student.name] = names[index]
        print(student.name, lookup[student.name])
        index += 1
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
                    for comment in submission.comments:
                        if comment.author_name in lookup:
                            comment.author_name = lookup[comment.author_name]["voornaam"] + " " + lookup[comment.author_name]["achternaam"]

    with open(instances.get_result_file_name(instances.current_instance), 'w') as f:
        dict_result = results.to_json(["perspectives"])
        json.dump(dict_result, f, indent=2)

    with open(instances.get_course_file_name(instances.current_instance), 'w') as f:
        dict_result = course.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)

    print("GC99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    print("GC01 generate_anonymous.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
