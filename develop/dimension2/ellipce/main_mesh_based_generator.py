import sys

from numpy.lib.shape_base import tile
sys.path.append('.')

from percolation.dimension2.ellipce.generator.simple.mesh_based_generator import Generator
from percolation.dimension2.ellipce.visualizer import Visualizer
from percolation.dimension2.ellipce.analyzer import Analyzer

import time

count = 100
percent = 0.4
big_axis = 0.2
small_axis = 0.1

coef = small_axis / 2

g = Generator()
v = Visualizer()
a = Analyzer()

i_time = []
for i in range(1):
    print(i)
    t_start = time.time()
    items = g.generate_elements_with_given_occupancy(big_axis, small_axis, count, percent)
    dt = time.time() - t_start
    print(f"dt: {dt}")
    i_time.append(dt)
    
biggest_cluster, info = a.get_biggest_cluster(items, coef)
print(info)
print(i_time)
print("awg_time:")
print(sum(i_time) / len(i_time))
axis_size = g.axis_size
v.vizualize(g.meshed_items, axis_size)
v.vizualize(items, axis_size)
v.vizualize(biggest_cluster, axis_size)
