import pandas as pd
from scipy.spatial.distance import euclidean as distance 
from math import sqrt
from random import shuffle, random
import math as m 

class CircleGenerator:
    def _validate_point(self, circle_radius, points, new_point):
        is_point_intersect = False
        for point in points:
            is_point_intersect = distance(point, new_point) < 2 * circle_radius
            if is_point_intersect: 
                break
        return not is_point_intersect

        
    def generate_with_circle_count(self, 
                                circle_radius, 
                                circle_count,
                                axis_size,
                                max_iteration=1000,
                                attempts=100,
                                verbose=False):
        res_points = []
        attempt = 0
        max_located_circles_count = 0
        total_iterations = 0

        while attempt < attempts:
            attempt += 1
            if verbose: print(f"Attempt: {attempt} of {attempts}")
            
            points = []
            located_circles_count = 0
            iteration = 0

            while (located_circles_count < circle_count and iteration < max_iteration):
                new_point = (random() * (axis_size - 2 * circle_radius) + circle_radius, 
                            random() * (axis_size - 2 * circle_radius) + circle_radius)

                is_point_valid = self._validate_point(circle_radius, points, new_point)

                if is_point_valid:
                    points.append(new_point)
                    located_circles_count += 1

                iteration +=1 
            
            total_iterations += iteration

            if max_located_circles_count <= located_circles_count:
                max_located_circles_count = located_circles_count

            if located_circles_count == circle_count:
                res_points = points
                break


        if verbose: print(f"""
        \rTotal info:
        \r\tSpent attempts: {attempt}
        \r\tSpent iterations: {iteration}
        \r\tTotal iterations: {total_iterations}
        \r\tMax located circles: {max_located_circles_count}
        """.strip())

        if not res_points:
            raise Exception(f"{max_iteration} iterations is not enough to " +
                            f"set {circle_count} circles with size {circle_radius} in {axis_size} space")
        
        return res_points

    def generate_with_circle_percent(self, circle_radius, circle_count, circle_percent, max_iteration=1000, attempts=100, verbose=False):
        circles_s = circle_count *  m.pi * circle_radius ** 2
        axis_size = sqrt(circles_s / circle_percent)
        return self.generate_with_circle_count(circle_radius, circle_count, axis_size, max_iteration, attempts, verbose), axis_size