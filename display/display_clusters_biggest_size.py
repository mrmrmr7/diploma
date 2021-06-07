import plotly.graph_objects as go
import os
from pprint import pprint
import json

x_arr = []
y_arr = []
y_str = []

with open('output/2d/ellipce/biggest_cluster/clusters_save_2.txt', 'r') as f:
    lines = f.readlines()
    points = json.loads(lines[2])
    repeats = int(lines[0])
    
    for (x, y) in points.items():
        x_arr.append(float(x))
        y_arr.append(float(y/repeats/1000.0))
        y_str.append(y)
    

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