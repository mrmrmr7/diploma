from percolation.dimension2.square.object import Square
import plotly.graph_objects as go
import numpy as np
import random
from scipy.spatial.distance import euclidean as distance
from operator import itemgetter as get 
import json
import math

class Generator:
    def generate_accurate_star_points(self, _star, accuracy = 5):
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
                               get("x", "y")(_star2))

        if (center_dist < _star1["r_inner"]+_star2["r_outer"]):
            return True
        elif (center_dist < _star1["r_outer"]*2):
            return self.hard_check(_star1, _star2)
        else:
            return False

    def generate_elements(self, count):
        items = []
        for i in range(self.p["item_count"]):
            x = random.randint(0, self.p["x_max"])
            y = random.randint(0, self.p["x_max"])
            phi = random.randint(0, 180)
            index = i
            items.append(Square(x, y, self.p['a'], phi, index))
        return items

    def solve_intersections(self, _items):
        items_intersect = {}
        for s1 in _items:
            items_intersect_list = []

            for s2 in _items:
                if s1.index != s2.index and s1.is_intersect(s2):
                    items_intersect_list.append(s2.index)

            items_intersect[s1.index] = items_intersect_list


        keys = list(items_intersect.keys())
        random.shuffle(keys)
        keys = set(keys)

        final_points = []
        while keys:
            k = keys.pop()
            final_points.append(k)

            for each in items_intersect[k]:
                if keys and each in keys: keys.remove(each)

        return final_points
    
    def generate_elements_with_given_axis_size(self, a, item_count, axis_size):
        self.p={
            "item_count": item_count,
            "a": a,
            "x_max": axis_size,
            "y_max": axis_size,
            "layout_w": 1000,
            "layout_h": 1000,
        }

        items = self.generate_elements(self.p)
        squares_without_intersections = self.solve_intersections(items)
        
        parsed = [ each for each in items if each.index in squares_without_intersections ]
        return parsed
