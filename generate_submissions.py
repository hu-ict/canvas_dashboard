# Haalt de studenten en de projecten op. Maakt een JSON waarin de url's naar de daily wordt opgeslagen.
from canvasapi import Canvas
import json

from lib.build_totals import get_actual_progress
from lib.file import read_start, read_course, read_results, read_progress
from lib.lib_submission import submission_builder, NO_SUBMISSION, remove_assignment, get_sum_score
from model.AssignmentDate import AssignmentDate
from lib.lib_date import API_URL, date_to_day, get_assignment_date, get_actual_date
from model.Comment import Comment
from model.ProgressDay import ProgressDay
from model.Submission import Submission


g_actual_date = get_actual_date()
print("read_start()")
start = read_start()
print("read_course(start.course_file_name)")
course = read_course(start.course_file_name)
# Initialize a new Canvas object
canvas = Canvas(API_URL, start.api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course = canvas.get_course(start.course_id)

results = read_results(start.results_file_name)
results.actual_date = g_actual_date
g_actual_day = (results.actual_date - start.start_date).days

# assignments to groups and roles
# print("canvas_course.get_assignments(include=['overrides'])")
canvas_assignments = canvas_course.get_assignments(include=['overrides'])
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
            if (results.actual_date - assignment.assignment_date).days > 10:
                # deadline langer dan twee weken geleden. Alle feedback is gegeven.
                continue
            if assignment.unlock_date:
                if assignment.unlock_date > results.actual_date:
                    if assignment.id != 267540:
                        continue
            if canvas_assignment.overrides:
                for override in canvas_assignment.overrides:
                    assignment_date = get_assignment_date(override.due_at, override.lock_at, start.end_date)
            else:
                assignment_date = get_assignment_date(canvas_assignment.due_at, canvas_assignment.lock_at, start.end_date)

            canvas_submissions = canvas_assignment.get_submissions(include=['submission_comments'])
            for canvas_submission in canvas_submissions:
                student = results.find_student(canvas_submission.user_id)
                if student is not None:
                    # voeg een submission toe aan een van de perspectieven
                    l_submission = submission_builder(student, assignment, canvas_submission, assignment_date)
                    if l_submission is not None:
                        # zoek bij welk perspectief de Submission hoort
                        l_perspective = course.find_perspective_by_assignment_group(l_submission.assignment_group_id)
                        if l_perspective is not None:
                            # haal het student perspectief op
                            this_perspective = student.get_perspective(l_perspective.name)
                            if this_perspective is not None:
                                # voeg de Submission aan het perspectief toe
                                this_perspective.put_submission(l_submission)
                                results.submission_count += 1
                                if not l_submission.graded:
                                    results.not_graded_count += 1

progress_history = read_progress("progress_sep23.json")
progress_day = ProgressDay(g_actual_day)

for student in results.students:
    for perspective in student.perspectives:
        # Perspective aanvullen met missed Assignments
        if len(perspective.assignment_groups) == 1:
            l_assignment_group = course.find_assignment_group(perspective.assignment_groups[0])
            l_assignments = l_assignment_group.assignments[:]

            # remove already submitted
            for l_submission in perspective.submissions:
                l_assignments = remove_assignment(l_assignments, l_submission)
            # open assignments
            for l_assignment in l_assignments:
                if date_to_day(start.start_date, l_assignment.assignment_date) < g_actual_day:
                    l_submission = Submission(0, l_assignment.group_id, l_assignment.id, 0, l_assignment.name,
                                              l_assignment.assignment_date, l_assignment.assignment_date,
                                              True, 0, l_assignment.points)
                    l_submission.comments.append(Comment(0, "Systeem", l_assignment.assignment_date, NO_SUBMISSION))
                    # missed assignment
                    perspective.submissions.append(l_submission)


# bepaal de voortgang
for student in results.students:
    for perspective in student.perspectives:
        perspective.sum_score, perspective.last_score = get_sum_score(perspective, start.start_date)
        if len(perspective.assignment_groups) == 1:
            # bepaal voortgang per perspective
            perspective.progress = course.find_assignment_group(perspective.assignment_groups[0]).bandwidth.get_progress(perspective.last_score, perspective.sum_score)
    # bepaal de totaal voortgang
    progress = get_actual_progress(student.perspectives)
    student.progress = progress
    progress_day.progress[str(progress)] += 1

progress_history.append_day(progress_day)
with open("progress_sep23.json", 'w') as f:
    dict_result = progress_history.to_json()
    json.dump(dict_result, f, indent=2)

with open(start.results_file_name, 'w') as f:
    dict_result = results.to_json([])
    json.dump(dict_result, f, indent=2)

print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")