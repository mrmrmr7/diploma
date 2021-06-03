from percolation.dimension2.ellipce.object import Ellipce
from random import shuffle
import math as m
from operator import itemgetter as get


class Generator:
    def _is_valid_position(self, items, new_item):
        for item in items:
            if new_item.is_intersect(item):
                return False
        return True

    def _shuffle(self, items, ax):
        r = items[0].a
        n = 30

        for _ in range(n):
            for ip in range(len(items)):
                new_p = items[ip].try_to_move(r, r, 0, 0, ax, 0, ax)
                if self._is_valid_position(items[:ip] + items[ip + 1:], new_p):
                    items[ip] = new_p

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
