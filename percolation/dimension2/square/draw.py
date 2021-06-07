
import plotly.graph_objects as go
import numpy as np
import random
from scipy.spatial.distance import euclidean as distance
from operator import itemgetter as get 
import json
import math

def generate_accurate_star_points(_star, accuracy = 3):
    (x_arr, y_arr) = generate_star_points(_star)

    accuracy = 3
    x_new_arr = []
    y_new_arr = []
    zip_points = zip(x_arr[:-1], x_arr[1:], 
                     y_arr[:-1], y_arr[1:])

    for (x, x_next, y, y_next) in zip_points:
        dx = (x_next - x) / accuracy
        dy = (y_next - y) / accuracy

        for i in range(accuracy):
            x_new_arr.append(x + i * dx)
            y_new_arr.append(y + i * dy)

    return (x_new_arr,y_new_arr)

def generate_star_points(_star):
    r_inner = _star["r_inner"]
    r_outer = _star["r_outer"]
    phi_0 = _star["phi_0"]
    x = _star["x"]
    y = _star["y"]

    x_arr = []
    y_arr = []
    step = 72

    for i in range(6):
        rads = np.deg2rad(step * i + phi_0)

        x_arr.append(-r_outer*np.sin(rads) + x)
        y_arr.append(r_outer*np.cos(rads) + y)

        rads = np.deg2rad(step * i + 36 + phi_0)

        x_arr.append(-r_inner*np.sin(rads) + x)
        y_arr.append(r_inner*np.cos(rads) + y)

    return (x_arr, y_arr)

def hard_check(_star1, _star2):
    p1arr = generate_accurate_star_points(_star1)
    p2arr = generate_accurate_star_points(_star2)

    dr = ((p1arr[0][1]-p1arr[0][0])**2+
          (p2arr[1][1]-p2arr[1][0])**2)**0.5
    
    for p1 in zip(p1arr[0],p1arr[1]):
        for p2 in zip(p2arr[0],p2arr[1]):
            if distance(p1,p2) < dr:
                return True

    return False

def is_stars_intersect(_star1,_star2):
    center_dist = distance(get("x", "y")(_star1), 
                           get("x", "y")(_star2))

    if (center_dist < _star1["r_inner"]+_star2["r_outer"]):
        return True
    elif (center_dist < _star1["r_outer"]*2):
        return hard_check(_star1, _star2)
    else:
        return False

def get_star_scatter(_star, _type = "simple", accuracy = 3):
    x_arr = []
    y_arr = []
    if _type == "simple": 
        (x_arr, y_arr) = generate_star_points(_star)
    if _type == "accurate":
        (x_arr, y_arr) = generate_accurate_star_points(_star, accuracy)
    return go.Scatter(
        x=x_arr,
        y=y_arr
        )

def generate_stars(count):
    stars = []
    for i in range(p["star_count"]):
        stars.append(
            {
                "phi_0": random.randint(0, 180),
                "r_inner": p["r_inner"],
                "r_outer": p["r_outer"],
                "x": random.randint(0, p["x_max"]),
                "y": random.randint(0, p["y_max"])
            }
        )
    return stars

def solve_intersections(_stars):
    s_intersect = {}
    for s1 in _stars:
        s_intersect_list = []

        for s2 in _stars:
            if s1 != s2 and is_stars_intersect(s1, s2):
                    s_intersect_list.append(s2)

        s_intersect[json.dumps(s1)] = s_intersect_list


    keys = list(s_intersect.keys())
    random.shuffle(keys)
    keys = set(keys)

    final_points = []
    while keys:
        k = keys.pop()
        final_points.append(k)

        for each in s_intersect[k]:
            s_str = json.dumps(each)
            if keys and s_str in keys: keys.remove(json.dumps(each))

    return final_points

def impose_stars_on_figure(_stars, _p, _get_scatter):
    fig = go.Figure(
        layout=go.Layout( 
            width=_p["layout_w"],
            height=_p["layout_h"],
            xaxis={"range": [-_p["r_outer"], _p["x_max"]+_p["r_outer"]]},
            yaxis={"range": [-_p["r_outer"], _p["y_max"]+_p["r_outer"]]},
            )
        )


    for each in stars_without_intersections:
        star_dict = json.loads(each)
        fig.add_trace(_get_scatter(star_dict))
    
    return fig
        
p = {
    "star_count":5,
    "r_inner":3,
    "r_outer":10,
    "x_max":100,
    "y_max":100,
    "layout_w":1000,
    "layout_h":1000,
}

stars = generate_stars(p)
stars_without_intersections = solve_intersections(stars)
fig = impose_stars_on_figure(stars, p, get_star_scatter)

fig.show()