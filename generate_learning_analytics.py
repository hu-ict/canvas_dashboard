import sys
from canvasapi import Canvas
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_actual_date, API_URL
from lib.file import read_course, read_results, read_course_instance, read_levels, read_levels_from_canvas, read_start


def generate_learning_analytics(instance_name):
    print("GLA01 - generate_learning_analytics.py")
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GLA02 - Instance:", instances.current_instance)
    course = read_course(instances.get_course_file_name(instances.current_instance))
    results = read_results(instances.get_result_file_name(instances.current_instance))
    templates = load_templates(instances.get_template_path())
    # level_serie_collection = read_levels("levels.json")
    start = read_start(instances.get_start_file_name())
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GLA03 - Username", user.name)
    canvas_course = canvas.get_course(course.canvas_id)
    level_serie_collection = read_levels_from_canvas(canvas_course)
    learning_analytics = {}
    for assignment_group in course.assignment_groups:
        perspective = course.find_perspective_by_assignment_group(assignment_group.id)
        grades = level_serie_collection.level_series[perspective.levels].grades
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                grades_dict = {}
                for grade in grades.keys():
                    grades_dict[grade] = 0
                learning_analytics[str(assignment.id)] = {"assignment": assignment.id,
                                                          "assignment_name": assignment.name,
                                                          "level_serie": perspective.levels,
                                                          "status": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
                                                          "grades": grades_dict}

    for student in results.students:
        # print(l_peil_construction)
        print("GLA10 -", student.name)
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    learning_analytics[str(submission.assignment_id)]["status"][str(submission.status)] += 1
                    if submission.grade is not None:
                        learning_analytics[str(submission.assignment_id)]["grades"][str(submission.grade)] += 1
    for assignment in learning_analytics.values():
        print(assignment)
    print("GLA99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_learning_analytics(sys.argv[1])
    else:
        generate_learning_analytics("")
