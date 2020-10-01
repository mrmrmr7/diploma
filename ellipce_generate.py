import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean as distance 
import math as m
import random
from operator import itemgetter as get
from scipy.spatial.distance import euclidean as distance 
import json

def calculate_r(phi, phi_0, a, b, **kvargs):
    phi_actual_rad = phi * m.pi / 180.0
    return (a * b)/m.sqrt(b**2 * m.cos(phi_actual_rad)**2 + a**2 * m.sin(phi_actual_rad)**2)

def calculate_phi(_ellipse1, _ellipse2):
    dx = _ellipse2['x']-_ellipse1['x']
    dy = _ellipse2['y']-_ellipse1['y']

    if dx == 0: return (90 + _ellipse1["phi_0"], 90 + _ellipse2["phi_0"])

    e1e2_tan = dy/dx
    tan_phi = m.atan(e1e2_tan) * 180.0 / m.pi
    e1_phi = 180.0 - tan_phi + _ellipse1["phi_0"]
    e2_phi = tan_phi - _ellipse2["phi_0"]

    e1_phi = e1_phi if e1_phi < 0 else e1_phi - 180
    e2_phi = e2_phi if e2_phi < 0 else e2_phi - 180
    return (e1_phi, e2_phi)

def ellipse_dist(_ellipse1, _ellipse2):
    return distance(get("x", "y")(_ellipse1), 
                    get("x", "y")(_ellipse2))

def is_ellipses_intersect(_ellipse1, _ellipse2):
    (e1_phi, e2_phi) = calculate_phi(_ellipse1, _ellipse2)
    r1 = calculate_r(phi=e1_phi, **_ellipse1)
    r2 = calculate_r(phi=e2_phi, **_ellipse2)
    dist = ellipse_dist(_ellipse1, _ellipse2)
    return (r1 + r2) * 1.1 > dist

def get_ellipce_scatter(_ellipse):
    t = np.linspace(0, 2*np.pi, 101)
    x0 = _ellipse["a"] * np.cos(t)
    y0 = _ellipse["b"] * np.sin(t)

    x_new = []
    y_new = []

    for (x, y) in zip(x0, y0):
        phi = _ellipse["phi_0"]
        x_move = _ellipse["x"]
        y_move = _ellipse["y"]
        rads = np.deg2rad(phi)
        x_new.append(x*np.cos(rads)-y*np.sin(rads)+x_move)
        y_new.append(x*np.sin(rads)+y*np.cos(rads)+y_move)

    return go.Scatter(
        x=x_new,
        y=y_new
        )

a = 2
b = 1

p_count = 300
ax_size = 100
square_vertex_size = 1000

ellipses = []

for _ in range(p_count):
    ellipses.append({
        "phi_0": random.randint(0, 179),
        "a": a, 
        "b": b,
        "x": random.randint(0, ax_size),
        "y": random.randint(0, ax_size),
        })

# print("Init points:")
# print("\n".join(map(str, ellipses)))

e_intersect = {}
for e1 in ellipses:
    e_intersect_list = []

    for e2 in ellipses:
        if e1 != e2 and is_ellipses_intersect(e1, e2):
                e_intersect_list.append(e2)

    e_intersect[json.dumps(e1)] = e_intersect_list


keys = list(e_intersect.keys())
random.shuffle(keys)
keys = set(keys)

final_points = []
while keys:
    k = keys.pop()
    final_points.append(k)

    for each in e_intersect[k]:
        e_str = json.dumps(each)
        if keys and e_str in keys: keys.remove(json.dumps(each))


layout = go.Layout( 
    width=1000,
    height=1000,
    xaxis={"range": [-2, 102]},
    yaxis={"range": [-2, 102]},
)

fig = go.Figure(layout=layout)

# print("Final points:")
# print("\n".join(map(str, final_points)))

for each in final_points:
    ellipse_dict = json.loads(each)
    fig.add_trace(get_ellipce_scatter(ellipse_dict))

fig.show()