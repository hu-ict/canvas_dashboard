from scripts.model.Assessor import Assessor
from scripts.model.StudentGroup import StudentGroup
from scripts.model.StudentLink import StudentLink


def get_groups(scope, canvas_course):
    print("LST11 -", scope, canvas_course.name)
    group_list = []
    if not scope or len(scope) == 0:
        return group_list
    if scope == "SECTIONS":
        print("GST21 - Werken met Canvas secties als groepen (meestal S1 propedeuse).")
        course_sections = canvas_course.get_sections()
        for course_section in course_sections:
            student_group = StudentGroup(course_section.id, course_section.name, 0)
            group_list.append(student_group)
        return group_list
    else:
        canvas_group_categories = canvas_course.get_group_categories()
        for canvas_group_category in canvas_group_categories:
            # print("GCONF20 -", canvas_group_category, start1.project_group_name, start1.guild_group_name)
            # retrieve project_groups
            if canvas_group_category.name == scope:
                canvas_groups = canvas_group_category.get_groups()
                for canvas_group in canvas_groups:
                    student_group = StudentGroup(canvas_group.id, canvas_group.name, 0)
                    group_list.append(student_group)
                    # print("GST23 - project_group", canvas_group)
                return group_list
    print("GST25 - onbekende group_category", canvas_group_category.name)
    return group_list


def get_students_in_groups(dashboard, course, canvas_course):
    if dashboard.project_group_name == "SECTIONS":
        print("GST31 - Werken met Canvas secties als groepen (meestal S1 propedeuse).")
    else:
        canvas_group_categories = canvas_course.get_group_categories()
        for canvas_group_category in canvas_group_categories:
            print("GST32 -", canvas_group_category)
            # Link students to project_groups
            if canvas_group_category.name == dashboard.project_group_name:
                print("GST33 - Link students to project_groups", canvas_group_category.name)
                link_students_to_project_groups(course, canvas_group_category.get_groups())
            if canvas_group_category.name == dashboard.guild_group_name:
                print("GST34 - Link students to guild_groups", canvas_group_category.name)
                link_students_to_guild_groups(course, canvas_group_category.get_groups())


def add_assessors_to_groups_and_students(course, student_group, teacher, responsibility):
    assessor = Assessor(teacher.id, responsibility.student_group_collection, student_group.id,
                        responsibility.assignment_group_id)
    # print("GST46 -", assessor, student_group.name)
    student_group.assessors.append(assessor)
    for student_link in student_group.students:
        student = course.find_student(student_link.id)
        student.assessors.append(assessor)


def link_assessors_to_groups_and_students(course):
    print('GST41 - Link assessors to groups and students')
    for teacher in course.teachers:
        for responsibility in teacher.responsibilities:
            # print("GST43 -", responsibility.student_group_collection)
            if responsibility.student_group_collection == "project_groups":
                for student_group_id in responsibility.student_groups:
                    # zoeken naar project_group en nummer of naam
                    student_group = course.find_project_group(student_group_id)
                    if student_group is None:
                        # zoeken op naam
                        student_group = course.find_project_group_by_name(student_group_id)
                    if student_group is not None:
                        add_assessors_to_groups_and_students(course, student_group, teacher, responsibility)
                    else:
                        print("GST45 - geen student_group voor", student_group_id)

            if responsibility.student_group_collection == "guild_groups":
                for student_group_name in responsibility.student_groups:
                    # zoeken naar project_group en nummer of naam
                    print("GST81 -", student_group_name)
                    student_group = course.find_guild_group(student_group_name)
                    if student_group is None:
                        # zoeken op naam
                        student_group = course.find_guild_group_by_name(student_group_name)
                    if student_group is not None:
                        add_assessors_to_groups_and_students(course, student_group, teacher, responsibility)
                    else:
                        print("GST47 - geen student_group voor", student_group_id)


def link_principal_assessor_to_groups_and_students(course):
    assignment_group = course.get_assignment_group(course.grade_moments.assignment_group_ids[0])
    for student_group in course.project_groups:
        for assessor in student_group.assessors:
            if assessor.assignment_group_id == assignment_group.id:
                student_group.principal_assessor = assessor.teacher_id


def get_section_students(project_group_name, course, canvas_course):
    # Ophalen Secties en Roles
    print("GST61 -", "Ophalen students and secties uit Canvas deze koppelen aan Role ")
    canvas_sections = canvas_course.get_sections(include=['students'])
    for course_section in canvas_sections:
        # use only relevant sections
        section = course.find_section(course_section.id)
        if section:
            course_section_students = course_section.students
            if course_section_students:
                for section_student in course_section_students:
                    student_id = section_student["id"]
                    student = course.find_student(student_id)
                    if student is not None:
                        if project_group_name == "SECTIONS":
                            project_group = course.find_project_group_by_name(section.name)
                            # print("GST63 -", section.name, project_group)
                            if project_group:
                                student.project_id = project_group.id
                                for teacher_id in project_group.assessors:
                                    student.project_teachers.append(teacher_id)
                                student_link = StudentLink.from_student(student)
                                # print("GS64 -", student_link)
                                project_group.students.append(student_link)
                            else:
                                print(f"GST65 - ERROR - section.name ({section.name}) not found in list student_group for student {student.name}.")
                        student.role = section.role
                        if student.role is None:
                            print("GST66 - student.role is leeg", student.name)
                    else:
                        print("GST67 -", "Student not found", section_student["id"], "from section", section)
            else:
                print("GST68 -", "No students in section", course_section.name)
        else:
            print("GST69 -", "Section not found", course_section.name)


def link_students_to_role(course):
    # Link students to roles
    print("GS71 - Link students to roles")
    for role in course.roles:
        students = course.find_students_by_role(role.short)
        for student in students:
            student_link = StudentLink.from_student(student)
            # print("GS73 -", student_link)
            role.students.append(student_link)


def link_students_to_project_groups(course, canvas_groups):
    # dit zijn de project_groups of de guild_groups
    print("GST81 - link_students_to_project_groups")
    for canvas_group in canvas_groups:
        print("GST82 -", canvas_group)
        student_group = course.find_project_group(canvas_group.id)
        if student_group:
            canvas_users = canvas_group.get_users()
            for canvas_user in canvas_users:
                student = course.find_student(canvas_user.id)
                # print("GST84 - Student", student)
                if student:
                    # print("GST85 - Student", student)
                    student.project_id = student_group.id
                    # for teacher_id in student_group.teachers:
                    #     student.project_teachers.append(teacher_id)
                    student_link = StudentLink.from_student(student)
                    # print("GS86 -", student_link)
                    student_group.students.append(student_link)
                else:
                    print("GST87 - Student in Canvas project_group not found", canvas_user.id, canvas_user.name)


def link_students_to_guild_groups(course, canvas_groups):
    # dit zijn de project_groups of de guild_groups
    print("GST91 - link_students_to_guild_groups")
    for canvas_group in canvas_groups:
        print("GST92 -", canvas_group)
        student_group = course.find_guild_group(canvas_group.id)
        if student_group:
            # print("GTS93 -", student_group)
            canvas_users = canvas_group.get_users()
            for canvas_user in canvas_users:
                student = course.find_student(canvas_user.id)
                if student:
                    # print("GTS94 -", student.name)
                    student.guild_id = student_group.id
                    # for teacher_id in student_group.teachers:
                    #     student.guild_teachers.append(teacher_id)
                    student_link = StudentLink.from_student(student)
                    # print("GS95 -", student_link)
                    student_group.students.append(student_link)
                else:
                    print("GST96 - Student in Canvas guild group not found", canvas_user.id, canvas_user.name)

