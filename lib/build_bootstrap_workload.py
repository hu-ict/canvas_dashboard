def build_workload_overtime(course, total_workload, templates):
    overtime_html_string = ""
    overtime_table = ""
    overtime_html_string += templates['workload_overtime'].substitute(
        {
            'overtime_table': overtime_table
        })
    return overtime_html_string
