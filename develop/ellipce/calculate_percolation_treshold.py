from math import inf
import sys
sys.path.append('.')

from percolation.dimension2.ellipce.generator.simple.mesh_based_generator import Generator
from percolation.dimension2.ellipce.visualizer import Visualizer
from percolation.dimension2.ellipce.analyzer import Analyzer
from pprint import pprint
from datetime import datetime
import numpy as np
import os

ellipce_count = 1000

big_axis = 1.0
coef = big_axis / 2
all_gen_count = 100
min_ellipce_percent = 0.1
max_ellipce_percent = 0.8
step = 0.005

g = Generator()
a = Analyzer()

output_dir = "output/2d/ellipce"
os.makedirs(output_dir, exist_ok=True)

for small_axis in np.arange(0.25, 1.0, 0.05):
    with open(f"{output_dir}/{datetime.now().strftime('%Y-%m-%d_%H%M%S')}_c{coef}_a{big_axis}_b{small_axis}_ec{ellipce_count}", 'w') as f:  
        for ellipce_percent in np.arange(min_ellipce_percent, max_ellipce_percent + step, step):
            conductive = 0
            for i in range(all_gen_count):
                print(f"ellipces: {format(ellipce_percent, '.3f')} repeat: {format(i, '3')} conductive: {conductive}")
                res = g.generate_elements_with_given_occupancy(big_axis, small_axis, ellipce_count, ellipce_percent)
                biggest_cluster, info = a.get_biggest_cluster(res, coef)
                axis = g.axis_size
                
                if i == 15 and conductive == 0:
                    break
                
                if (info['size'] >= axis - big_axis):
                    conductive += 1

            conductivity_percent_per_ellipce_count = conductive / all_gen_count
            f.write(f"{ellipce_percent}:{format(conductive / all_gen_count, '.3f')}\n")   
            f.flush() 
            if conductivity_percent_per_ellipce_count > 0.98:
                break

