import textwrap
from lib.lib_plotly import peil_labels, score_dict
from lib.lib_submission import NO_DATA


def peil_contruct(a_course, a_peil_perspective):
    peilingen = {}
    for peil in peil_labels:
        peilingen[peil] = []
    peil_perspective = a_course.find_perspective_by_name(a_peil_perspective)
    assignment_group = a_course.find_assignment_group(peil_perspective.assignment_groups[0])
    for assignment in assignment_group.assignments:
        for peil_label in peil_labels:
            if peil_label.lower() in assignment.name.lower():
                peilingen[peil_label].append(assignment)
    return peilingen


# zoek het juiste peilmoment
def get_perspective_name(a_course, a_peilmoment, a_peil_perspective):
    # "peil"
    peil_perspective = a_course.find_perspective_by_name(a_peil_perspective)
    for perspective in a_course.perspectives:
        if perspective.name != peil_perspective.name:
            print(perspective, a_peilmoment )
            if perspective.name.lower() in a_peilmoment.name.lower():
                return perspective.name
    return None


def get_bar_score(a_peilmoment):
    score = 0.1
    if a_peilmoment:
        if a_peilmoment.graded:
            score = a_peilmoment.score + 1
    return score


def get_peil_hover(a_peilmoment):
    score = 0.1
    hover = NO_DATA
    if a_peilmoment:
        if a_peilmoment.graded:
            score = a_peilmoment.score + 1
        if "Beoordeling" in a_peilmoment.assignment_name:
            hover = a_peilmoment.assignment_name + " - " + score_dict[int(score - 1)]["beoordeling"]
        else:
            hover = a_peilmoment.assignment_name + " - " + score_dict[int(score - 1)]["voortgang"]
        for comment in a_peilmoment.comments:
            value = comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                hover += "<br>" + line
    return hover

