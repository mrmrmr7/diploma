import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean as distance
import math as m
import random
from operator import itemgetter as get
import json


class Generator:
    def calculate_r(self, phi, phi_0, a, b, **kvargs):
        phi_actual_rad = phi * m.pi / 180.0
        return (a * b)/m.sqrt(b**2 * m.cos(phi_actual_rad)**2 + a**2 * m.sin(phi_actual_rad)**2)

    def calculate_phi(self, _ellipse1, _ellipse2):
        dx = _ellipse2['x']-_ellipse1['x']
        dy = _ellipse2['y']-_ellipse1['y']

        if dx == 0:
            return (90 + _ellipse1["phi_0"], 90 + _ellipse2["phi_0"])

        e1e2_tan = dy/dx
        tan_phi = m.atan(e1e2_tan) * 180.0 / m.pi
        e1_phi = 180.0 - tan_phi + _ellipse1["phi_0"]
        e2_phi = tan_phi - _ellipse2["phi_0"]

        e1_phi = e1_phi if e1_phi < 0 else e1_phi - 180
        e2_phi = e2_phi if e2_phi < 0 else e2_phi - 180
        return (e1_phi, e2_phi)

    def ellipse_dist(self, _ellipse1, _ellipse2):
        return distance(get("x", "y")(_ellipse1),
                        get("x", "y")(_ellipse2))

    def is_ellipses_intersect(self, _ellipse1, _ellipse2):
        (e1_phi, e2_phi) = self.calculate_phi(_ellipse1, _ellipse2)
        r1 = self.calculate_r(phi=e1_phi, **_ellipse1)
        r2 = self.calculate_r(phi=e2_phi, **_ellipse2)
        dist = self.ellipse_dist(_ellipse1, _ellipse2)
        return (r1 + r2) * 1.5 > dist

    def get_ellipce_scatter(self, _ellipse):
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

        return go.Scatter(x=x_new, y=y_new)

    def generate_with_ellipce_count(self,
                                    circle_count,
                                    axis_size,
                                    a,
                                    b):
        ellipses = []

        for _ in range(circle_count):
            ellipses.append({
                "phi_0": random.randint(0, 179),
                "a": a,
                "b": b,
                "x": random.random() * (axis_size - 2 * a) + a,
                "y": random.random() * (axis_size - 2 * a) + a,
            })

        e_intersect = {}
        for e1 in ellipses:
            e_intersect_list = []

            for e2 in ellipses:
                if e1 != e2 and self.is_ellipses_intersect(e1, e2):
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
                if keys and e_str in keys:
                    keys.remove(json.dumps(each))

        parsed = [json.loads(each) for each in final_points]
        zip_ellipce_with_index = zip(parsed, range(len(parsed)))
        return [{**e, 'index': index + 1} for (e, index) in zip_ellipce_with_index]
