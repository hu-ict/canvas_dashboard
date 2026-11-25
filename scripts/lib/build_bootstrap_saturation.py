from scripts.lib.file import read_plotly
from scripts.lib.lib_date import get_date_time_loc
from scripts.lib.plot_totals import SATURATION_PLOTLY_HTML


def build_bootstrap_saturation_tab(instance, course, templates, level_serie_collection):
    html_string = ""
    saturation_html_string = ""
    for learning_outcome in course.learning_outcomes:
        file_name = "saturation_" + str(learning_outcome.id).lower() + ".html"
        link_path_name = instance.get_link_general_path() + file_name
        # print("BBL51 -", file_name)
        saturation_html_string += templates["learning_outcome"].substitute(
                {'url': link_path_name,
                 'learning_outcome_short': learning_outcome.short})
        write_saturation_index(instance, course, templates, learning_outcome, instance.get_html_general_path()+file_name)
    html_string += templates["learning_outcome_card"].substitute({'learning_outcomes': saturation_html_string})
    list_html_string = ""
    course.teachers = sorted(course.teachers, key=lambda t: t.initials)
    for teacher in course.teachers:
        item_file_name = "teacher_saturation_" + teacher.initials + ".html"
        link_path_name = instance.get_link_general_path() + item_file_name
        list_html_string += templates["selector"].substitute(
            {'selector_file': link_path_name, 'selector_name': teacher.name, 'selector': teacher.initials})
    html_string += templates["overzicht"].substitute(
        {'url': instance.get_link_general_path() + SATURATION_PLOTLY_HTML, 'title': 'Docent saturatie', 'buttons': list_html_string})

    return html_string


def write_saturation_index(instance, course, templates, learning_outcome, file_name):
    file_name_html = instance.get_temp_path() + "distribution_" + learning_outcome.id + ".html"
    distribution_plot_html = read_plotly(file_name_html)
    file_name_html = instance.get_temp_path() + "saturation_" + learning_outcome.id + ".html"
    saturation_plot_html = read_plotly(file_name_html)
    write_saturation_index_html_string = templates['saturation_index'].substitute(
        {
            'learning_outcome_short': learning_outcome.short,
            'distribution_plot': distribution_plot_html,
            'saturation_plot': saturation_plot_html
        }
    )
    with open(file_name, mode='w', encoding="utf-8") as file_learning_outcome_index:
        file_learning_outcome_index.write(write_saturation_index_html_string)
    return
