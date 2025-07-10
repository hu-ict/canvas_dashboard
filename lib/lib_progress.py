from lib.lib_attendance import get_attendance_progress
from model.ProgressDay import ProgressDay
from model.perspective.Status import MISSED_ITEM


def flow_to_progress(flow):
    if flow < 0.01:
        return 0
    elif flow < 0.3:
        return 1
    elif 0.3 <= flow <= 0.7:
        return 2
    else:
        return 3


def get_overall_progress(a_progress):
    # print("LP11 - get_overall_progress", a_progress)
    if 0 in a_progress:
        return 0
    if 1 in a_progress:
        return 1
    if -1 in a_progress:
        return -1
    if len(a_progress) == 1:
        return a_progress[0]
    boven = 8
    if len(a_progress) == 3: # 3 perspectieven
        if a_progress[0] >= 2 and a_progress[1] >= 2 and a_progress[2] >= 2:
            if sum(a_progress) >= boven:
                # boven niveau
                return 3
            else:
                # op niveau
                return 2
        else:
            return 1
    if len(a_progress) == 4: # 3 perspectieven
        if a_progress[0] >= 2 and a_progress[1] >= 2 and a_progress[2] >= 2 and a_progress[3] >= 2:
            if sum(a_progress) >= 10:
                # boven niveau
                return 3
            else:
                # op niveau
                return 2
        else:
            return 1
    return -1


def get_progress(course, perspective):
    # bepaal de voortgang
    if len(perspective.assignment_groups) == 1:
        assignment_group = course.find_assignment_group(perspective.assignment_groups[0])
        if assignment_group is not None:
            if assignment_group.bandwidth is not None:
                if len(perspective.submission_sequences) > 0:
                    total_score = 0.00
                    total_count = 0
                    last_flow = 0.5
                    for submission_sequence in perspective.submission_sequences:
                        if submission_sequence.is_graded() or submission_sequence.get_status() == MISSED_ITEM:
                            perspective.last_score = submission_sequence.get_day()
                            total_score += round(submission_sequence.get_score(), 2)
                            total_count += 1
                            # print("LP62 -", submission_sequence.name, perspective.last_score, submission_sequence.get_score(), round(total_score, 2))
                            submission_sequence.flow = assignment_group.bandwidth.get_progress_range(perspective.last_score, total_score)
                            # print("LP63 -", submission_sequence.flow)
                            perspective.sum_score = round(total_score, 2)
                            last_flow = submission_sequence.flow
                            # print("Graded")
                        else:
                            submission_sequence.flow = last_flow
                            # print("Not graded")
                    if total_count == 0:
                        # Niet te bepalen
                        return 0
                    elif perspective.last_score != 0:
                        return assignment_group.bandwidth.get_progress(perspective.last_score,
                                                                                       perspective.sum_score)
                    else:
                        # Niet te bepalen
                        return 0
                else:
                    # Niet te bepalen
                    return 0
            else:
                # Niet te bepalen
                return 0
        else:
            print("LP63 - Perspective assignment_group is not set [None]")
            return 0
    elif len(perspective.assignment_groups) > 1:
        print("LP64 - Perspective has more then one assignment_groups attached", perspective.name, perspective.assignment_groups)
        return 0
    else:
        print("LP65 - Perspective has no assignment_groups attached", perspective.name, perspective.assignment_groups)
        return 0


def proces_progress(course, results, progress_history):
    progress_day = ProgressDay(results.actual_day, course.perspectives.keys())
    for student in results.students:
        if course.attendance is not None:
            student.student_attendance.progress = get_attendance_progress(course.attendance, student)
            progress_day.attendance[str(student.student_attendance.progress)] += 1
        for perspective in student.perspectives.values():
            perspective.progress = get_progress(course, perspective)
            # print("LP71 -", perspective.name, progress_day)
            progress_day.perspectives[perspective.name][str(perspective.progress)] += 1
    # bepaal de totaal voortgang
    for student in results.students:
        perspectives = []
        for perspective in student.perspectives.values():
            # print("GP08 -", perspective.name, perspective.progress)
            perspectives.append(perspective.progress)
        # print("LP21 - proces_progress", perspectives)
        progress = get_overall_progress(perspectives)
        # print("LP22 - student.progress =", progress, student.name)
        student.progress = progress
        progress_day.progress[str(progress)] += 1
        # print(f"{student.name}, {student.role}, {student.progress}, {student.perspectives['team'].progress}, {student.perspectives['gilde'].progress}, {student.perspectives['kennis'].progress}")
    progress_history.append_day(progress_day)

