from string import Template


def load_templates(template_path):
    templates = {}
    # Create a template that has placeholder for value of x
    with open(template_path + 'template.html', mode='r', encoding="utf-8") as file_index_template:
        string_index_html = file_index_template.read()
        templates["index"] = Template(string_index_html)

    with open(template_path + 'template_overzicht.html', mode='r', encoding="utf-8") as file_late_template:
        string_late_html = file_late_template.read()
        templates["overzicht"] = Template(string_late_html)

    with open(template_path + 'template_slb.html', mode='r', encoding="utf-8") as file_slb_template:
        string_slb_html = file_slb_template.read()
        templates["slb"] = Template(string_slb_html)

    with open(template_path + 'template_structure_index.html', mode='r', encoding="utf-8") as file_index_template:
        string_index_html = file_index_template.read()
        templates["index_structure"] = Template(string_index_html)

    with open(template_path + 'template_studentgroup.html', mode='r', encoding="utf-8") as file_group_template:
        string_group_html = file_group_template.read()
        templates["group"] = Template(string_group_html)

    with open(template_path + 'template_role_selector.html', mode='r', encoding="utf-8") as file_role_template:
        string_role_html = file_role_template.read()
        templates["role"] = Template(string_role_html)

    with open(template_path + 'template_roles_card.html', mode='r', encoding="utf-8") as file_roles_card_template:
        string_roles_card_html = file_roles_card_template.read()
        templates["roles_card"] = Template(string_roles_card_html)

    with open(template_path + 'template_coaches_card.html', mode='r', encoding="utf-8") as file_coaches_card_template:
        string_coaches_card_html = file_coaches_card_template.read()
        templates["coaches_card"] = Template(string_coaches_card_html)

    with open(template_path + 'template_student.html', mode='r', encoding="utf-8") as file_student_template:
        string_student_html = file_student_template.read()
        templates["student"] = Template(string_student_html)

    with open(template_path + 'template_coach.html', mode='r', encoding="utf-8") as file_coach_template:
        string_coach_html = file_coach_template.read()
        templates["coach"] = Template(string_coach_html)

    with open(template_path + 'template_selector.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["selector"] = Template(string_html)

    with open(template_path + 'template_students_tabs.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["students_tabs"] = Template(string_html)

    with open(template_path + 'template_students_tab.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["students_tab"] = Template(string_html)

    with open(template_path + 'template_overzichten.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["overzichten"] = Template(string_html)

    with open(template_path + 'template_release_planning.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["release_planning"] = Template(string_html)

    with open(template_path + 'template_release_planning_list.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["release_planning_list"] = Template(string_html)

    with open(template_path + 'template_assignment_sequence.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["assignment_sequence"] = Template(string_html)

    with open(template_path + 'template_assignment.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["assignment"] = Template(string_html)

    with open(template_path + 'template_message.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["message"] = Template(string_html)

    with open(template_path + 'template_late.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["late"] = Template(string_html)

    with open(template_path + 'template_late_perspective.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["late_perspective"] = Template(string_html)

    with open(template_path+'template_late_list.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["late_list"] = Template(string_html)

    with open(template_path+'template_submission.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["submission"] = Template(string_html)

    with open(template_path + 'template_grading.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["grading"] = Template(string_html)

    with open(template_path + 'template_explanation.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["explanation"] = Template(string_html)

    with open(template_path + 'template_learning_outcome.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["learning_outcome"] = Template(string_html)

    with open(template_path + 'template_portfolio.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["portfolio"] = Template(string_html)

    with open(template_path + 'template_portfolio_leeg.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["portfolio_leeg"] = Template(string_html)

    with open(template_path + 'template_student_index.html', mode='r', encoding="utf-8") as file_template:
        string_html = file_template.read()
        templates["student_index"] = Template(string_html)

    return templates
