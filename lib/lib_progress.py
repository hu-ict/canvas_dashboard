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
    if -1 in a_progress:
        return -1
    elif 0 in a_progress:
        return 0
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
    return -1


def get_progress(start, course, results, perspective):
    # bepaal de voortgang
    if len(perspective.assignment_groups) == 1:
        assignment_group = course.find_assignment_group(perspective.assignment_groups[0])
        if assignment_group is not None:
            if perspective.name == start.attendance_perspective:
                perspective.submissions = sorted(perspective.submissions, key=lambda s: s.submitted_date)
                total_score = 0
                total_count = 0
                for submission in perspective.submissions:
                    perspective.last_score = date_to_day(start.start_date, submission.submitted_date)
                    total_score += submission.score
                    total_count += 1
                    submission.flow = total_score / total_count * 100 / 2
                    # print(submission.flow)
                    perspective.sum_score = total_score
                perspective.progress = assignment_group.bandwidth.get_progress(assignment_group.strategy,
                                                                               results.actual_day,
                                                                               perspective.last_score,
                                                                               total_score / total_count * 100 / 2)
            elif assignment_group.bandwidth is not None:
                if len(perspective.submissions) > 0:
                    perspective.submissions = sorted(perspective.submissions, key=lambda s: s.submitted_date)
                    total_score = 0
                    total_count = 0
                    for submission in perspective.submissions:
                        if submission.graded:
                            perspective.last_score = submission.assignment_day
                            total_score += submission.score
                            total_count += 1
                            submission.flow = assignment_group.bandwidth.get_progress_range(perspective.last_score, total_score)
                            # print(submission.flow)
                            perspective.sum_score = total_score
                            # print("Graded")
                        else:
                            pass
                            # print("Not graded")
                    if total_count == 0:
                        # Niet te bepalen
                        perspective.progress = -1
                    elif perspective.last_score != 0:
                        perspective.progress = assignment_group.bandwidth.get_progress(assignment_group.strategy,
                                                                                       results.actual_day,
                                                                                       perspective.last_score,
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
            print("Could not find assignment_group with id", perspective.assignment_groups[0])
    elif len(perspective.assignment_groups) > 1:
        print("Perspective has more then one assignment_groups attached", perspective.name,
              perspective.assignment_groups)
    else:
        print("Perspective has no assignment_groups attached", perspective.name, perspective.assignment_groups)

