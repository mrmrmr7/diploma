import numpy as np
import math as m
import random
from scipy.spatial import distance
import copy
import plotly.express as px
import scipy as sp

from statistic import Statistic


class GeneratorOf3DSpheres: 
    def __init__(self, sphere_count, sphere_size, sphere_fill_percent, pocket_count):
        self.sphere_count = sphere_count
        self.sphere_size = sphere_size
        self.sphere_fill_percent = sphere_fill_percent
        self.ranges = self._get_space_range(sphere_size, sphere_count, sphere_fill_percent)
        self.pocket_count = pocket_count


    def _get_space_range(self, R, n, sphere_volume_percent):
        v = 4*np.pi*(R**3)/3
        a = (v * n / sphere_volume_percent) ** (1/3)
        return {'x': a, 'y': a, 'z': a}


    def _tighest_packed_spheres(self):
        print(f"Generating tighest packed spheres start.")

        single_sphere_volume = 4*np.pi*(self.sphere_size**3)/3
        total_spheres_volume = single_sphere_volume * self.sphere_count

        h = m.sqrt(2)*self.sphere_size
        sphere_volume_percent_max = 0.72
        tight_packing_volume = total_spheres_volume / sphere_volume_percent_max * 1.2
        a = tight_packing_volume**(1/3)*h
        k = {'x': a, 'y': a, 'z': a}

        tighest_spheres = []

        current_n = 0
        iz = 1
        next_z = 0
        while not (next_z + 2 * h >= k['z'] or current_n >= self.sphere_count):
            next_z = iz * h
            iy = 0
            next_y = 0
            while not (next_y + 2 * h >= k['y'] or current_n >= self.sphere_count):
                next_y = (iy + 1) * h
                ix = 0
                next_x = 0
                while not (next_x + 3 * h >= k['x'] or current_n >= self.sphere_count):
                    if iz % 2 == 1:
                        next_x = h * (2 * ix + (iy % 2 + 1))
                    else:
                        next_x = h * (2 * (ix + ((iy + 1) % 2)) + (iy % 2))

                    tighest_spheres.append({'x': next_x,'y': next_y,'z': next_z})
                    current_n += 1
                    ix += 1
                iy += 1
            iz += 1

        self.tighest_spheres = tighest_spheres
        print(f"Generating tighest packed spheres done.\n")
        return tighest_spheres


    def _extend_tighest_spheres(self):
        print(f"Spheres extending start.")

        tighest_spheres = self.tighest_spheres
        ranges = self.ranges
        size = self.sphere_size

        sphere_position_max = {'x': -1, 'y': -1, 'z': -1}

        for sphere in tighest_spheres:
            for k, v in sphere.items():
                if v > sphere_position_max[k]:
                    sphere_position_max[k] = v

        aspect_ratio = {}
        for i in sphere_position_max.keys(): 
            aspect_ratio[i] = (ranges[i] - size) / sphere_position_max[i]

        extended_spheres = []
        for sphere in tighest_spheres:
            for k, v in sphere.items():
                sphere[k] = v * aspect_ratio[k] - aspect_ratio[k] / 2

            extended_spheres.append(sphere)

        self.extended_spheres = extended_spheres
        print(f"Spheres extending end.\n")
        return extended_spheres


    def _single_shuffle(self, sphere, k):
        di = random.random() * self.sphere_size - self.sphere_size / 2
        new_k = sphere[k] + di
        if new_k - self.sphere_size < 0:
            sphere[k] = self.ranges[k] - self.sphere_size
        elif new_k + self.sphere_size > self.ranges[k]:
            sphere[k] = self.sphere_size
        else:
            sphere[k] = new_k
        
        return sphere

    
    def _is_sphere_intersect_with_others(self, sphere, others, i):
        is_intersect = False

        for j in [*range(i), *range(i + 1, len(others))]:
            dist = distance.euclidean(list(sphere.values()), list(others[j].values()))
            is_intersect = dist <= 2 * self.sphere_size

            if is_intersect:
                break

        return is_intersect


    def _get_not_uniformed_axis(self, spheres, current_axis):
        print(f"\nCheck uniform distributions for axises: {current_axis} start.") 
        axis_to_check = copy.deepcopy(current_axis)
        stat = Statistic()

        uniform_approves = []

        for axis in axis_to_check:
            axis_arr = []

            for figure in spheres:
                axis_arr.append(figure[axis])

            dist = stat.get_single_axis_distribution(axis_arr, self.ranges[axis], pocket_count=self.pocket_count)
            is_axis_uniform = abs(np.polyfit(np.arange(self.pocket_count), dist, 1)[0]) < 0.2
            print(f"Is axis {axis} uniformed: {is_axis_uniform}")
            uniform_approves.append(is_axis_uniform)

            if is_axis_uniform:
                current_axis.remove(axis)
        
        is_fully_uniform = all(uniform_approves)
        print(f"Check uniform distributions for axises: {axis_to_check} done") 
        return is_fully_uniform, current_axis


    def _shuffle_extended_spheres(self):
        print(f"Spheres shuffeling start.")

        shuffled_spheres = self.extended_spheres
        shuffe_axis = list(shuffled_spheres[0].keys())

        shuffle_step = 1
        is_uniform = False

        while not is_uniform and shuffle_step < 1000:
            for i in range(len(self.extended_spheres)):
                k = random.choice(shuffe_axis)
                current_sphere = self._single_shuffle(copy.deepcopy(shuffled_spheres[i]), k)

                if not self._is_sphere_intersect_with_others(current_sphere, shuffled_spheres, i):
                    shuffled_spheres[i] = current_sphere

            shuffle_step += 1
            if shuffle_step % 50 == 0:
                print(f"Shuffles done: {shuffle_step}")
                is_uniform, shuffe_axis = self._get_not_uniformed_axis(shuffled_spheres, shuffe_axis)

        self.shuffled_extended_spheres = shuffled_spheres
        print(f"Spheres shuffeling end.\n")
        return shuffled_spheres


    def get_uniform_distributed_spheres(self):
        self._tighest_packed_spheres()
        self._extend_tighest_spheres()
        self._shuffle_extended_spheres()

        return self.shuffled_extended_spheres

