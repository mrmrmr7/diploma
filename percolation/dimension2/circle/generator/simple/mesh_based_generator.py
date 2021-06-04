import pandas as pd
from percolation.dimension2.circle.object import Circle
from random import shuffle
import math as m

class Generator:
    def _is_valid_position(self, items, new_item):
        for item in items:
            if new_item.is_intersect(item):
                return False
        return True

    def _shuffle(self, items, ax):
        r = items[0].r
        n = 30 

        for _ in range(n):
            for ip in range(len(items)):
                new_p = items[ip].try_to_move(r, r, 0, ax, 0, ax)
                if self._is_valid_position(items[:ip] + items[ip + 1:], new_p):
                    items[ip] = new_p

        return items
    
    def _generate(self, r, count, axis_size):
        root = m.sqrt(count)
        is_square_equals_count = int(root + 0.5) ** 2 == count
        nearest_root = int(root) if is_square_equals_count else int(root + 1)
        self.nearest_root = nearest_root

        drx = axis_size / (2 * nearest_root)
        dry = axis_size / (2 * nearest_root)

        items = []
        for iy in range(nearest_root):
            for ix in range(nearest_root):
                x = drx + ix * axis_size / nearest_root
                y = dry + iy * axis_size / nearest_root
                items.append(Circle(x, y, r))

        shuffle(items)
        return items[:count]

    def generate_elements_with_given_axis_size(self, r, count, axis_size):
        self.base_element = Circle(0, 0, r)
        items = self._generate(r, count, axis_size)
        indexed_items = []
        for item, index in zip(items, range(1, count + 1)):
            item.index = index
            indexed_items.append(item)
        self.meshed_items = items
        return self._shuffle(indexed_items, axis_size)

    def generate_elements_with_given_occupancy(self, r, count, percent):
        self.base_element = Circle(0, 0, r)
        item_s = count * self.base_element.get_area()
        ax = m.sqrt(item_s / percent)
        return self.generate_elements_with_given_axis_size(r, count, ax)
