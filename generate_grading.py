import sys

from lib.file import read_course_instance, read_start, read_course, read_results, read_levels
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_actual_date, get_date_time_loc
from lib.translation_table import translation_table


def build_bootstrap_grading(a_instances, a_start, a_course, a_results, a_templates, a_levels):
    if not a_instances.is_instance_of('inno_courses'):
        return
    for student in a_results.students:
        level_moment = student.get_peilmoment_submission_by_query(["overall","beoordeling"])
        if level_moment is None:
            continue
        print(level_moment)
        if not level_moment.graded:
            continue
        l_grader_name = level_moment.grader_name
        l_grade_overall = a_levels.level_series[a_start.grade_levels].levels[str(int(level_moment.score))].label
        role = a_course.get_role(student.role)
        l_explanation = ""
        for comment in level_moment.comments:
            if len(l_explanation) > 0:
                l_explanation += "<br>"+comment.comment
            else:
                l_explanation += comment.comment

        explanations_html_string = a_templates['explanation'].substitute(
                {'perspective': 'overall',
                'grade': l_grade_overall,
                'grade_date': get_date_time_loc(level_moment.graded_date),
                'examiner': level_moment.grader_name,
                'explanation': l_explanation})
        examiners = "("
        for perspective in student.perspectives:
            level_moment = student.get_peilmoment_submission_by_query(["beoordeling", perspective])
            if level_moment is None:
                continue
            l_grade = a_levels.level_series[a_start.grade_levels].levels[str(int(level_moment.score))].label
            l_explanation = ""
            for comment in level_moment.comments:
                if len(l_explanation) > 0:
                    l_explanation += "<br>" + comment.comment
                else:
                    l_explanation += comment.comment
            explanations_html_string += a_templates['explanation'].substitute(
                {'perspective': perspective,
                'grade': l_grade,
                'grade_date': get_date_time_loc(level_moment.graded_date),
                'examiner': level_moment.grader_name,
                'explanation': l_explanation})

            if level_moment is not None:
                if len(examiners) > 1:
                    examiners += ", "+level_moment.grader_name
                else:
                    examiners += level_moment.grader_name
        examiners += ")"

        grading_html_string = a_templates['grading'].substitute(
            {'major': role.major,
             'semester': a_course.name,
             'role_name': role.name,
             'student_name': student.name,
             'student_number': student.id,
             'grade': l_grade_overall,
             'grade_date': get_date_time_loc(level_moment.graded_date),
             'examiners': l_grader_name + " " + examiners,
             'explanations': explanations_html_string})
        file_name = a_instances.get_plot_path() + student.name + " grading"

        asci_file_name = file_name.translate(translation_table)
        print("GG11 - Write grade for", student.name)
        with open(asci_file_name + ".html", mode='w', encoding="utf-8") as file_grade:
            file_grade.write(grading_html_string)

def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GD02 - Instance:", instances.current_instance, instances.get_category(instances.current_instance))
    start = read_start(instances.get_start_file_name())
    course = read_course(instances.get_course_file_name(instances.current_instance))
    results = read_results(instances.get_result_file_name(instances.current_instance))
    templates = load_templates(instances.get_template_path())
    level_series = read_levels("levels.json")

    # team_coaches = init_coaches_dict(course)
    # for team_coach in team_coaches.values():
    #     print("GD04 -", team_coach["teacher"])

    build_bootstrap_grading(instances, start, course, results, templates, level_series)
    print("GD99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GG01 - generate_grading.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
