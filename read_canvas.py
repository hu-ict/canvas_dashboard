# Haalt de studenten en de projecten op. Maakt een JSON waarin de url's naar de daily wordt opgeslagen.
from canvasapi import Canvas
import json
from lib.file import read_course_config, read_course_config_start
from model.AssignmentDate import AssignmentDate
from model.Comment import Comment
from model.Course import *
from lib.config import not_graded, actual_date, API_URL

course_config_start = read_course_config_start()
course_config = read_course_config(course_config_start.course_file_name)

def submissionBuilder(student, assignment, canvas_submission, assignmentDate):
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
                # course.statistics.not_graded_count += 1
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
    # course.statistics.submission_count += 1
    submission = Submission(canvas_submission.id, assignment.group_id, assignment.id, student.id,
                            assignment.name, submitted_at, graded, score)
    canvas_comments = canvas_submission.submission_comments
    if len(local_comment) > 0:
        submission.comments.append(Comment(0, "System", local_comment))
    for canvas_comment in canvas_comments:
        submission.comments.append(
            Comment(canvas_comment['author_id'], canvas_comment['author_name'], canvas_comment['comment']))
    l_perspective = course_config.find_perspective_by_assignment_group(submission.assignment_group_id)
    if l_perspective:
        this_perspective = student.get_perspective(l_perspective.name)
        if this_perspective:
            this_perspective.submissions.append(submission)

# Initialize a new Canvas object
canvas = Canvas(API_URL, course_config_start.api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course = canvas.get_course(course_config_start.course_id)
course = Course(canvas_course.id, canvas_course.name, actual_date.strftime("%A %d-%m-%Y"))
# kopieer de groepen en studenten vanuit de configuratie
course.studentGroups = course_config.studentGroups

# assignments to groups and roles
canvas_assignments = canvas_course.get_assignments(include=['overrides'])
for canvas_assignment in canvas_assignments:
    assignment_group = course_config.find_assignment_group(canvas_assignment.assignment_group_id)
    if assignment_group:
        # print("Processing G {0:8} - {1}".format(assignment_group.id, assignment_group.name))
        assignment = course_config.find_assignment(assignment_group.id, canvas_assignment.id)
        if assignment:
            print("Processing Assignment {0:6} - {1} {2}".format(assignment.id, assignment_group.name, assignment.name))
            if canvas_assignment.overrides:
                for override in canvas_assignment.overrides:
                    assignment_date = AssignmentDate(override.id, override.due_at, override.lock_at)
            else:
                assignment_date = AssignmentDate(canvas_assignment.id, canvas_assignment.due_at, canvas_assignment.lock_at)
            canvas_submissions = canvas_assignment.get_submissions(include=['submission_comments'])
            for canvas_submission in canvas_submissions:
                student = course.find_student(canvas_submission.user_id)
                if student:
                    submissionBuilder(student, assignment, canvas_submission, assignment_date)


def get_submitted_at(item):
    return item[1].submitted_at

for group in course.studentGroups:
    for student in group.students:
        for perspective in student.perspectives:
            perspective = sorted(perspective.submissions, key=lambda s: s.submitted_at)

with open(course_config_start.results_file_name, 'w') as f:
    dict_result = course.to_json(['assignment'])
    json.dump(dict_result, f, indent=2)
