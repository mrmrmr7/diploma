import plotly.graph_objects as go
import os
from pprint import pprint

x_arr = []
y_arr = []
y_str = []

with open(os.path.abspath(os.getcwd()) + '/display/to_display', 'r') as f:
    n = 0.01
    for line in f.readlines():
        print(line)
        parsed = line.replace('\n', '').split(":")
        print(parsed)
        x_arr.append(float(parsed[0]))
        y_arr.append(float(parsed[1]))
        y_str.append(parsed[1])
        n += 0.002

pprint(list(zip(x_arr, y_arr, y_str)))
scatter = go.Scatter(
    x=x_arr,
    y=y_arr,
    line={"width": 6, "color": "black"}
)
fig = go.Figure(data=scatter,
)

fig.update_xaxes(showgrid=True, gridwidth=2, gridcolor='Gray')
fig.update_yaxes(showgrid=True, gridwidth=2, gridcolor='Gray')
fig.update_xaxes(showline=True, linewidth=10, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=10, linecolor='black', mirror=True)
fig.update_layout(paper_bgcolor='rgb(255,255,255)',
    plot_bgcolor='rgb(255,255,255)')
fig.update_layout(font_size=34)

fig.show()
