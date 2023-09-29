import json

import requests
from canvasapi import Canvas
from lib.config import API_URL, actual_date, DATE_TIME_STR, get_date_time_obj
from lib.file import read_start, read_config
from lib.translation_table import translation_table
from model.Assignment import Assignment
from model.Perspective import Perspective
from model.Student import Student

CLIENT_SECRET = "eyJ0eXAiOiJKV1QiLCJub25jZSI6InlOM1dYbFhvNGZ6Vk5QLUNOWVB0RU1QWHpTUXlHWUJxOU9pekVrb0tlTjQiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC85ODkzMjkwOS05YTVhLTRkMTgtYWNlNC03MjM2YjViNWUxMWQvIiwiaWF0IjoxNjk1ODA3NTUzLCJuYmYiOjE2OTU4MDc1NTMsImV4cCI6MTY5NTg5NDI1NCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhVQUFBQVJVVW5CaHcyZDRjcnVlL3F0MnlkU3lOSG1ReVlmWFJSUFJXRE5qRzZnQ0p1ZDQvMmROdlhMTDZ1bGxrcDc0aDdmaHA4ZE5VOWNoVEhSdWZYcXVaNW1aL3o0Mk9waXF3aE5SM1UvU0gyamJvPSIsImFtciI6WyJwd2QiLCJyc2EiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImRldmljZWlkIjoiYTBjODI2YWYtMDNhMC00ZTY2LTlmNzEtMGQ3ZGVkYmU0MTU0IiwiZmFtaWx5X25hbWUiOiJXaWxrZW5zIiwiZ2l2ZW5fbmFtZSI6IkJlcmVuZCIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjE2OC4xMTkuNTcuMTk4IiwibmFtZSI6IkJlcmVuZCBXaWxrZW5zIiwib2lkIjoiMjlmZjI4MTgtMzFlMC00MzRjLThjMzAtNTBjYTA0ZGYwYTEyIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTE3NTc0MzYyNjYtMTA3MDM3OTMyNi0xNDUyNzYzMTYxLTY3NDM3IiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMzRkZGODYyMjhDRTUiLCJwd2RfZXhwIjoiMzMzMTYwIiwicHdkX3VybCI6Imh0dHBzOi8vc3RzLmh1Lm5sL2FkZnMvcG9ydGFsL3VwZGF0ZXBhc3N3b3JkLyIsInJoIjoiMC5BUUlBQ1NtVG1GcWFHRTJzNUhJMnRiWGhIUU1BQUFBQUFBQUF3QUFBQUFBQUFBQUNBSkEuIiwic2NwIjoiQXVkaXRMb2cuUmVhZC5BbGwgQ2FsZW5kYXJzLlJlYWRXcml0ZSBDb250YWN0cy5SZWFkV3JpdGUgRGV2aWNlTWFuYWdlbWVudEFwcHMuUmVhZC5BbGwgRGV2aWNlTWFuYWdlbWVudEFwcHMuUmVhZFdyaXRlLkFsbCBEZXZpY2VNYW5hZ2VtZW50Q29uZmlndXJhdGlvbi5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50Q29uZmlndXJhdGlvbi5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5Qcml2aWxlZ2VkT3BlcmF0aW9ucy5BbGwgRGV2aWNlTWFuYWdlbWVudE1hbmFnZWREZXZpY2VzLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRSQkFDLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRSQkFDLlJlYWRXcml0ZS5BbGwgRGV2aWNlTWFuYWdlbWVudFNlcnZpY2VDb25maWcuUmVhZC5BbGwgRGV2aWNlTWFuYWdlbWVudFNlcnZpY2VDb25maWcuUmVhZFdyaXRlLkFsbCBEaXJlY3RvcnkuQWNjZXNzQXNVc2VyLkFsbCBEaXJlY3RvcnkuUmVhZC5BbGwgRGlyZWN0b3J5LlJlYWRXcml0ZS5BbGwgRmlsZXMuUmVhZFdyaXRlLkFsbCBHcm91cC5SZWFkLkFsbCBHcm91cC5SZWFkV3JpdGUuQWxsIElkZW50aXR5Umlza0V2ZW50LlJlYWQuQWxsIE1haWwuUmVhZFdyaXRlIE1haWxib3hTZXR0aW5ncy5SZWFkV3JpdGUgTm90ZXMuUmVhZFdyaXRlLkFsbCBvcGVuaWQgUGVvcGxlLlJlYWQgcHJvZmlsZSBSZXBvcnRzLlJlYWQuQWxsIFNpdGVzLlJlYWRXcml0ZS5BbGwgVGFza3MuUmVhZFdyaXRlIFRlYW1zQXBwSW5zdGFsbGF0aW9uLlJlYWRGb3JUZWFtIFRlYW1zQXBwSW5zdGFsbGF0aW9uLlJlYWRXcml0ZUZvclRlYW0gVXNlci5SZWFkIFVzZXIuUmVhZEJhc2ljLkFsbCBVc2VyLlJlYWRXcml0ZSBVc2VyLlJlYWRXcml0ZS5BbGwgZW1haWwiLCJzaWduaW5fc3RhdGUiOlsiZHZjX21uZ2QiLCJkdmNfZG1qZCIsImttc2kiXSwic3ViIjoiazZlQ2U4RnEzb2I3SUlGcmlVVXlfby00aFFfejQwSE1YQzBDamQzTDJ2cyIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJFVSIsInRpZCI6Ijk4OTMyOTA5LTlhNWEtNGQxOC1hY2U0LTcyMzZiNWI1ZTExZCIsInVuaXF1ZV9uYW1lIjoiYmVyZW5kLndpbGtlbnNAaHUubmwiLCJ1cG4iOiJiZXJlbmQud2lsa2Vuc0BodS5ubCIsInV0aSI6Im9waGZEMExnZWtXQzFUcjF1YWNYQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfY2MiOlsiQ1AxIl0sInhtc19zc20iOiIxIiwieG1zX3N0Ijp7InN1YiI6InUtSzFpeWRBOGNfc01kRGh5dEk4UjdKMjByMFZpTUY2T3NhaEUtQWV3alUifSwieG1zX3RjZHQiOjEzNDE5MjA0OTAsInhtc190ZGJyIjoiRVUifQ.im6U-_JlzzIK7ggfFoVBzMrQ1oO21xXPIohCviMnKyXnpY9wS_AHIYpYVdlrX4iQOT30LWz-Pl4-hNxT645LwDUHqYrgFqdNasUqTZFdrzam2pQr0tYNuZSJj2WMjhN2b7W0RhGeArk_dVibnhJRB2Ik6fQ9Uc-EuZsEzYBb6dA0EYv-FU3biDUuFvgJc7lT1qbBtL9xxWUx7qZnhP0oa02OEvtdw_PKfVtbo6HjMxKjR1K-20X0Dsn5ItPhZcv8K2sK15iGxXmsNfJbYgQEi-0CDRW_gd888Lqx_y8sI6fwKA8qhJoMjaHFBYRsTb3K9hDYbxjzY7f5OELDwgBs4g"
def get_dates(input):
    if input['due_at']:
        assignment_date = get_date_time_obj(input['due_at'])
    else:
        if input['lock_at']:
            assignment_date = get_date_time_obj(input['lock_at'])
        else:
            assignment_date = course_config_start.end_date
    if input['unlock_at']:
        unlock_date = get_date_time_obj(input['unlock_at'])
    else:
        unlock_date = course_config_start.start_date
    return unlock_date, assignment_date

def get_sites(a_config):
    l_sites = {}
    url = f"https://graph.microsoft.com/v1.0/sites?search={'INNO'}"
    headers = {
        "Authorization": "Bearer " + CLIENT_SECRET,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        values = result['value']
        print("Aantal sites:",len(values))
        for value in values:
            # "INNO - Sep23 - Studenten - Kyrill Westdorp"
            l_display_name = value['displayName']
            l_student_name = l_display_name.split(' - ')
            if len(l_student_name) > 3:
                l_student_name = l_display_name.split(' - ')[3]
                print(l_display_name, l_student_name)
                l_student = a_config.find_student_by_name(l_student_name)

                if l_student:
                    print(l_student.name, value['id'])
                    l_student.site = value['id']
    else:
        print(f"Error getting token: {response.json()}")
    return l_sites


def link_teachers():
    print('Link teachers to student_groups and assignment_groups')
    for teacher in config.teachers:
        for studentGroupId in teacher.projects:
            studentGroup = config.find_student_group(studentGroupId)
            if studentGroup:
                studentGroup.teachers.append(teacher.id)
        for assignmentGroupId in teacher.assignment_groups:
            assignmentGroup = config.find_assignment_group(assignmentGroupId)
            if assignmentGroup:
                assignmentGroup.teachers.append(teacher.id)

course_config_start = read_start()
config = read_config(course_config_start.config_file_name)
print(config)


# Initialize a new Canvas object
canvas = Canvas(API_URL, course_config_start.api_key)
user = canvas.get_current_user()
print(user.name)

canvas_course = canvas.get_course(course_config_start.course_id)

link_teachers()

# course = Course(canvas_course.id, canvas_course.name, actual_date.strftime(DATE_TIME_STR))

# Ophalen Students
users = canvas_course.get_users(enrollment_type=['student'])
config.students = []
for user in users:
    print(user.name, user.login_id)
    student = Student(user.id, 0, user.name, 'None', user.login_id, "")
    config.students.append(student)

get_sites(config)

# Ophalen canvas_pages
# pages = canvas_course.get_pages()
# for page in pages:
#     print(f"{page.published:1};{page.title};{page.url}")

# Ophalen Secties en Roles
course_sections = canvas_course.get_sections(include=['students'])
for course_section in course_sections:
    # use only relevant sections
    section = config.find_section(course_section.id)
    if section:
        print("course_section", section)
        course_section_students = course_section.students
        if course_section_students:
            for section_student in course_section_students:
                student_id = section_student["id"]
                student = config.find_student(student_id)
                if student:
                    student.roles.append(section.role)

for student in config.students:
    if len(student.roles) == 0:
        config.students.remove(student)
config.student_count = len(config.students)

# Perspectives toevoegen aan Students
for student in config.students:
    for perspective in config.perspectives:
        # print(perspective.assignment_groups)
        if len(perspective.assignment_groups) > 1:
            new_perspective = Perspective(perspective.name)
            assignment_group_id = config.find_assignment_group_by_role(student.get_role())
            new_perspective.assignment_groups.append(assignment_group_id)
            student.perspectives.append(new_perspective)
        else:
            student.perspectives.append(perspective)

# Students en StudentGroups koppelen
canvas_group_categories = canvas_course.get_group_categories()
for canvas_group_category in canvas_group_categories:
    print(canvas_group_category)
    # ophalen projectgroepen
    if canvas_group_category.name == course_config_start.projects_groep_name:
        canvas_groups = canvas_group_category.get_groups()
        for canvas_group in canvas_groups:
            print(canvas_group)
            studentGroup = config.find_student_group(canvas_group.id)
            if studentGroup:
                canvas_users = canvas_group.get_users()
                for canvas_user in canvas_users:
                    student = config.find_student(canvas_user.id)
                    if student:
                        student.group_id = studentGroup.id
                        if len(studentGroup.teachers) > 0:
                            student.coach_initials = config.find_teacher(studentGroup.teachers[0]).initials
                        studentGroup.students.append(student)
    # ophalen slb-groepen
    if canvas_group_category.name == course_config_start.slb_groep_name:
        canvas_groups = canvas_group_category.get_groups()
        for canvas_group in canvas_groups:
            print(canvas_group)
            slb_group = config.find_slb_group(canvas_group.id)
            if slb_group:
                canvas_users = canvas_group.get_users()
                for canvas_user in canvas_users:
                    student = config.find_student(canvas_user.id)
                    if student:
                        slb_group.students.append(student)

# Ophalen Assignments bij de AssignmentsGroups
canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides', 'online_quiz'])
for canvas_assignment_group in canvas_assignment_groups:
    # use only relevant assignment_groups
    assignment_group = config.find_assignment_group(canvas_assignment_group.id)
    if assignment_group:
        print("assignment_group", canvas_assignment_group)
        group_points_possible = 0
        for canvas_assignment in canvas_assignment_group.assignments:
            if canvas_assignment['points_possible']:
                group_points_possible += canvas_assignment['points_possible']
                points_possible = canvas_assignment['points_possible']
            else:
                points_possible = 0

            # l_submission_types = canvas_assignment['submission_types']
            # print(l_submission_types)
            # if 'external_tool' in l_submission_types:
            #     print(canvas_assignment['quiz_id'])
            if canvas_assignment['overrides']:
                for overrides in canvas_assignment['overrides']:
                    unlock_date, assignment_date = get_dates(overrides)
                    if 'course_section_id' in overrides.keys():
                        section_id = overrides['course_section_id']
                    else:
                        section_id = 0
                    assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'], canvas_assignment['assignment_group_id'], section_id, points_possible, assignment_date, unlock_date)
                    print("OVERRIDE", assignment)
                    assignment_group.append_assignment(assignment)
            else:
                unlock_date, assignment_date = get_dates(canvas_assignment)
                section_id = 0
                assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'],
                                    canvas_assignment['assignment_group_id'], section_id,
                                    points_possible, assignment_date, unlock_date)
                print(assignment)
                assignment_group.append_assignment(assignment)
        print(assignment_group.name, assignment_group.total_points, group_points_possible)
        # assignment_group.total_points = group_points_possible

with open(course_config_start.course_file_name, 'w') as f:
    dict_result = config.to_json(["assignment"])
    json.dump(dict_result, f, indent=2)
