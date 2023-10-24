import textwrap

from lib.lib_date import date_to_day, get_date_time_loc
from lib.lib_plotly import get_marker_size, fraction_to_level, hover_style, score_dict, fraction_to_bin_level, score_bin_dict
import plotly.graph_objs as go

from lib.lib_submission import NOT_GRADED


def get_hover(a_peil_submissions):
    score = 0.1
    hover = "Geen data"
    if a_peil_submissions:
        if a_peil_submissions.graded:
            score = a_peil_submissions.score + 1
        if "Beoordeling".lower() in a_peil_submissions.assignment_name.lower():
            hover = "<b>"+a_peil_submissions.assignment_name + "</b> - " + score_dict[int(score - 1)]['beoordeling']
        else:
            hover = "<b>"+a_peil_submissions.assignment_name + "</b> - " + score_dict[int(score-1)]["voortgang"]
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
            #Heeft beoordeling
            series['size'].append(get_marker_size(True)+2)
            series['hover'].append(get_hover(pleiling['submission']))
            series['x'].append(date_to_day(a_start_date, pleiling['submission'].submitted_at))
            if "Beoordeling".lower() in pleiling['assignment'].name.lower():
                series['color'].append(score_dict["beoordeling"][int(pleiling['submission'].score)]['color'])
            else:
                series['color'].append(score_dict["voortgang"][int(pleiling['submission'].score)]['color'])
        else:
            #Heeft nog geen beoordeling
            series['size'].append(get_marker_size(False)+2)
            series['hover'].append("<b>"+pleiling['assignment'].name + "</b> (" + get_date_time_loc(pleiling['assignment'].assignment_date) + ")")
            series['x'].append(date_to_day(a_start_date, pleiling['assignment'].assignment_date))
            if "Beoordeling".lower() in pleiling['assignment'].name.lower():
                series['color'].append(score_dict["beoordeling"][-1]['color'])
            else:
                series['color'].append(score_dict["voortgang"][-1]['color'])
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
        series['color'].append(score_dict["team"][-1]['color'])
        series['hover'].append("<b>"+assignment.name + "</b> ("+str(assignment.points)+" punten, deadline: " + get_date_time_loc(assignment.assignment_date) + ")")
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


def plot_bandbreedte(a_row, a_col, a_fig, assignment_group, a_actual_day, a_actual_date, a_progress):
    if assignment_group.total_points <= 0:
        return

    a_fig.add_trace(
        go.Scatter(
            x=[a_actual_day ,a_actual_day+2, a_actual_day+2, a_actual_day, a_actual_day],
            y=[0, 0, assignment_group.total_points, assignment_group.total_points, 0],
            fill="toself",
            mode='lines',
            name='',
            hoverlabel=hover_style,
            text=f"Dag van snapshot in semester: {a_actual_day} [{a_actual_date}]",
            opacity=0
        ),
        row=a_row, col=a_col
    )
    l_color = score_dict['voortgang'][int(a_progress)]['color']
    a_fig.add_shape(
        dict(type="rect", x0=a_actual_day, x1=a_actual_day+1, y0=0, y1=assignment_group.total_points,
             fillcolor=l_color, line_color=l_color
             ),
        row=a_row,
        col=a_col
    )

    a_fig.update_yaxes(title_text="Punten", range=[0, assignment_group.total_points], row=a_row, col=a_col)

    # teken bandbreedte
    a_fig.add_trace(
        go.Scatter(
            x=assignment_group.bandwidth.days + assignment_group.bandwidth.days[::-1],  # x, then x reversed
            y=assignment_group.bandwidth.uppers + assignment_group.bandwidth.lowers[::-1],  # upper, then lower reversed
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
    y_hover = ['<b>Start</b> '+get_date_time_loc(a_start_date)]
    y_colors = [score_dict[a_perspective.name][-2]['color']]
    y_size = [get_marker_size(False)]
    cum_score = 0
    l_last_graded_day = 0
    l_submissions = sorted(a_perspective.submissions, key=lambda s: s.submitted_date)
    for submission in l_submissions:
        y_size.append(get_marker_size(submission.graded))
        l_day = date_to_day(a_start_date, submission.submitted_date)
        x_submission.append(l_day)
        l_hover = "<b>"+submission.assignment_name + "</b> ("+str(submission.points)+" punten, deadline: " + get_date_time_loc(submission.assignment_date) + ")"

        if submission.graded:
            if l_day > l_last_graded_day:
                l_last_graded_day = l_day
            cum_score += submission.score
            if submission.points <= 1.1:
                y_colors.append(score_bin_dict[a_perspective.name][fraction_to_bin_level(submission.score / submission.points)]['color'])
                l_hover += "<br><b>" + score_bin_dict[a_perspective.name][fraction_to_bin_level(submission.score / submission.points)]['niveau'] + "</b>, score: " + str(submission.score) + " [" + get_date_time_loc(submission.submitted_date) + "]"
            else:
                y_colors.append(score_dict[a_perspective.name][fraction_to_level(submission.score/submission.points)]['color'])
                l_hover += "<br><b>" + score_dict[a_perspective.name][fraction_to_level(submission.score/submission.points)]['niveau']+"</b>, score: " + str(submission.score) + " [" + str(submission.points) + "]" + " - " + get_date_time_loc(submission.submitted_date)
        else:
            y_colors.append(score_dict[a_perspective.name][-2]['color'])
            l_hover += "<br><b>" + NOT_GRADED + "</b> - " + get_date_time_loc(submission.submitted_date)
        for comment in submission.comments:
            value = get_date_time_loc(comment.date) + " - " + comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                l_hover += "<br>" + line
        y_submission.append(cum_score)
        y_hover.append(l_hover)

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
    return a_assignments

def plot_perspective(a_row, a_col, a_fig, a_assignment_group, a_perspective, a_peil_construction,
                     a_start_date, a_actual_day, a_days_in_semester, a_actual_date):
    l_assignments = a_assignment_group.assignments[:]
    l_missed_submissions = []
    for l_submission in a_perspective.submissions:
        l_assignments = remove_assignment(l_assignments, l_submission)

    a_perspective.submissions = a_perspective.submissions + l_missed_submissions
    plot_progress(a_row, a_col, a_fig, a_peil_construction[a_perspective.name], a_start_date)
    plot_open_assignments(a_row, a_col, a_fig, l_assignments, a_start_date, a_actual_day)
    plot_bandbreedte(a_row, a_col, a_fig, a_assignment_group, a_actual_day, a_actual_date, a_perspective.progress)
    plot_submissions(a_row, a_col, a_fig, a_perspective, a_start_date, a_days_in_semester)
