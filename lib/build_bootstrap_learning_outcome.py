from lib.lib_date import get_date_time_loc


def build_bootstrap_learning_outcome_tab(instance, course, templates, a_level_serie_collection):
    html_string = ""
    learning_outcomes_html_string = ""
    for learning_outcome in course.learning_outcomes:
        # assignment_html_string = ""
        # assignment_list = []
        # for assignment_sequence in assignment_group.assignment_sequences:
        #     for assignment in assignment_sequence.assignments:
        #         assignment_list.append(assignment)
        # assignment_list = sorted(assignment_list, key=lambda a: a.assignment_day)
        # for assignment in assignment_list:
        file_name = "general/learning_outcome_" + str(learning_outcome.id).lower() + ".html"
        print("BBL41 -", file_name)
        learning_outcomes_html_string += templates["learning_outcome"].substitute(
                {'url': file_name,
                 'learning_outcome_short': learning_outcome.short})
        write_learning_outcome_index(course, templates, learning_outcome, instance.get_html_root_path()+file_name)

    html_string += templates["learning_outcome_card"].substitute({'learning_outcomes': learning_outcomes_html_string})
    return html_string


def write_learning_outcome_index(course, templates, learning_outcome, file_name):
    write_learning_outcome_assignments_html_string = get_learning_outcome_assignments(course, templates, learning_outcome)
    if learning_outcome.min_items is not None:
        up_level = str(learning_outcome.min_items) + " items"
        above_level = str(learning_outcome.above_items) + " items"
    elif learning_outcome.min_score is not None:
        up_level = str(learning_outcome.min_score) + " punten"
        above_level = str(learning_outcome.above_score) + " punten"
    else:
        up_level = "niet bepaald"
        above_level = "niet bepaald"
    write_learning_outcome_index_html_string = templates['learning_outcome_index'].substitute(
        {
            'learning_outcome_short': learning_outcome.short,
            'learning_outcome_description': learning_outcome.description,
            'up_level': up_level,
            'above_level': above_level,
            'assignment_sequences': write_learning_outcome_assignments_html_string
        }
    )

    with open(file_name, mode='w', encoding="utf-8") as file_learning_outcome_index:
        file_learning_outcome_index.write(write_learning_outcome_index_html_string)
    return


def get_learning_outcome_assignments(a_course, a_templates, a_learning_outcome):
    html_string = ""
    portfolio_items = []
    for assignment_sequence_tag in a_learning_outcome.assignment_sequences:
        assignment_sequence = a_course.find_assignment_sequence(assignment_sequence_tag)
        portfolio_items.append({
                'portfolio_item': assignment_sequence.name,
                'tag': assignment_sequence.tag,
                'assignment_date': get_date_time_loc(assignment_sequence.get_date()),
                'assignment_day': assignment_sequence.get_day(),
                'points': assignment_sequence.points,
                'count': len(assignment_sequence.assignments)
            })
    portfolio_items = sorted(portfolio_items, key=lambda a: a['assignment_day'])
    for portfolio_item in portfolio_items:
        html_string += a_templates['learning_outcome_portfolio_item'].substitute(portfolio_item)
    return html_string

