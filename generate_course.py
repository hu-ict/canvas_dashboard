
import json

from lib.file import read_course_config_start, read_course_config

course_config_start = read_course_config_start()
course_config = read_course_config(course_config_start.config_file_name)
print(course_config)

for teacher in course_config.teachers:
    for studentGroupId in teacher.projects:
        studentGroup = course_config.find_student_group(studentGroupId)
        if studentGroup:
            studentGroup.teachers.append(teacher.id)
    for assignmentGroupId in teacher.assignment_groups:
        assignmentGroup = course_config.find_assignment_group(assignmentGroupId)
        if assignmentGroup:
            assignmentGroup.teachers.append(assignmentGroup.id)

print(course_config)

with open(course_config_start.course_file_name, 'w') as f:
    dict_result = course_config.to_json([])
    json.dump(dict_result, f, indent=2)
