# Haalt de studenten en de projecten op. Maakt een JSON waarin de url's naar de daily wordt opgeslagen.
from canvasapi import Canvas
import json
from datetime import timezone, datetime

from lib.file import read_course_config, read_course_config_start
from model.AssignmentDate import AssignmentDate
from model.Comment import Comment
from model.Course import *
from lib.config import group_names, not_graded, actual_date, roles, API_URL

total_submissions = 0
total_not_graded = 0

def submissionBuilder(canvas_submission, assignmentDate, course):
    local_comment = ""
    if canvas_submission.score != None:
        if canvas_submission.grade == 'complete':
            # print("Grade", canvas_submission.grade, canvas_submission.score, canvas_submission.assignment_id)
            score = 1.0
        elif canvas_submission.grade == 'incomplete':
            # print("Grade", canvas_submission.grade, canvas_submission.score, canvas_submission.assignment_id)
            score = 0.5
        else:
            score = round(canvas_submission.score, 2)
        graded = 1
    else:
        if not canvas_submission.submitted_at:
            return
        else:
            if not canvas_submission.grader_id:
                score = 0
                graded = 0
                course.statistics.not_graded_count += 1
                local_comment = not_graded
            else:
                graded = 1
                score = 0.0

    if canvas_submission.submitted_at:
        submitted_at = canvas_submission.submitted_at
    else:
        if assignmentDate.lock_at:
            submitted_at = assignmentDate.lock_at
        else:
            if assignmentDate.due_at:
                submitted_at = assignmentDate.due_at
            else:
                submitted_at = "2023-02-06T12:00:00Z"
    course.statistics.submission_count += 1
    submission = Submission(canvas_submission.id, canvas_assignment.assignment_group_id, canvas_assignment.id, canvas_submission.user_id,
                            canvas_assignment.name, submitted_at, graded, score)
    canvas_comments = canvas_submission.submission_comments
    if len(local_comment) > 0:
        submission.comments.append(Comment(0, "System", local_comment))
    for canvas_comment in canvas_comments:
        submission.comments.append(
            Comment(canvas_comment['author_id'], canvas_comment['author_name'], canvas_comment['comment']))
    if group_names[submission.assignment_group_id] == "Peilmomenten":
        course.students[canvas_submission.user_id].peilmomenten[submission.assignment_id] = submission
    elif group_names[submission.assignment_group_id] == "TEAM":
        course.students[canvas_submission.user_id].team[submission.assignment_id] = submission
    elif group_names[submission.assignment_group_id] == "GILDE":
        course.students[canvas_submission.user_id].gilde[submission.assignment_id] = submission
    elif group_names[submission.assignment_group_id] in ["AI", "BIM", "CSC", "SD_B", "SD_F", "TI"]:
        course.students[canvas_submission.user_id].kennis[submission.assignment_id] = submission
    else:
        pass

course_config_start = read_course_config_start()
course_config = read_course_config(course_config_start.config_file_name)

# Initialize a new Canvas object
canvas = Canvas(API_URL, course_config.api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course = canvas.get_course(course_config.course_id)
course = Course(canvas_course.id, canvas_course.name, actual_date.strftime("%A %d-%m-%Y"))
users = canvas_course.get_users(enrollment_type=['student'])
student_count = 0
for user in users:
    student_count += 1
    student = Student(user.id, 0, user.name, 'None')
    course.students[user.id] = student

# ophalen secties en roles
course_sections = canvas_course.get_sections(include=['students'])
for course_section in course_sections:
    print("course_section", course_section)
    course_section_students = course_section.students
    if course_section_students:
        for section_student in course_section_students:
            if roles.get(course_section.name):
                student_id = section_student["id"]
                if course.students.get(student_id):
                    course.students[student_id].roles.append(roles[course_section.name])

canvas_group_categories = canvas_course.get_group_categories()
for canvas_group_category in canvas_group_categories:
    print(canvas_group_category)
    if canvas_group_category.name == "Project Groups":
        canvas_groups = canvas_group_category.get_groups()
        for canvas_group in canvas_groups:
            studentGroup = StudentGroup(canvas_group.id, canvas_group.name, "Leeg")
            course.studentGroups.append(studentGroup)
            print(canvas_group)
            canvas_users = canvas_group.get_users()
            for canvas_user in canvas_users:
                print(canvas_user.name)
                if course.students.get(canvas_user.id):
                    student = course.students[canvas_user.id]
                    student.group_id = studentGroup.id
                    teacher = course_config.find_teacher_by_group(studentGroup.id)
                    if teacher:
                        student.coach_initials = teacher.initials
                    else:
                        student.coach_initials = 'None'
                    studentGroup.students.append(student)

# assignments to groups and roles
canvas_assignments = canvas_course.get_assignments(include=['overrides'])
for canvas_assignment in canvas_assignments:
    if group_names.get(canvas_assignment.assignment_group_id) and canvas_assignment.name != "Roll Call Attendance":
        if canvas_assignment.points_possible:
            points = canvas_assignment.points_possible
        else:
            points = 0

        group_name = group_names.get(canvas_assignment.assignment_group_id)
        #print("GroupName", group_name, canvas_assignment)
        print("Processing {0:8} - {1}".format(group_name, canvas_assignment.name))
        if canvas_assignment.overrides:
            for override in canvas_assignment.overrides:
                assignment_date = AssignmentDate(override.id, override.due_at, override.lock_at)
                canvas_submissions = canvas_assignment.get_submissions(include=['submission_comments'])
                for canvas_submission in canvas_submissions:
                    #print("override C", canvas_submission)
                    if course.students.get(canvas_submission.user_id):
                        submissionBuilder(canvas_submission, assignment_date, course)
        else:
            canvas_submissions = canvas_assignment.get_submissions(include=['submission_comments'])
            assignment_date = AssignmentDate(canvas_assignment.id, canvas_assignment.due_at, canvas_assignment.lock_at)
            for canvas_submission in canvas_submissions:
                if course.students.get(canvas_submission.user_id):
                    submissionBuilder(canvas_submission, assignment_date, course)

def get_submitted_at(item):
    return item[1].submitted_at

for student in course.students.values():
    # sort list by `name` in the natural order
    student.team = dict(sorted(student.team.items(), key=get_submitted_at))
    student.gilde = dict(sorted(student.gilde.items(), key=get_submitted_at))
    student.kennis = dict(sorted(student.kennis.items(), key=get_submitted_at))
    print(student.name, student.roles)

with open("student_results.json", 'w') as f:
    dict_result = course.to_json(['assignment'])
    json.dump(dict_result, f, indent=2)
