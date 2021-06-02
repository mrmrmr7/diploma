from copy import deepcopy
from scipy.spatial.distance import euclidean as dist
from random import random
import math as m

class Ellipce:
    def __init__(self, x, y, phi, a, b): 
        self.x = x
        self.y = y
        self.phi = phi
        self.a = a
        self.b = b
        
    def _calculate_r(self, a, b, phi):
        phi_actual_rad = phi * m.pi / 180.0
        return (a * b)/m.sqrt(b**2 * m.cos(phi_actual_rad)**2 + a**2 * m.sin(phi_actual_rad)**2)

    def _calculate_phi(self, _ellipse1, _ellipse2):
        dx = _ellipse2.x-_ellipse1.x
        dy = _ellipse2.y-_ellipse1.y

        if dx == 0:
            return (90 + _ellipse1.phi, 90 + _ellipse2.phi)

        e1e2_tan = dy/dx
        tan_phi = m.atan(e1e2_tan) * 180.0 / m.pi
        e1_phi = 180.0 - tan_phi + _ellipse1.phi
        e2_phi = tan_phi - _ellipse2.phi

        e1_phi = e1_phi if e1_phi < 0 else e1_phi - 180
        e2_phi = e2_phi if e2_phi < 0 else e2_phi - 180
        return (e1_phi, e2_phi)

    def _ellipse_dist(self, _ellipse1, _ellipse2):
        self_xy = [_ellipse1.x, _ellipse1.y]
        other_xy = [_ellipse2.x, _ellipse2.y]
        return dist(self_xy, other_xy)

    def is_intersect(self, other):
        (e1_phi, e2_phi) = self._calculate_phi(self, other)
        r1 = self._calculate_r(self.a, self.b, e1_phi)
        r2 = self._calculate_r(other.a, other.b, e2_phi)
        dist = self._ellipse_dist(self, other)
        return (r1 + r2) > dist
    
    def try_to_move(self, dx, dy, dphi, min_x, max_x, min_y, max_y):
        res = deepcopy(self)
        new_x = res.x + (2 * random() - 1) * dx
        new_y = res.y + (2 * random() - 1) * dy
        new_phi = res.phi + (2 * random() - 1) * dphi

        if new_x >= max_x - self.a:
            new_x = max_x - self.a

        if new_x <= min_x + self.a:
            new_x = min_x + self.a

        if new_y >= max_y - self.b:
            new_y = max_y - self.b

        if new_y <= min_y + self.b:
            new_y = min_y + self.b
        
        res.x = new_x
        res.y = new_y
        res.phi = new_phi
        
        return res
    
    def get_area(self): 
        return m.pi * self.a * self.b