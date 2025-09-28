from lib.build_plotly_bandwidth import process_bandwidth
from lib.file import read_plotly
from lib.lib_date import get_date_time_loc


def write_release_planning_index(course, templates, assignment_group_id, file_name, file_name_bandwidth):
    assignment_group = course.get_assignment_group(assignment_group_id)
    bandwith_html_string = '<h2 class="mt-2">Opbouw</h2>' + read_plotly(file_name_bandwidth)
    release_planning_html_string = write_release_planning(course, templates, assignment_group_id)
    release_planning_index_html_string = templates['release_planning_index'].substitute(
        {
            'assignment_group_name': assignment_group.name,
            'assignment_group_id': assignment_group.id,
            'total_points': int(assignment_group.total_points),
            'lower_points': assignment_group.lower_points,
            'upper_points': assignment_group.upper_points,
            'strategie': assignment_group.strategy,
            'planning': release_planning_html_string,
            'flow': bandwith_html_string
        }
    )

    with open(file_name, mode='w', encoding="utf-8") as file_release_planning_index:
        file_release_planning_index.write(release_planning_index_html_string)
    return



def write_release_planning_oud(a_start, a_templates, a_assignment_group, a_file_name):
    list_html_string = ""
    for assignment in a_assignment_group.assignments:
        url = "https://canvas.hu.nl/courses/" + str(a_start.canvas_course_id) + "/assignments/" + str(assignment.id)
        # print(assignment.name)
        rubric_points = 0
        rubric_count = 0
        for criterion in assignment.rubrics:
            rubric_points += criterion.points
            rubric_count += 1
        if rubric_count == 0:
            rubrics_str = "Geen criteria"
        else:
            rubrics_str = str(int(rubric_points)) + " [" + str(rubric_count) + "]"
        list_html_string += a_templates["assignment"].substitute({'assignment_name': assignment.name,
                                                                  'assignment_unlock_date': get_date_time_loc(
                                                                      assignment.unlock_date),
                                                                  'assignment_lock_date': get_date_time_loc(
                                                                      assignment.assignment_date),
                                                                  'assignment_grading_type': assignment.grading_type,
                                                                  'assignment_points': assignment.points,
                                                                  'rubrics_points': rubrics_str,
                                                                  'url': url})
    file_html_string = a_templates["release_planning_list"].substitute(
        {'total_points': int(a_assignment_group.total_points), 'lower_points': a_assignment_group.lower_points,
         'upper_points': a_assignment_group.upper_points, 'strategie': a_assignment_group.strategy,
         'assignments': list_html_string})

    with open(a_file_name, mode='w', encoding="utf-8") as file_list:
        file_list.write(file_html_string)


def write_release_planning(a_course, a_templates, a_assignment_group_id):
    list_html_string = ""
    assignment_group = a_course.get_assignment_group(a_assignment_group_id)
    for assignment_sequence in assignment_group.assignment_sequences:
        messages_html_string = ""
        assignment_sequence_html_string = ""
        # print(assignment_sequence.name)
        for assignment in assignment_sequence.assignments:
            url = "https://canvas.hu.nl/courses/" + str(a_course.canvas_id) + "/assignments/" + str(assignment.id)
            rubric_points = 0
            rubric_count = 0
            rubrics_html_string = '<table class="table-sm">'
            for criterion in assignment.rubrics:
                rubrics_html_string += "<tr><td>" + str(round(criterion.points, 2)) + " ptn, " + criterion.description + "</td>"
                rubric_points += criterion.points
                rubric_count += 1
                rubrics_html_string += "<td>"
                for rating in criterion.ratings:
                    rubrics_html_string += rating.description + ": " + str(round(rating.points, 2)) + " ptn, "
                rubrics_html_string += "</td></tr>"
            rubrics_html_string += "</table>"
            if rubric_count == 0:
                rubrics_str = str(round(0, 2))
                rubrics_html_string = "Geen criteria"
            else:
                rubrics_str = str(round(rubric_points, 2))
            if len(assignment.sections) > 0:
                sections_html_string = ""
                for section_id in assignment.sections:
                    section = a_course.find_section(section_id)
                    if section is None:
                        sections_html_string += str(section_id)+", "
                    else:
                        role = a_course.get_role(section.role)
                        sections_html_string += section.name+" ("+role.name+"), "
            else:
                sections_html_string = "Geen specifieke secties"

            assignment_sequence_html_string += a_templates["assignment"].substitute({'assignment_name': assignment.name,
                                                                                     'assignment_unlock_date': get_date_time_loc(
                                                                                         assignment.unlock_date),
                                                                                     'assignment_lock_date': get_date_time_loc(
                                                                                         assignment.assignment_date),
                                                                                     'assignment_grading_type': assignment.grading_type,
                                                                                     'assignment_points': assignment.points,
                                                                                     'rubrics_points': rubrics_str,
                                                                                     'rubrics': rubrics_html_string,
                                                                                     'sections': sections_html_string,
                                                                                     'url': url})

            for message in assignment.messages:
                messages_html_string += a_templates["message"].substitute({'message': message})

        list_html_string += a_templates["assignment_sequence"].substitute({'assignment_name': assignment_sequence.name,
                                                                           'assignment_tag': assignment_sequence.tag,
                                                                           'assignment_grading_type': assignment_sequence.grading_type,
                                                                           'assignment_points': assignment_sequence.points,
                                                                           'messages': messages_html_string,
                                                                           'assignments': assignment_sequence_html_string})
    release_planning_html_string = a_templates["release_planning_list"].substitute(
        {'assignment_group': assignment_group.name + " " + str(assignment_group.id),
         'total_points': int(assignment_group.total_points), 'lower_points': "a_perspective.lower_points",
         'upper_points': "a_perspective.upper_points", 'strategie': "a_perspective.strategy",
         'assignments': list_html_string})
    return release_planning_html_string


def get_assignment_group_release_planning(instance, assignment_group, templates):
    file_name_levels = ".//" + instance.name + "//general//level_serie_" + str(assignment_group.levels) + ".html"
    file_name_release_planning = ".//" + instance.name + "//general//release_planning_" + str(assignment_group.id) + ".html"
    # print("BBS31 -", file_name_group)

    return templates["release_planning_perspective"].substitute(
        {'url_levels': file_name_levels,
         'url_group': file_name_release_planning,
         'levels': assignment_group.levels,
         'assignment_group_name': assignment_group.name})


def write_level_serie(a_course, a_templates, level_serie, a_file_name):
    status_list_html_string = ""
    for status_id in level_serie.status:
        level = level_serie.status[status_id]
        status_list_html_string += a_templates["level_status"].substitute(
            {'id': status_id,
             'label': level.label,
             'color': level.color})
    value_list_html_string = ""
    for grade_id in level_serie.grades:
        grades = level_serie.grades[grade_id]
        value_list_html_string += a_templates["level_level"].substitute(
            {'id': grade_id,
             'label': grades.label,
             'color': grades.color,
             'fraction': grades.fraction,
             'value': grades.value})
    file_html_string = a_templates["level_serie_index"].substitute(
        {'level_serie_name': level_serie.name,
         'status_list': status_list_html_string,
         'value_list': value_list_html_string})
    with open(a_file_name, mode='w', encoding="utf-8") as file_list:
        file_list.write(file_html_string)


def build_bootstrap_release_planning_tab(a_instance, a_course, a_templates, level_serie_collection):
    # genereer de bestanden voor in de IFrame
    html_string = ""
    for level_serie in level_serie_collection.level_series.values():
        file_name = a_instance.get_html_path() + "level_serie_" + str(level_serie.name) + ".html"
        write_level_serie(a_course, a_templates, level_serie, file_name)
    for perspective in a_course.perspectives.values():
        for assignment_group_id in perspective.assignment_group_ids:
            file_name_bandwidth = a_instance.get_temp_path() + "bandwidth_" + str(assignment_group_id) + ".html"
            process_bandwidth(a_course, assignment_group_id, level_serie_collection, file_name_bandwidth)
    for perspective in a_course.perspectives.values():
        for assignment_group_id in perspective.assignment_group_ids:
            file_name_bandwidth = a_instance.get_temp_path() + "bandwidth_" + str(assignment_group_id) + ".html"
            file_name_release_planning = a_instance.get_html_path() + "release_planning_" + str(assignment_group_id) + ".html"
            write_release_planning_index(a_course, a_templates, assignment_group_id, file_name_release_planning, file_name_bandwidth)

    assignment_group_html_string = ""
    # voor elk perspectief een card
    for perspective in a_course.perspectives.values():
        for assignment_group_id in perspective.assignment_group_ids:
            assignment_group = a_course.get_assignment_group(assignment_group_id)
            assignment_group_html_string += get_assignment_group_release_planning(a_instance, assignment_group, a_templates)
        html_string += a_templates["release_planning"].substitute({'perspective': perspective.name, 'assignment_groups': assignment_group_html_string})

    # de peil en beoordelingen krijgen een eigen card
    perspectives_html_string = ""
    if a_course.level_moments is not None:
        for assignment_group_id in a_course.level_moments.assignment_group_ids:
            assignment_group = a_course.get_assignment_group(assignment_group_id)
            perspectives_html_string += get_assignment_group_release_planning(a_instance, assignment_group, a_templates)
    if a_course.grade_moments is not None:
        for assignment_group_id in a_course.grade_moments.assignment_group_ids:
            assignment_group = a_course.get_assignment_group(assignment_group_id)
            perspectives_html_string += get_assignment_group_release_planning(a_instance, assignment_group, a_templates)
    html_string += a_templates["release_planning"].substitute({'perspective': "peil en beoordelingen", 'assignment_groups': perspectives_html_string})
    return html_string

