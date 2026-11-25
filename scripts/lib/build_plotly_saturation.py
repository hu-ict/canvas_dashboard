import plotly.graph_objects as go

from scripts.lib.plot_totals import SATURATION_PLOTLY_HTML

traces = {'high': {'title': "Hoogste", 'color': 'purple'},
          'plus_stdv': {'title': "Plus_1_stdv", 'color': 'blue'},
          'average': {'title': "Gemiddelde", 'color': 'green'},
          'min_stdv': {'title': "Min_1_stdv", 'color': 'orange'},
          'low': {'title': "Laagste", 'color': 'red'}}

def get_plots():
    return {
        "LU1": {'y_ax_title': 'Observaties', 'title': "LU1 - Onderzoekend vermogen"},
        "LU2": {'y_ax_title': 'Observaties', 'title': "LU2 - Organiserend vermogen"},
        "LU3": {'y_ax_title': 'Observaties', 'title': "LU3 - Interactief vermogen"},
        "LU4": {'y_ax_title': 'Observaties', 'title': "LU4 - Lerend vermogen"},
        "LU5": {'y_ax_title': 'Observaties', 'title': "LU5 - Vakkundigheid"}
    }

def process_plotly_single_saturation(instance, saturation_learning_outcomes, y_max):
    plots = get_plots()
    # print("BPS07 - learning_outcomes:", len(saturation_learning_outcomes))
    for saturation_learning_outcome in saturation_learning_outcomes:
        # print("BPS08 - saturation_learning_outcome", saturation_learning_outcome)
        # print("BPS09 - saturation_statistics", saturation_learning_outcome.get_day(80))
        plot = plots[saturation_learning_outcome.id]
        fig = go.Figure()
        fig.update_layout(title="Verloop in de tijd - "+plot['title'], height=400, width=600, showlegend=True)
        fig.update_yaxes(title_text=plot["y_ax_title"], range=[0, y_max])
        fig.update_xaxes(title_text='Dag in semester')
        x_values = []
        for day in saturation_learning_outcome.days:
            x_values.append(day.day)
        for trace in traces:
            y_values = []
            for day in saturation_learning_outcome.days:

                if trace == "high":
                    y_values.append(day.high)
                elif trace == "plus_stdv":
                    y_values.append(day.plus_stdv)
                elif trace == "average":
                    y_values.append(day.average)
                elif trace == "min_stdv":
                    y_values.append(day.min_stdv)
                elif trace == "low":
                    y_values.append(day.low)
            # print("BPS11 - x_values:", x_values)
            # print("BPS12 - y_values:", y_values)
            scatter_trace = go.Scatter(
                x=x_values,
                y=y_values,
                mode="lines",
                line=dict(
                    width=4,
                    color=traces[trace]['color']
                ),
                name=traces[trace]['title']
            )
            # print("BPS13 - positions:", learning_outcome['id'])
            fig.add_trace(scatter_trace)
        file_name = instance.get_temp_path() + "saturation_" + saturation_learning_outcome.id + ".html"
        # print("BPS14 -", file_name)
        fig.write_html(file_name, include_plotlyjs="cdn")


def process_plotly_single_distribution(instance, saturation_learning_outcomes, y_max, day_max):
    plots = get_plots()
    for saturation_learning_outcome in saturation_learning_outcomes:
        plot = plots[saturation_learning_outcome.id]
        fig = go.Figure()
        fig.update_layout(title="Verdeling - "+plot['title'], height=400, width=500, showlegend=True)
        fig.update_xaxes(title_text='Aantal observaties', range=[0, y_max])
        fig.update_yaxes(title_text='Aantal studenten')
        data = saturation_learning_outcome.last_day_collection
        histogram_trace = go.Histogram(
                x=data,
                name="Dag "+str(day_max),
                xbins=dict(start=0, end=y_max, size=1)
            )

        # print("BPS12 - positions:", learning_outcome['id'])
        fig.add_trace(histogram_trace)
        file_name = instance.get_temp_path() + "distribution_" + saturation_learning_outcome.id + ".html"
        # print("BPS16 -", file_name)
        fig.write_html(file_name, include_plotlyjs="cdn")

def proces_student_saturations(instance, student_saturations, progress_levels):
    y_counts = []
    x_labels = []
    y_colors = []
    y_hover = []
    fig = go.Figure()
    fig.update_layout(title="Saturatie klasse", height=500, width=800, showlegend=True)
    fig.update_yaxes(title_text="Aantal studenten")

    x_labels.append("5 LU Low Saturation")
    y_counts.append(student_saturations['1'])
    y_colors.append(progress_levels.grades[str(1)].color)

    x_labels.append("4 LU Low Saturation")
    y_counts.append(student_saturations['2'])
    y_colors.append(progress_levels.grades[str(1)].color)

    x_labels.append("3 LU Low Saturation")
    y_counts.append(student_saturations['3'])
    y_colors.append(progress_levels.grades[str(1)].color)

    x_labels.append("2 LU Low Saturation")
    y_counts.append(student_saturations['4'])
    y_colors.append(progress_levels.grades[str(1)].color)

    x_labels.append("1 LU Low Saturation")
    y_counts.append(student_saturations['5'])
    y_colors.append(progress_levels.grades[str(1)].color)

    x_labels.append("5 LU Medium Saturation")
    y_counts.append(student_saturations['6'])
    y_colors.append(progress_levels.grades[str(2)].color)

    x_labels.append("5 LU High Saturation")
    y_counts.append(student_saturations['7'])
    y_colors.append(progress_levels.grades[str(3)].color)

    fig.add_trace(go.Bar(x=x_labels,
                         y=y_counts,
                         text=y_counts,
                         marker=dict(color=y_colors)))

    file_name = instance.get_html_general_path() + "portfolio_item_saturation.html"

    print("BPS14 -", file_name)
    fig.write_html(file_name, include_plotlyjs="cdn")

def proces_portfolio_saturation(instance, portfolio_saturation):
    y_counts = []
    x_labels = []
    y_colors = []
    y_hover = []
    for portfolio_item in portfolio_saturation.values():
        x_labels.append(portfolio_item.name)
        y_counts.append(portfolio_item.get_average_lu())
        y_hover.append(str(portfolio_item.get_average_lu()))

    # y_marker_symbols = []
    fig = go.Figure()
    fig.update_layout(title="Portfolio-item saturatie", height=800, width=800, showlegend=True)
    fig.update_yaxes(title_text="Saturatie")

    fig.add_trace(
        go.Scatter(
            x=x_labels,
            y=y_counts,
            hoverinfo="text",
            hovertext=y_hover,
            mode='lines+markers',
            line_color="#444444",
            marker=dict(
                size=12,
                opacity=1.0,
                line=dict(width=2)
            )
        )
    )
    file_name = instance.get_html_general_path() + SATURATION_PLOTLY_HTML
    print("BPS15 -", file_name)
    fig.write_html(file_name, include_plotlyjs="cdn")

def proces_portfolio_teacher_saturation(instance, teacher, x_labels, y_counts, y_hover):
    # y_marker_symbols = []
    fig = go.Figure()
    fig.update_layout(title="Portfolio-item saturatiequotient "+teacher.name, height=800, width=800, showlegend=True)
    fig.update_yaxes(title_text="Saturatiequotient", range=[-1, 1])
    fig.add_trace(
        go.Scatter(
            x=x_labels,
            y=y_counts,
            hoverinfo="text",
            hovertext=y_hover,
            mode='lines+markers',
            line_color="#444444",
            marker=dict(
                size=12,
                opacity=1.0,
                line=dict(width=2)
            )
        )
    )
    file_name = instance.get_html_general_path() + "teacher_saturation_" + teacher.initials + ".html"
    print("BPS15 -", file_name)
    fig.write_html(file_name, include_plotlyjs="cdn")