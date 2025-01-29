def build_bootstrap_canvas_werkvoorraad(a_instance, a_templates, a_course, a_perspectives, a_student_totals):
    overzicht_html_string = ""
    dict_index = 0
    for perspective in a_perspectives:
        if dict_index == 0 and a_instance.is_instance_of("prop_courses"):
            list_html_string = ""
            for selector in a_student_totals["perspectives"][perspective.name]["list"].keys():
                # print(selector)
                list_html_string += a_templates["selector"].substitute(
                    {'selector_file': ".//" + a_instance.name + "//general//late_" + selector + ".html", 'selector': selector})
            overzicht_html_string += a_templates["overzicht"].substitute({'perspective': "Totaal", 'buttons': list_html_string})

        list_html_string = ""
        for selector in a_student_totals["perspectives"][perspective.name]["list"].keys():
            # print(selector)
            list_html_string += a_templates["selector"].substitute(
                {'selector_file': ".//" + a_instance.name + "//general//late_" + perspective.name + "_" + selector + ".html", 'selector': selector})
        overzicht_html_string += a_templates["overzicht"].substitute(
            {'perspective': perspective.title, 'buttons': list_html_string})
        dict_index += 1
    return overzicht_html_string


