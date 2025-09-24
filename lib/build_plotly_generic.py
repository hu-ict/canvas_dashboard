import plotly.graph_objs as go
from lib.lib_bandwidth import calc_dev


def plot_bandbreedte_colored(a_row, a_col, a_fig, a_days, a_bandwidth, a_flow, a_total_points):
    if a_total_points <= 0:
        return
    if a_bandwidth is None:
        return
    band_min = calc_dev(a_days, 0, 0, 0, 0)
    if a_flow:
        band_lower = calc_dev(a_days, 0, 0, 0, 0.3)
        band_upper = calc_dev(a_days, 0, 0, 0, 0.7)
        band_max = calc_dev(a_days, 0, 0, 0, 1)
        l_days = calc_dev(a_days, 0, 0, 1, 0)
    else:
        band_min = calc_dev(a_days, 0, 0, 0, 0)
        band_upper = a_bandwidth.get_uppers()
        band_lower = a_bandwidth.get_lowers()
        band_max = calc_dev(a_days, 0, 0, 0, a_total_points)
        l_days = a_bandwidth.get_days()
    # print("BPG01 - plot_bandbreedte_colored")
    boven_niveau = go.Scatter(
        x=l_days + l_days[::-1],  # x, then x reversed
        y=band_max + band_upper[::-1],  # upper, then lower reversed
        fill='toself',
        fillcolor='rgba(7, 107, 32, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False
    )
    op_niveau = go.Scatter(
        x=l_days + l_days[::-1],  # x, then x reversed
        y=band_upper + band_lower[::-1],  # upper, then lower reversed
        fill='toself',
        fillcolor='rgba(114, 232, 93, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False
    )
    onder_niveau = go.Scatter(
        x=l_days + l_days[::-1],  # x, then x reversed
        y=band_lower + band_min[::-1],  # upper, then lower reversed
        fill='toself',
        fillcolor='rgba(232, 117, 2, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False
    )
    if a_row == 0:
        pass
        # mone graph
        a_fig.add_trace(boven_niveau)
        a_fig.add_trace(op_niveau)
        a_fig.add_trace(onder_niveau)
    else:
        # multigraph
        a_fig.add_trace(boven_niveau, row=a_row, col=a_col)
        a_fig.add_trace(op_niveau, row=a_row, col=a_col)
        a_fig.add_trace(onder_niveau, row=a_row, col=a_col)

