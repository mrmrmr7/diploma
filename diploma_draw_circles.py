import plotly.graph_objects as go
import pandas as pd
from numpy.random import rand 
from scipy.spatial.distance import euclidean as distance 
from math import sqrt
from random import shuffle

p_radius = 0.2
p_count = 2000

ax_size = 10
square_vertex_size = 1000

points = list(zip(rand(p_count) * ax_size, rand(p_count) * ax_size)) 

p_intersect = {}
for p1 in points:
    p_intersect_list = []

    for p2 in points:
        diff_points = p1 != p2
        too_close = distance(p1, p2) < 2 * p_radius

        if diff_points and too_close:
                p_intersect_list.append(p2)

    p_intersect[p1] = p_intersect_list

keys = list(p_intersect.keys())
shuffle(keys)
keys = set(keys)

final_points = []
while len(keys) > 0:
    k = keys.pop()
    final_points.append(k)
    keys = keys.difference(p_intersect[k])
    
shapes = [
    {
        "type":"circle",
        "xref":"x",
        "yref":"y",
        "x0":(x-p_radius),
        "x1":(x+p_radius),
        "y0":(y-p_radius),
        "y1":(y+p_radius),
        "line_color":"LightSeaGreen",
    }

    for (x, y) in final_points
]

layout = go.Layout( 
    width=1000,
    height=1000,
    shapes=shapes,
    xaxis={"range":[-p_radius, ax_size + p_radius]},
    yaxis={"range":[-p_radius, ax_size + p_radius]}
)

fig = go.Figure(layout=layout)

fig.show()