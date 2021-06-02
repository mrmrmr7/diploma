from math import inf
import sys
sys.path.append('.')

from percolation.dimension2.ellipce.generator.simple.mesh_based_generator import Generator
from percolation.dimension2.ellipce.visualizer import Visualizer
from percolation.dimension2.ellipce.analyzer import Analyzer
from pprint import pprint
from datetime import datetime
import numpy as np

ellipce_count = 20
coef = 2.1
big_axis = 0.4
small_axis = 0.4
all_gen_count = 100
min_ellipce_percent = 0.4
max_ellipce_percent = 0.402

conductivity_percent_per_ellipce_count = {}

g = Generator()
a = Analyzer()


with open(f"output/2d/ellipce/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}_c{coef}_a{big_axis}_b{small_axis}", 'w') as f:  
    for ellipce_percent in np.arange(min_ellipce_percent, max_ellipce_percent, 0.002):
        conductive = 0
        for i in range(all_gen_count):
            print(f"ellipces: {ellipce_percent} repeat: {i} conductive: {conductive}")
            axis, shuffled, selected, ellipces_init  = g.generate_with_ellipce_percent(ellipce_count, ellipce_percent, big_axis, small_axis)
            biggest_cluster, info = a.get_biggest_cluster(shuffled, coef)
            print(info)
            if (info['size'] >= axis - 0.1 * big_axis):
                conductive += 1

        conductivity_percent_per_ellipce_count[ellipce_count] = conductive / all_gen_count
        f.write(f"{ellipce_percent}:{format(conductive / all_gen_count, '.3f')}\n")   
        f.flush() 

