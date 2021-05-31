from scipy.spatial.distance import euclidean as dist
from scipy.spatial.distance import euclidean as distance 
import math as m
import random
from operator import itemgetter as get


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

def is_ellipses_intersect(_ellipse1, _ellipse2, coef):
    (e1_phi, e2_phi) = calculate_phi(_ellipse1, _ellipse2)
    r1 = calculate_r(phi=e1_phi, **_ellipse1)
    r2 = calculate_r(phi=e2_phi, **_ellipse2)
    dist = ellipse_dist(_ellipse1, _ellipse2)
    return (r1 + r2) * coef > dist
    
def split_on_clusters(ellipces, coef):
    # zip_ellipce_with_index = zip(ellipces_without_index, range(len(ellipces_without_index)))
    # ellipces = [ {**e, 'index': index + 1} for (e, index) in zip_ellipce_with_index]
    # print(ellipces)
    # print(zip_ellipce_with_index)
    markers = { i['index']: i['index'] for i in ellipces }
    for i in range(len(ellipces)):
        for j in [*range(0, i), *range(i + 1, len(ellipces))]:
            if is_ellipses_intersect(ellipces[i], ellipces[j], coef):
                i_marker = markers[ellipces[i]['index']]
                j_marker = markers[ellipces[j]['index']]
                circles_with_marker_i = [ k for k, v in markers.items() if v == i_marker ]
                for c in circles_with_marker_i:
                    markers[c] = j_marker
    clusters = { i: [] for i in set(markers.values()) }
    for k, v in markers.items():
        clusters[v] = clusters[v] + [k]
    return clusters


def get_clusters_ranges(circles, clusters):
    clusters_ranges = { }
    
    for k, v in clusters.items():
        cluster_circles = [ i for i in circles if i['index'] in v ]
        min_x = min([ c['x'] for c in cluster_circles ])
        max_x = max([ c['x'] for c in cluster_circles ])
        min_y = min([ c['y'] for c in cluster_circles ])
        max_y = max([ c['y'] for c in cluster_circles ])
        
        clusters_ranges[k] = {  'min_x': min_x, 'max_x': max_x,
                                'min_y': min_y, 'max_y': max_y, }
        
    return clusters_ranges
    
def get_biggest_cluster(clusters_ranges): 
    sizes = [(k, v['max_x'] - v['min_x']) for k, v in clusters_ranges.items()]
    return max(sizes, key=lambda x: x[1])