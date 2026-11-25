def build_bootstrap_speedgrader(course, student_results, templates):
    student_speedgrader_html_string = ""
    for perspective in course.perspectives.values():
        for assignment_group_id in perspective.assignment_group_ids:
            assignment_group = course.get_assignment_group(assignment_group_id)
            for assignment_sequence in assignment_group.assignment_sequences:
                for assignment in assignment_sequence.assignments:
                    speedgrader_url = "https://canvas.hu.nl/courses/" + str(course.canvas_id) + "/gradebook/speed_grader?assignment_id=" + str(assignment.id) + "&student_id=" + str(student_results.id)

                    student_speedgrader_html_string += templates['canvas_line'].substitute(
                    {
                        'assignment_name': assignment.name,
                        'speedgrader_url': speedgrader_url,
                        'observation_count': 0,
                        'date': assignment.date
                    })

    student_canvas_html_string = templates['canvas'].substitute(
        {
            'canvas_lines': student_speedgrader_html_string
        })
    return student_canvas_html_string





