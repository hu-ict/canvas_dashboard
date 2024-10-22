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
    if 0 in a_progress:
        return 0
    if 1 in a_progress:
        return 1
    if -1 in a_progress:
        return -1
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


def get_attendance_progress(attendance, attendance_perspective):
    # bepaal de voortgang
    attendance_perspective.attendance_submissions = sorted(attendance_perspective.attendance_submissions, key=lambda s: s.day)
    attendance_perspective.count = 0
    attendance_perspective.percentage = 0
    attendance_perspective.essential_count = 0
    attendance_perspective.essential_percentage = 0
    essential_points = 0
    points = 0
    last_flow = 1.0
    for submission in attendance_perspective.attendance_submissions:
        moment = attendance.get_moment(submission.day)
        attendance_perspective.count += 1
        points += submission.score
        attendance_perspective.percentage = points / attendance_perspective.count / 2
        if moment is not None:
            # print("LP61 -", moment)
            # alleen op vastgestelde dagen wordt aanwezigheid beloond
            essential_points += submission.score
            attendance_perspective.essential_count += 1
            attendance_perspective.essential_percentage = essential_points / attendance_perspective.essential_count / moment.points
            submission.flow = attendance_perspective.essential_percentage
            last_flow = submission.flow
        else:
            submission.flow = last_flow
        attendance_perspective.last_score = submission.day
    if attendance_perspective.essential_count == 0:
        # Niet te bepalen
        attendance_perspective.progress = -1
    elif attendance_perspective.last_score != 0:
        # print(f"LP54 - Laatste dag {attendance_perspective.last_score}, laatste waarde {attendance_perspective.sum_score}")
        attendance_perspective.progress = attendance.bandwidth.get_progress(attendance_perspective.last_score,  attendance_perspective.essential_percentage*100)
        # print(f"LP55 - Laatste dag {attendance_perspective.last_score}, laatste waarde {attendance_perspective.sum_score*100}, voortgang {attendance_perspective.progress}")
    else:
        # Niet te bepalen
        attendance_perspective.progress = -1


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
                            # print("LP62 -", submission_sequence.name, perspective.last_score, round(total_score, 2))
                            submission_sequence.flow = assignment_group.bandwidth.get_progress_range(perspective.last_score, total_score)
                            # print(submission.flow)
                            perspective.sum_score = round(total_score, 2)
                            last_flow = submission_sequence.flow
                            # print("Graded")
                        else:
                            submission_sequence.flow = last_flow
                            # print("Not graded")
                    if total_count == 0:
                        # Niet te bepalen
                        perspective.progress = 0
                    elif perspective.last_score != 0:
                        perspective.progress = assignment_group.bandwidth.get_progress(perspective.last_score,
                                                                                       perspective.sum_score)
                    else:
                        # Niet te bepalen
                        perspective.progress = 0
                else:
                    # Niet te bepalen
                    perspective.progress = 0
            else:
                # Niet te bepalen
                perspective.progress = 0
        else:
            print("LP63 - Perspective assignment_group is not set [None]")
    elif len(perspective.assignment_groups) > 1:
        print("LP64 - Perspective has more then one assignment_groups attached", perspective.name,
              perspective.assignment_groups)
    else:
        print("LP65 - Perspective has no assignment_groups attached", perspective.name, perspective.assignment_groups)


def proces_progress(course, results, progress_history):
    progress_day = ProgressDay(results.actual_day, course.perspectives.keys())
    for student in results.students:
        if course.attendance is not None:
            get_attendance_progress(course.attendance, student.attendance_perspective)
            progress_day.attendance[str(student.attendance_perspective.progress)] += 1
        for perspective in student.perspectives.values():
            get_progress(course, perspective)
            progress_day.perspective[perspective.name][str(perspective.progress)] += 1
    # bepaal de totaal voortgang
    for student in results.students:
        perspectives = []
        for perspective in student.perspectives.values():
            # print("GP08 -", perspective.name, perspective.progress)
            perspectives.append(perspective.progress)
        # print("GP10 -", perspectives)
        progress = get_overall_progress(perspectives)
        # print("GP20 - student.progress =", progress, student.name)
        student.progress = progress
        progress_day.progress[str(progress)] += 1
        # print(f"{student.name}, {student.role}, {student.progress}, {student.perspectives['team'].progress}, {student.perspectives['gilde'].progress}, {student.perspectives['kennis'].progress}")
    progress_history.append_day(progress_day)

