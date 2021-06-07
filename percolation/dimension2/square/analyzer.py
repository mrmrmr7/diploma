from scipy.spatial.distance import euclidean as dist
from scipy.spatial.distance import euclidean as distance 
import math as m
import random
from operator import itemgetter as get
import numpy as np

class Analyzer:
    def generate_accurate_star_points(self, _star, accuracy = 3):
        (x_arr, y_arr) = self.generate_star_points(_star)

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

    def generate_star_points(self, _star):
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
    
    def hard_check(self, _star1, _star2):
        p1arr = self.generate_accurate_star_points(_star1)
        p2arr = self.generate_accurate_star_points(_star2)

        dr = ((p1arr[0][1]-p1arr[0][0])**2+
            (p2arr[1][1]-p2arr[1][0])**2)**0.5
        
        for p1 in zip(p1arr[0],p1arr[1]):
            for p2 in zip(p2arr[0],p2arr[1]):
                if distance(p1,p2) < dr:
                    return True

        return False
    
    def is_stars_intersect(self, _star1, _star2):
        center_dist = distance(get("x", "y")(_star1), 
                            get("x", "y")(_star2)) * 0.5

        if (center_dist < _star1["r_inner"] + _star2["r_outer"]):
            return True
        elif (center_dist < _star1["r_outer"] * 2):
            return self.hard_check(_star1, _star2)
        else:
            return False
    
    def split_on_clusters(self, stars, coef):
        markers = { i.index: i.index for i in stars }
        for i in range(len(stars)):
            for j in [*range(0, i), *range(i + 1, len(stars))]:
                if stars[i].is_intersect(stars[j]):
                    i_marker = markers[stars[i].index]
                    j_marker = markers[stars[j].index]
                    circles_with_marker_i = [ k for k, v in markers.items() if v == i_marker ]
                    for c in circles_with_marker_i:
                        markers[c] = j_marker
        clusters = { i: [] for i in set(markers.values()) }
        for k, v in markers.items():
            clusters[v] = clusters[v] + [k]
        return clusters
    
    
    def get_clusters_ranges(self, circles, clusters):
        clusters_ranges = { }
        
        for k, v in clusters.items():
            cluster_circles = [ i for i in circles if i.index in v ]
            min_x = min([ c.x for c in cluster_circles ])
            max_x = max([ c.x for c in cluster_circles ])
            min_y = min([ c.y for c in cluster_circles ])
            max_y = max([ c.y for c in cluster_circles ])
            
            clusters_ranges[k] = {  'min_x': min_x, 'max_x': max_x,
                                    'min_y': min_y, 'max_y': max_y, }
            
        return clusters_ranges
        
    def _get_biggest_cluster(self, clusters_ranges): 
        sizes = [(k, v['max_x'] - v['min_x']) for k, v in clusters_ranges.items()]
        return max(sizes, key=lambda x: x[1])
    
    def get_biggest_cluster(self, ellipces, coef):
        clusters = self.split_on_clusters(ellipces, coef)
        clusters_ranges = self.get_clusters_ranges(ellipces, clusters)
        biggest_cluster_number = self._get_biggest_cluster(clusters_ranges)

        cluster_max = [biggest_cluster_number[0], *(clusters[biggest_cluster_number[0]])]
        biggest_cluster = [ c for c in ellipces if c.index in cluster_max]
        
        return biggest_cluster, { 'size': biggest_cluster_number[1] }