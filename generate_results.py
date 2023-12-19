# Haalt de studenten en de projecten op. Maakt een JSON waarin de url's naar de daily wordt opgeslagen.
import sys

from canvasapi import Canvas
import json

from lib.file import read_start, read_course, read_progress, read_course_instance
from lib.lib_submission import submission_builder, NO_SUBMISSION, remove_assignment, bepaal_voortgang, count_graded, \
    add_missed_assignments
from model.Comment import Comment
from model.ProgressDay import ProgressDay
from model.Result import *
from lib.lib_date import get_actual_date, API_URL, get_assignment_date, date_to_day
from model.Submission import Submission

def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(start.course_file_name)
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print(user.name)
    canvas_course = canvas.get_course(start.canvas_course_id)

    results = Result(start.canvas_course_id, course.name, g_actual_date, (g_actual_date - start.start_date).days, 0, 0)
    results.students = course.students

    # print("canvas_course.get_assignments(include=['overrides'])")
    canvas_assignments = canvas_course.get_assignments(include=['overrides'])
    for canvas_assignment in canvas_assignments:
        # if "Roll Call" in canvas_assignment.name:
        #     #Roll Call Attendance
        #     continue
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
                            l_perspective = course.find_perspective_by_assignment_group(l_submission.assignment_group_id)
                            if l_perspective:
                                this_perspective = student.perspectives[l_perspective.name]
                                if this_perspective:
                                    this_perspective.submissions.append(l_submission)
                                    results.submission_count += 1
                                    if not l_submission.graded:
                                        results.not_graded_count += 1
            else:
                print("Could not find assignment", canvas_assignment.id, "within group", assignment_group.id)
        else:
            print("Could not find assignment_group with canvas_assignment_group_id", canvas_assignment.assignment_group_id)

    for student in results.students:
        for perspective in student.perspectives.values():
            # Perspective aanvullen met missed Assignments
            add_missed_assignments(start, course, results, perspective)
    for student in results.students:
        for perspective in student.perspectives.values():
            perspective.submissions = sorted(perspective.submissions, key=lambda s: s.submitted_date)

    results.submission_count, results.not_graded_count = count_graded(results)

    with open(start.results_file_name, 'w') as f:
        dict_result = results.to_json([])
        json.dump(dict_result, f, indent=2)

    print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")