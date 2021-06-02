import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean as distance
from random import shuffle, random
import math as m
import random
from operator import itemgetter as get
from copy import deepcopy
import json
from scipy.spatial.distance import euclidean as dist
from operator import itemgetter


class Generator:
    def calculate_r(self, phi, phi_0, a, b, **kvargs):
        phi_actual_rad = phi * m.pi / 180.0
        return (a * b) / m.sqrt(b**2 * m.cos(phi_actual_rad) ** 2 + a ** 2 * m.sin(phi_actual_rad) ** 2)

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
        return (r1 + r2) > dist

    def _validate_point(self, points, moved_point, moved_point_munber):
        correct_range = [*range(moved_point_munber),
                         *range(moved_point_munber + 1, len(points))]
        is_intersect = False
        for jp in correct_range:
            is_intersect = self.is_ellipses_intersect(moved_point, points[jp])
            if is_intersect:
                break
        return not is_intersect

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

    def generate_elements(self,
                          ellipce_count,
                          a,
                          b,
                          axis_size):
        result = []

        x_ellipce_count = int(axis_size // (2 * b))
        y_ellipce_count = int(axis_size // (2 * a))

        for ix in range(x_ellipce_count):
            for iy in range(y_ellipce_count):
                result.append({
                    "phi_0": 0,
                    "a": a,
                    "b": b,
                    "x": iy * 2 * a + a,
                    "y": ix * 2 * b + b,
                })

        result_shuffled = deepcopy(result)
        shuffle(result_shuffled)
        result_shuffled = result_shuffled[:ellipce_count]
        zip_ellipce_with_index = zip(
            result_shuffled, range(len(result_shuffled)))
        return result, [{**e, 'index': index + 1} for (e, index) in zip_ellipce_with_index]
    
    
    def _extend_tighest_circles(self, circles, a, b, axis_size):
        tighest_circles = deepcopy(circles)

        axis_max = {
            'x': max([p['x'] for p in tighest_circles]) + a, 
            'y': max([p['y'] for p in tighest_circles]) + b
            }

        aspect = {
            'x': axis_size / axis_max['x'],
            'y': axis_size / axis_max['y'],
        }

        extended_circles = [ { 
                **c, 
                'x': c['x'] * aspect['x'], 
                'y': c['y'] * aspect['y']
            } for c in tighest_circles ]

        self.extended_circles = extended_circles
        return extended_circles

    def generate_with_ellipce_count(self,
                                    ellipce_count,
                                    a,
                                    b,
                                    axis_size):
        init_ellipces, selected_ellipces = self.generate_elements(
            ellipce_count, a, b, axis_size)
        
        selected_ellipces = self._extend_tighest_circles(selected_ellipces, a, b, axis_size)
        
        shuffled_ellipces = deepcopy(selected_ellipces)
        shuffles_count = 20
        dr_x = a
        dr_y = a

        for _ in range(shuffles_count):
            for ip in range(len(shuffled_ellipces)):
                ellipce_to_shuffle = shuffled_ellipces[ip]
                
                new_x = ellipce_to_shuffle['x'] + (2 * random.random() - 1) * dr_x
                new_y = ellipce_to_shuffle['y'] + (2 * random.random() - 1) * dr_y
                new_phi = ellipce_to_shuffle['phi_0'] # + random.randint(-30, 30) 
                
                if new_x >= axis_size - a:
                    new_x = axis_size - a

                if new_x <= a:
                    new_x = a

                if new_y >= axis_size - a:
                    new_y = axis_size - a

                if new_y <= a:
                    new_y = a

                moved_point = deepcopy(ellipce_to_shuffle)
                moved_point['x'] = new_x
                moved_point['y'] = new_y
                moved_point['phi_0'] = new_phi

                is_valid_motion = self._validate_point(
                    shuffled_ellipces, moved_point, ip)
                if is_valid_motion:
                    shuffled_ellipces[ip] = moved_point

        return shuffled_ellipces, selected_ellipces, init_ellipces 

    def generate_with_ellipce_percent(self,
                                      ellipce_count,
                                      ellipce_percent,
                                      a,
                                      b):
        ellipce_s = ellipce_count * m.pi * a * b
        axis_size = m.sqrt(ellipce_s / ellipce_percent)
        shuffled_ellipces, selected_ellipces, init_ellipces = self.generate_with_ellipce_count(
            ellipce_count, a, b, axis_size)
        
        return axis_size, shuffled_ellipces, selected_ellipces, init_ellipces
