import pandas as pd
from scipy.spatial.distance import euclidean as dist
from math import sqrt
from random import shuffle, random
import math as m 
from copy import deepcopy
from operator import itemgetter

class CircleGenerator:
    def _validate_point(self, points, moved_point, moved_point_munber, circle_radius):
        correct_range = [*range(moved_point_munber), *range(moved_point_munber + 1, len(points))]
        for jp in correct_range:
            is_intersect = dist(itemgetter('x', 'y')(moved_point), 
                                itemgetter('x', 'y')(points[jp])) <= 2 * circle_radius
            if is_intersect:
                break        
        return not is_intersect
    
    def shuffle_circles(self, init_points, r, axis_size, square_side):
        points = deepcopy(init_points)
        dr = min(square_side - r, 2 * r)
        n = 30 * int(square_side / dr)
        # n = 0

        for _ in range(n):
            for ip in range(len(points)):
                new_x = points[ip]['x'] + (2 * random() - 1) * dr
                new_y = points[ip]['y'] + (2 * random() - 1) * dr 

                if new_x >= axis_size - r:
                    new_x = axis_size - r

                if new_x <= r:
                    new_x = r

                if new_y >= axis_size - r:
                    new_y = axis_size - r

                if new_y <= r:
                    new_y = r

                moved_point = deepcopy(points[ip])
                moved_point['x'] = new_x
                moved_point['y'] = new_y

                is_valid_motion = self._validate_point(points, moved_point, ip, r)
                if is_valid_motion:
                    points[ip] = moved_point

        return points


    def generate_with_circle_count(self, 
                                circle_radius, 
                                circle_count, 
                                axis_size, 
                                verbose=False):
        self.axis_size = axis_size
        points = []

        root = m.sqrt(circle_count)
        nearest_root = 0
        
        if int(root + 0.5) ** 2 != circle_count:
            nearest_root = int(root + 1)
        else:
            nearest_root = int(root)
            
        self.nearest_root = nearest_root

        drx = axis_size / (2 * nearest_root)
        dry = axis_size / (2 * nearest_root)

        for iy in range(nearest_root):
            for ix in range(nearest_root):
                x = drx + ix * axis_size / nearest_root
                y = dry + iy * axis_size / nearest_root
                points.append({'x': x, 'y': y})

        shuffle(points)
        points = points[:circle_count]
        points = [ {**p, 'index': i} for p, i in zip(points, range(1, circle_count + 1))]

        self.meshed_circles = deepcopy(points)
        shuffled_points = self.shuffle_circles(points, circle_radius, axis_size, drx)
        self.shuffled_circles = deepcopy(shuffled_points)
        return shuffled_points

    def generate_with_circle_percent(self, 
                                    circle_radius, 
                                    circle_count, 
                                    circle_percent, 
                                    max_iteration=1000, attempts=100, 
                                    verbose=False):
        circles_s = circle_count *  m.pi * circle_radius ** 2
        axis_size = sqrt(circles_s / circle_percent)
        shuffled = self.generate_with_circle_count(circle_radius, 
                                                    circle_count, 
                                                    axis_size, 
                                                    verbose)
        return shuffled