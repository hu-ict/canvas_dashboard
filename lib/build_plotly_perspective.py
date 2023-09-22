import textwrap

from lib.config import get_marker_size, fraction_to_level, hover_style, date_to_day, score_dict, get_date_time_str, \
    get_date_time_loc
import plotly.graph_objs as go

from model.Comment import Comment
from model.Submission import Submission


def calc_dev(iterations, r, a, b, c):
    iteration_list = []
    for x in range(iterations-r):
        y = a*x*x+b*x+c
        if y < 0:
            y = 0
        iteration_list.append(y)
    for x in range(r):
        iteration_list.append(y)
    return iteration_list


def get_hover(a_peil_submissions):
    score = 0.1
    hover = "Geen data"
    if a_peil_submissions:
        if a_peil_submissions.graded:
            score = a_peil_submissions.score + 1
        if "Beoordeling" in a_peil_submissions.assignment_name:
            hover = a_peil_submissions.assignment_name + " - " + score_dict[int(score - 1)]['beoordeling']
        else:
            hover = a_peil_submissions.assignment_name + " - " + score_dict[int(score-1)]["voortgang"]
        for comment in a_peil_submissions.comments:
            value = comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                hover += "<br>" + line
    return hover


def find_submissions(a_student, a_peil_construction):
    for l_perspective in a_peil_construction.values():
        for peil in l_perspective:
            l_submission = a_student.get_peilmoment(peil['assignment'].id)
            if l_submission:
                peil['submission'] = l_submission
    return a_peil_construction


def plot_progress(a_row, a_col, a_fig, a_perspective, a_start_date):
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': [], 'size': []}
    for pleiling in a_perspective:
        series['y'].append(0)
        if pleiling['submission']:
            series['size'].append(get_marker_size(True)+2)
            series['hover'].append(get_hover(pleiling['submission']))
            series['x'].append(date_to_day(a_start_date, pleiling['submission'].submitted_at))
            series['color'] = score_dict[int(pleiling['submission'].score)]['color']
        else:
            series['size'].append(get_marker_size(False)+2)
            series['hover'].append(pleiling['assignment'].name + "<br>" + get_date_time_loc(pleiling['assignment'].assignment_date))
            series['x'].append(date_to_day(a_start_date, pleiling['assignment'].assignment_date))
            series['color'] = score_dict[-1]['color']
    a_fig.add_trace(
        go.Scatter(
            x=series['x'],
            y=series['y'],
            hoverinfo="text",
            hovertext=series['hover'],
            mode='markers',
            marker_color=series['color'],
            hoverlabel=hover_style,
            line_color="#444444",
            marker=dict(
                size=series['size'],
                symbol="arrow-down",
                opacity=1.0,
                line=dict(
                    width=2
                )
            )
        ),
        row=a_row, col=a_col
    )


def plot_open_assignments(a_row, a_col, a_fig, a_assignments, a_start_date, a_actual_day):
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': []}

    for assignment in a_assignments:
        series['size'].append(get_marker_size(False))
        series['x'].append(date_to_day(a_start_date, assignment.assignment_date))
        series['y'].append(0)
        series['color'].append(score_dict[-1]['color'])
        series['hover'].append(assignment.name + "<br>" + get_date_time_loc(assignment.assignment_date) + "<br>" + str(assignment.points) + " punten")
    a_fig.add_trace(
        go.Scatter(
            x=series['x'],
            y=series['y'],
            hoverinfo="text",
            hovertext=series['hover'],
            mode='markers',
            marker_color=series['color'],
            line_color="#444444",
            hoverlabel=hover_style,
            marker=dict(
                size=series['size'],
                opacity=1.0,
                line=dict(
                    width=2
                )
            )
        ),
        row=a_row, col=a_col
    )
    return



def plot_bandbreedte(a_row, a_col, a_fig, assignment_group, a_actual_day, a_days_in_semester):
    if assignment_group.total_points <= 0:
        return
    x_time = calc_dev(a_days_in_semester, 0, 0, 1, 0)
    # bereken bandbreedte
    if assignment_group.name == "TEAM":
        band_lower = calc_dev(a_days_in_semester, 14, 0.0016, 0.08, -1.5)
        band_upper = calc_dev(a_days_in_semester, 14, 0.0020, 0.08, 11)
    else:
        b = assignment_group.lower_points / (a_days_in_semester-14 - 30)
        c = - 30 * b
        band_lower = calc_dev(a_days_in_semester, 14, 0, b, c)
        band_upper = calc_dev(a_days_in_semester, 14, 0, b, c + assignment_group.upper_points - assignment_group.lower_points)

    a_fig.add_trace(
        go.Scatter(
            x=[a_actual_day,a_actual_day+2,a_actual_day+2,a_actual_day,a_actual_day],
            y=[0,0,20,20,0],
            fill="toself",
            mode='lines',
            name='',
            hoverlabel=hover_style,
            text='Dag van snapshot in semester',
            opacity=0
        ),
        row=a_row, col=a_col
    )
    a_fig.add_shape(
        dict(type="rect", x0=a_actual_day, x1=a_actual_day+1, y0=0, y1=200,
             fillcolor="#888888", line_color="#888888"
             ),
        row=a_row,
        col=a_col
    )

    a_fig.update_yaxes(title_text="Punten", range=[0, assignment_group.total_points], row=a_row, col=a_col)

    # teken bandbreedte
    a_fig.add_trace(
        go.Scatter(
            x=x_time + x_time[::-1],  # x, then x reversed
            y=band_upper + band_lower[::-1],  # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ),
        row=a_row, col=a_col
    )


def plot_submissions(a_row, a_col, a_fig, a_perspective, a_start_date, a_days_in_semester):
    x_submission = [0]
    y_submission = [0]
    y_hover = ['Start '+get_date_time_loc(a_start_date)]
    y_colors = [score_dict[-2]['color']]
    y_size = [get_marker_size(False)]
    cum_score = 0
    l_submissions = sorted(a_perspective.submissions, key=lambda s: s.submitted_at)
    for submission in l_submissions:
        y_size.append(get_marker_size(submission.graded))
        x_submission.append(date_to_day(a_start_date, submission.submitted_at))
        if submission.graded:
            cum_score += submission.score
            y_colors.append(fraction_to_level(submission.score/submission.points)['color'])
            hover = submission.assignment_name + "<br>" + fraction_to_level(submission.score/submission.points)['niveau']+" Score: " + str(submission.score)
        else:
            y_colors.append(score_dict[-2]['color'])
            hover = submission.assignment_name + "<br>" + "Nog niet beoordeeld."
        for comment in submission.comments:
            value = comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                hover += "<br>" + line
        y_submission.append(cum_score)
        y_hover.append(hover)

    a_fig.add_trace(
        go.Scatter(
            x=x_submission,
            y=y_submission,
            hoverinfo="text",
            hovertext=y_hover,
            mode='lines+markers',
            marker_color=y_colors,
            line_color="#444444",
            hoverlabel=hover_style,
            marker=dict(
                size=y_size,
                opacity=1.0,
                line=dict(
                    width=2
                )
            )
        ),
        row=a_row, col=a_col
    )
    a_fig.update_xaxes(title_text="Dagen in semester", range=[0, a_days_in_semester], row=a_row, col=a_col)
    return {"x": x_submission, "y": y_submission}


def remove_assignment(a_assignments, a_submission):
    for i in range(0, len(a_assignments)):
        if a_assignments[i].id == a_submission.assignment_id:
            del a_assignments[i]
            return a_assignments


def plot_perspective(a_row, a_col, a_fig, a_assignment_group, a_perspective, a_start_date, a_actual_day, a_days_in_semester):
    l_assignments = a_assignment_group.assignments[:]
    l_missed_submissions = []
    for l_submission in a_perspective.submissions:
        l_assignments = remove_assignment(l_assignments, l_submission)

    #missed assignments
    for l_assignment in l_assignments:
        if date_to_day(a_start_date, l_assignment.assignment_date) < a_actual_day:
            l_submission = Submission(0, l_assignment.group_id, l_assignment.id, 0, l_assignment.name, l_assignment.assignment_date,
                       True, 0, l_assignment.points)
            l_submission.comments.append(Comment(0, "Systeem", l_assignment.assignment_date, "Niets ingeleverd voor de deadline"))
            l_missed_submissions.append(l_submission)
            remove_assignment(l_assignments, l_submission)

    a_perspective.submissions = a_perspective.submissions + l_missed_submissions
    plot_open_assignments(a_row, a_col, a_fig, l_assignments, a_start_date, a_actual_day)
    plot_bandbreedte(a_row, a_col, a_fig, a_assignment_group, a_actual_day, a_days_in_semester)
    plot_submissions(a_row, a_col, a_fig, a_perspective, a_start_date, a_days_in_semester)