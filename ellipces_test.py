import plotly.graph_objects as go
from numpy import pi,cos,sin,linspace,deg2rad
from scipy.spatial.distance import euclidean as distance 
from random import shuffle
from operator import itemgetter as get
import math as m

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
    print(r1, r2, dist)
    return (r1 + r2) > dist

def get_ellipce_scatter(_ellipse):
    t = linspace(0, 2*pi, 101)
    x0 = _ellipse["a"] * cos(t)
    y0 = _ellipse["b"] * sin(t)

    x_new = []
    y_new = []

    for (x, y) in zip(x0, y0):
        phi = _ellipse["phi_0"]
        x_move = _ellipse["x"]
        y_move = _ellipse["y"]
        rads = deg2rad(phi)
        x_new.append(x*cos(rads)-y*sin(rads)+x_move)
        y_new.append(x*sin(rads)+y*cos(rads)+y_move)

    return go.Scatter(
        x=x_new,
        y=y_new
        )

# ellipses = [
#     {"phi_0": 65, "a": 2, "b": 1, "x": 0, "y": 0},
#     {"phi_0": 50, "a": 2, "b": 1, "x": 2, "y": 3}
# ]

ellipses = [
    {"phi_0": 56, "a": 2, "b": 1, "x": 2, "y": 6},
    {"phi_0": 102, "a": 2, "b": 1, "x": 2, "y": 9}
]

(_phi1, _phi2) = calculate_phi(ellipses[0], ellipses[1])
print(_phi1, _phi2)
print(calculate_r(phi=_phi1, **ellipses[0]))

layout = go.Layout( 
    width=1000,
    height=1000,
    xaxis={"range":[-2, 12]},
    yaxis={"range":[-2, 12]},
)

fig = go.Figure(layout=layout)

print(is_ellipses_intersect(ellipses[0], ellipses[1]))

[
    fig.add_trace(get_ellipce_scatter(e))
    
    for e in ellipses
] 

fig.add_trace(go.Scatter(
    x=[x["x"] for x in ellipses],
    y=[x["y"] for x in ellipses]
))

fig.show()