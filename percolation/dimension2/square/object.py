from copy import deepcopy
from scipy.spatial.distance import euclidean as dist
from random import random
import math as m
from scipy.spatial.distance import euclidean as distance
from operator import itemgetter as get 
import numpy as np

class Square:
    def __init__(self, x, y, a, phi, index):
        self.x = x
        self.y = y
        self.a = a
        self.phi = phi
        self.index = index
    
    
    def generate_accurate_square_points(self, _star, accuracy = 20):
        (x_arr, y_arr) = _star.generate_square_points(_star)

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
    
    
    def generate_square_points(self, _star):
        phi = _star.phi
        x = _star.x
        y = _star.y
        a = _star.a

        x_arr = []
        y_arr = []
        step = 90

        for i in range(6):
            rads = np.deg2rad(step * i + phi)
            x_arr.append(a*m.sqrt(2)*np.sin(rads) + x)
            y_arr.append(a*m.sqrt(2)*np.cos(rads) + y)

        return (x_arr, y_arr)
    
        
    def hard_check(self, _star1, _star2):
        p1arr = _star1.generate_accurate_square_points(_star1)
        p2arr = _star2.generate_accurate_square_points(_star2)

        dr = ((p1arr[0][1]-p1arr[0][0])**2+
            (p2arr[1][1]-p2arr[1][0])**2)**0.5
        
        for p1 in zip(p1arr[0],p1arr[1]):
            for p2 in zip(p2arr[0],p2arr[1]):
                if distance(p1,p2) < dr:
                    return True

        return False
        
    def is_intersect(self, other):
        xy_self = [self.x, self.y]
        xy_other = [other.x, other.y]
        center_dist = distance(xy_self, xy_other)

        if (center_dist < self.a):
            return True
        elif (center_dist < self.a + other.a):
            return self.hard_check(self, other)
        else:
            return False
    
    def try_to_move(self, dx, dy, min_x, max_x, min_y, max_y):
        res = deepcopy(self)
        new_x = res.x + (2 * random() - 1) * dx
        new_y = res.y + (2 * random() - 1) * dy

        if new_x >= max_x - self.r:
            new_x = max_x - self.r

        if new_x <= min_x + self.r:
            new_x = min_x + self.r

        if new_y >= max_y - self.r:
            new_y = max_y - self.r

        if new_y <= min_y + self.r:
            new_y = min_y + self.r
        
        res.x = new_x
        res.y = new_y
        
        return res
    
    def get_area(self):
        return m.pi * self.r * self.r