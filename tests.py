
import random
import numpy as np
from scipy.spatial import distance
from math import sin,cos,sqrt,pi,atan
from operator import itemgetter as get
from scipy.spatial.distance import euclidean as distance 

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

ellipce1 = {
    "phi_0": 0,
    "a": 4, 
    "b": 2,
    "x": 0,
    "y": 0,
}

ellipce2 = {
    "phi_0": 45,
    "a": 4,
    "b": 2,
    "x": -1,
    "y": -5
}   


print(is_ellipces_intersect(ellipce1, ellipce2))
