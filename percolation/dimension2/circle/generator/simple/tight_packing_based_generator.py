import numpy as np
import random
import math as m
from scipy.spatial.distance import euclidean as dist
import copy
import plotly.express as px
import scipy as sp
from copy import deepcopy
from operator import itemgetter


class CircleGenerator: 
    def _get_area_range(self, R, n, circle_area_percent):
        s = np.pi * R ** 2
        a = (s * n / circle_area_percent) ** (1/2)
        return {'x': a, 'y': a}

    def _tighest_packed_circles(self):
        if self.verbose: print(f"Generating tighest packed circles start.")

        root = m.sqrt(self.circle_count)
        nearest_root = 0
        if int(root + 0.5) ** 2 != self.circle_count:
            nearest_root = int(root + 1)
        else:
            nearest_root = int(root)

        tighest_circles = []
        iy = 0
        dy = m.sqrt(3) * self.circle_radius
        installed_circle_count = 0
        while installed_circle_count < self.circle_count:
            x_max = nearest_root - iy % 2
            ix = 0
            while ix < x_max and installed_circle_count < self.circle_count:
                next_x = (iy % 2 + 1 + 2 * ix) * self.circle_radius
                if next_x > self.ranges['x'] - self.circle_radius:
                    break
                next_y = self.circle_radius + iy * dy
                installed_circle_count += 1
                tighest_circles.append({'index': installed_circle_count, 'x': next_x, 'y': next_y})
                ix += 1
            iy += 1

        self.tighest_circles = tighest_circles
        if self.verbose: print(f"Generating tighest packed circles done.\n")
        return tighest_circles


    def _extend_tighest_circles(self):
        if self.verbose: print(f"circles extending start.")

        tighest_circles = deepcopy(self.tighest_circles)

        axis_max = {
            'x': max([p['x'] for p in tighest_circles]) + self.circle_radius, 
            'y': max([p['y'] for p in tighest_circles]) + self.circle_radius
            }

        aspect = {
            'x': self.ranges['x'] / axis_max['x'],
            'y': self.ranges['y'] / axis_max['y'],
        }

        extended_circles = [ {
                'x': c['x'] * aspect['x'], 
                'y': c['y'] * aspect['y'],
                'index': c['index']
            } for c in tighest_circles ]

        self.extended_circles = extended_circles
        if self.verbose: print(f"circles extending end.\n")
        return extended_circles


    def shuffle_extended_circles(self):
        if self.verbose: print(f"circles shuffeling start.")
        ranges = self.ranges
        size = self.circle_radius
        extended_circles_count = len(self.extended_circles)

        shuffled_circles = deepcopy(self.extended_circles)

        shuffle_step_count = self.shuffles_count
        print_step = int(shuffle_step_count // 10)

        for shuffle_step in range(shuffle_step_count):
            if shuffle_step % print_step == 0:
                if self.verbose: print(f"Percents done: {int(shuffle_step // print_step) * 10}%.")
                if self.verbose: print(f"Shuffles done: {shuffle_step}")

            for i in range(extended_circles_count):
                current_circle = deepcopy(shuffled_circles[i])
                index = current_circle.pop('index', None)

                for k, v in current_circle.items():
                    di = (random.random() - 1 / 2) * size
                    new_k = v + di
                    if new_k - size < 0:
                        current_circle[k] = size
                    elif new_k + size > ranges[k]:
                        current_circle[k] = ranges[k] - size
                    else:
                        current_circle[k] = new_k

                current_circle['index'] = index
                is_intersect = False
                for j in [*range(i), *range(i + 1, extended_circles_count)]:
                    is_intersect = dist(itemgetter('x', 'y')(current_circle), 
                                        itemgetter('x', 'y')(shuffled_circles[j])) <= 2 * size
                    if is_intersect:
                        break

                if not is_intersect:
                    shuffled_circles[i] = current_circle

        self.shuffled_extended_circles = shuffled_circles
        if self.verbose: print(f"circles shuffeling end.\n")
        return shuffled_circles


    def generate_with_circle_count(self, 
                                    circle_radius, 
                                    circle_count, 
                                    axis_size,
                                    shuffles_count,
                                    verbose):
                                    # circle_fill_percent):
        self.circle_count = circle_count
        self.circle_radius = circle_radius
        self.verbose = verbose
        self.shuffles_count = shuffles_count
        # self.circle_fill_percent = circle_fill_percent
        self.ranges = {'x': axis_size, 'y': axis_size}
        # self.ranges = self._get_area_range(circle_radius, circle_count, circle_fill_percent)
        self._tighest_packed_circles()
        self._extend_tighest_circles()
        return self.shuffle_extended_circles()

