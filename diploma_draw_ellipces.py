import plotly.graph_objects as go
import pandas as pd
from numpy.random import rand 
from scipy.spatial.distance import euclidean as distance 
from math import sqrt
from random import shuffle


def calculate_r(phi, phi_0, a, b, **kvargs):
    phi_actual_rad = (phi + phi_0) * pi / 180.0
    return (a * b)/sqrt((b * cos(phi_actual_rad)) ** 2 + (a * sin(phi_actual_rad)) ** 2)

def calculate_phi(e1, e2):
    e1e2_tan = (e2["y"]-e1["y"]) / (e2["x"]-e1['x'])
    tan_phi = atan(e1e2_tan) * 180.0 / pi
    e1_phi = 180.0 - tan_phi + e1["phi_0"]
    e2_phi = tan_phi - e2["phi_0"]
    return (e1_phi, e2_phi)

def ellipce_dist(ellipce_1, ellipce_2):
    return distance(get("x", "y")(ellipce_1), 
                    get("x", "y")(ellipce_2))

def is_ellipces_intersect(ellipce_1, ellipce_2):
    (e1_phi, e2_phi) = calculate_phi(ellipce1, ellipce2)
    r1 = calculate_r(phi=e1_phi, **ellipce1)
    r2 = calculate_r(phi=e2_phi, **ellipce1)
    return (r1 + r2) * 1.1 >= ellipce_dist(ellipce1, ellipce2)


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