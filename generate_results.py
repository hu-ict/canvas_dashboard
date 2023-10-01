# Haalt de studenten en de projecten op. Maakt een JSON waarin de url's naar de daily wordt opgeslagen.
from canvasapi import Canvas
import json
from lib.file import read_start, read_course
from model.AssignmentDate import AssignmentDate
from model.Comment import Comment
from model.Result import *
from lib.config import actual_date, API_URL, NOT_GRADED, get_assignment_date
from model.Submission import Submission


def get_submitted_at(item):
    return item[1].submitted_at


def submission_builder(a_student, a_assignment, a_canvas_submission, a_assignment_date):
    if a_canvas_submission.score:
        if a_canvas_submission.grade.isnumeric():
            score = float(a_canvas_submission.grade)
        elif a_canvas_submission.grade == 'complete':
            score = 1.0
        elif a_canvas_submission.grade == 'incomplete':
            score = 0.5
        else:
            score = round(a_canvas_submission.score, 2)
        graded = True
    else:
        score = 0
        if a_canvas_submission.grader_id:
            graded = True
        else:
            graded = False
    if a_canvas_submission.submitted_at:
        submitted_at = get_date_time_obj(a_canvas_submission.submitted_at)
    else:
        submitted_at = None
    # maak een submission en voeg de commentaren toe
    canvas_comments = a_canvas_submission.submission_comments
    if not a_canvas_submission.submitted_at and len(canvas_comments) == 0:
        return None
    else:
        l_submission = Submission(a_canvas_submission.id, a_assignment.group_id, a_assignment.id, a_student.id,
                                  a_assignment.name, a_assignment_date, submitted_at, graded, score,
                                  a_assignment.points)
        for canvas_comment in canvas_comments:
            l_submission.comments.append(
                    Comment(canvas_comment['author_id'], canvas_comment['author_name'],
                    get_date_time_obj(canvas_comment['created_at']), canvas_comment['comment']))
        if not submitted_at:
            l_submission.submitted_at = l_submission.comments[0].date
        return l_submission


course_config_start = read_start()
course = read_course(course_config_start.course_file_name)
# Initialize a new Canvas object
canvas = Canvas(API_URL, course_config_start.api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course = canvas.get_course(course_config_start.course_id)
# print("Course(canvas_course.id, canvas_course.name, actual_date)")
results = Result(canvas_course.id, canvas_course.name, actual_date, 0, 0)
# kopieer de groepen en studenten vanuit de configuratie
# print("course.studentGroups")
results.students = course.students

# assignments to groups and roles
# print("canvas_course.get_assignments(include=['overrides'])")
canvas_assignments = canvas_course.get_assignments(include=['overrides'])
# print("for canvas_assignment in canvas_assignments")
for canvas_assignment in canvas_assignments:
    if canvas_assignment.id == "273700":
        #Roll Call Attendance
        break
    assignment_group = course.find_assignment_group(canvas_assignment.assignment_group_id)
    if assignment_group is not None:
        # print("Processing G {0:8} - {1}".format(assignment_group.id, assignment_group.name))
        assignment = course.find_assignment_by_group(assignment_group.id, canvas_assignment.id)
        if assignment is not None:
            print("Processing Assignment {0:6} - {1} {2}".format(assignment.id, assignment_group.name, assignment.name))
            if assignment.unlock_date:
                if assignment.unlock_date > results.actual_date:
                    if assignment.id != 267540:
                        continue
            if canvas_assignment.overrides:
                for override in canvas_assignment.overrides:
                    assignment_date = get_assignment_date(override.due_at, override.lock_at, course_config_start.end_date)
            else:
                assignment_date = get_assignment_date(canvas_assignment.due_at, canvas_assignment.lock_at, course_config_start.end_date)

            canvas_submissions = canvas_assignment.get_submissions(include=['submission_comments'])
            for canvas_submission in canvas_submissions:
                student = results.find_student(canvas_submission.user_id)
                if student is not None:
                    # voeg een submission toe aan een van de perspectieven
                    l_submission = submission_builder(student, assignment, canvas_submission, assignment_date)
                    if l_submission is not None:
                        l_perspective = course.find_perspective_by_assignment_group(l_submission.assignment_group_id)
                        if l_perspective:
                            this_perspective = student.get_perspective(l_perspective.name)
                            if this_perspective:
                                this_perspective.submissions.append(l_submission)
                                results.submission_count += 1
                                if not l_submission.graded:
                                    results.not_graded_count += 1

# for group in results.studentGroups:
#     for student in group.students:
#         for perspective in student.perspectives:
#             perspective.submissions = sorted(perspective.submissions, key=lambda s: s.submitted_at)

with open(course_config_start.results_file_name, 'w') as f:
    dict_result = results.to_json([])
    json.dump(dict_result, f, indent=2)
