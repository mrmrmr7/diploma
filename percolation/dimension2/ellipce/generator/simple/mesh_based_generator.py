from hashlib import new
import random
from random import shuffle
from scipy.spatial.distance import euclidean as dist
import math as m
from operator import itemgetter as get
from percolation.dimension2.ellipce.object import Ellipce


class Generator:
    def _is_valid_position(self, items, new_item, v_index):
        a = items[0].a
        items_len = len(items)
        x_sorted_arr = sorted(items, key=lambda v: v.x)
        # y_sorted_arr = sorted(items, key=lambda v: v.x)

        i = 0
        new_item_index = new_item.index
        for index in range(items_len):
            if x_sorted_arr[index].index == new_item_index:
                i = index
                break
            
        for item_index in range(i - 1, -1, -1):
            item = x_sorted_arr[item_index]
            if abs(item.x - new_item.x) > 2 * a:
                break
            
            if new_item.is_intersect(item):
                return False
                
        for item_index in range(i + 1, items_len, 1):
            item = x_sorted_arr[item_index]
            if abs(item.x - new_item.x) > 2 * a:
                return False
            
            if new_item.is_intersect(item):
                return False
        return True

    def _shuffle(self, items, ax):
        items_count = len(items)
        ra = items[0].a
        rb = items[0].b
        n_max = 20

        motions_dist = 0
        for _ in range(n_max):
            for ip in range(items_count):
                item = items[ip]
                if not item.is_moved_enought():
                    way_to_update = random.randint(1, 3)
                    if way_to_update == 1:
                        new_p = item.try_to_move(ra, 0, 0, 0, ax, 0, ax)
                    if way_to_update == 2:
                        new_p = item.try_to_move(0, rb, 0, 0, ax, 0, ax)
                    if way_to_update == 3:
                        new_p = item.try_to_move(ra, rb, 0, 0, ax, 0, ax)
                        
                    if self._is_valid_position(items, new_p, ip):
                        d = dist([new_p.x, new_p.y], [item.x, item.y])
                        new_p.add_walked_dist(d)
                        motions_dist += d
                        items[ip] = new_p
                    
            if motions_dist > items_count * ra:
                break

        return items

    def _generate(self, a, b, count, axis_size):
        x_ellipce_count = int(axis_size // (2 * a))
        y_ellipce_count = int(axis_size // (2 * b))
        
        ax = axis_size / (2 * a * x_ellipce_count)
        ay = axis_size / (2 * b * y_ellipce_count)
        
        items = []
        for ix in range(x_ellipce_count):
            for iy in range(y_ellipce_count):
                x = (ix * 2 + 1) * a * ax
                y = (iy * 2 + 1) * b * ay
                items.append(Ellipce(x, y, 0, a, b))

        shuffle(items)
        return items[:count]

    def generate_elements_with_given_axis_size(self, a, b, count, axis_size):
        self.base_element = Ellipce(0, 0, 0, a, b)
        items = self._generate(a, b, count, axis_size)
        indexed_items = []
        for item, index in zip(items, range(1, count + 1)):
            item.index = index
            indexed_items.append(item)
        self.meshed_items = items
        return self._shuffle(indexed_items, axis_size) 

    def generate_elements_with_given_occupancy(self, a, b, count, percent):
        self.base_element = Ellipce(0, 0, 0, a, b)
        item_s = count * self.base_element.get_area()
        ax = m.sqrt(item_s / percent)
        self.axis_size = ax
        return self.generate_elements_with_given_axis_size(a, b, count, ax)
