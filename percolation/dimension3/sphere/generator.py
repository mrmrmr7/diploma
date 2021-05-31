import numpy as np
import math as m
import random
from scipy.spatial import distance
import copy
import plotly.express as px
import scipy as sp


class GeneratorOf3DSpheres: 
    def __init__(self, sphere_count, sphere_size, sphere_fill_percent):
        self.sphere_count = sphere_count
        self.sphere_size = sphere_size
        self.sphere_fill_percent = sphere_fill_percent
        self.ranges = self._get_space_range(sphere_size, sphere_count, sphere_fill_percent)


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


    def shuffle_extended_spheres(self):
        print(f"Spheres shuffeling start.")
        ranges = self.ranges
        size = self.sphere_size
        extended_spheres_count = len(self.extended_spheres)

        shuffled_spheres = copy.deepcopy(self.extended_spheres)

        shuffle_step_count = 100
        print_step = int(shuffle_step_count // 10)

        for shuffle_step in range(shuffle_step_count):
            if shuffle_step % print_step == 0:
                print(f"Percents done: {int(shuffle_step // print_step) * 10}%.")
                print(f"Shuffles done: {shuffle_step}")

            for i in range(extended_spheres_count):
                current_sphere = copy.deepcopy(shuffled_spheres[i])

                for k, v in current_sphere.items():
                    di = random.random() * size - size / 2
                    new_k = v + di
                    if new_k - size < 0:
                        current_sphere[k] = ranges[k] - size
                    elif new_k + size > ranges[k]:
                        current_sphere[k] = size
                    else:
                        current_sphere[k] = new_k

                is_intersect = False
                for j in [*range(i), *range(i + 1, extended_spheres_count)]:
                    figures_dist = distance.euclidean(list(current_sphere.values()), list(shuffled_spheres[j].values()))
                    is_intersect = figures_dist <= 2 * size

                    if is_intersect:
                        break

                if not is_intersect:
                    shuffled_spheres[i] = current_sphere

        self.shuffled_extended_spheres = shuffled_spheres
        print(f"Spheres shuffeling end.\n")
        return shuffled_spheres


    def get_uniform_distributed_spheres(self):
        self._tighest_packed_spheres()
        self._extend_tighest_spheres()
        return self.shuffle_extended_spheres()

