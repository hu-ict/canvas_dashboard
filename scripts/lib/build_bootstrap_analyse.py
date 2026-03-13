from scripts.lib.build_bootstrap_structure import process_analyse_moment
from scripts.lib.lib_date import get_date_time_loc


def build_bootstrap_analyse_tab(instance, a_course, a_results, a_templates, a_level_serie_collection):
    html_string = ""
    moments_html_string = ""
    for level_moment in a_course.get_level_moments():

        file_name = instance.name + "/general/analyse1_" + str(level_moment.id) + ".html"
        moments_html_string += a_templates["analyse_moment"].substitute(
            {'url': file_name,
             'assignment_name': level_moment.name,
             'end_date': level_moment.date})
        # process_analyse_level_moment(a_course, a_results, level_moment, a_level_serie_collection, a_templates,
        #                              instance.get_html_index_path() + file_name)
    for grade_moment in a_course.get_grade_moments():
        file_name = instance.name + "/general/analyse_" + str(grade_moment.id) + ".html"
        moments_html_string += a_templates["analyse_moment"].substitute(
            {'url': file_name,
             'assignment_name': grade_moment.name,
             'end_date': get_date_time_loc(grade_moment.date)})
        process_analyse_moment(a_course, a_results, grade_moment, a_level_serie_collection, a_templates,
                                     instance.get_html_index_path() + file_name)

    html_string += a_templates["analyse_card"].substitute({'moments': moments_html_string})
    return html_string
