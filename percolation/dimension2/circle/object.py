from copy import deepcopy
from scipy.spatial.distance import euclidean as dist
from random import random
import math as m

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.index = None
        
    def is_intersect(self, other):
        self_xy = [self.x, self.y]
        other_xy = [other.x, other.y]
        return dist(self_xy, other_xy) <= self.r + other.r
    
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