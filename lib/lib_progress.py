from lib.lib_date import date_to_day


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


def get_attendance_progress(attendance, results, attendance_perspective):
    # bepaal de voortgang
    attendance_perspective.attendance_submissions = sorted(attendance_perspective.attendance_submissions, key=lambda s: s.day)
    total_score = 0
    total_count = 0
    last_flow = 1.0
    for submission in attendance_perspective.attendance_submissions:
        if submission.graded:
            attendance_perspective.last_score = submission.day
            total_score += submission.score
            total_count += 1
            submission.flow = total_score / total_count / 2
            # print(submission.flow)
            attendance_perspective.sum_score = submission.flow
            last_flow = submission.flow
        else:
            submission.flow = last_flow
    if total_count == 0:
        # Niet te bepalen
        attendance_perspective.progress = -1
    elif attendance_perspective.last_score != 0:
        # print(f"LP54 - Laatste dag {attendance_perspective.last_score}, laatste waarde {attendance_perspective.sum_score}")
        attendance_perspective.progress = attendance.bandwidth.get_progress(attendance_perspective.last_score,  attendance_perspective.sum_score*100)
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
                        if submission_sequence.is_graded():
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
                        perspective.progress = -1
                    elif perspective.last_score != 0:
                        perspective.progress = assignment_group.bandwidth.get_progress(perspective.last_score,
                                                                                       perspective.sum_score)
                    else:
                        # Niet te bepalen
                        perspective.progress = -1
                else:
                    # Niet te bepalen
                    perspective.progress = -1
            else:
                # Niet te bepalen
                perspective.progress = -1
        else:
            print("LP63 - Perspective assignment_group is not set [None]")
    elif len(perspective.assignment_groups) > 1:
        print("LP64 - Perspective has more then one assignment_groups attached", perspective.name,
              perspective.assignment_groups)
    else:
        print("LP65 - Perspective has no assignment_groups attached", perspective.name, perspective.assignment_groups)

