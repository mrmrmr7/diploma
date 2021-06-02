from math import inf
import sys
sys.path.append('.')

from percolation.dimension2.ellipce.generator.simple.mesh_based_generator import Generator
from percolation.dimension2.ellipce.visualizer import Visualizer
from percolation.dimension2.ellipce.analyzer import Analyzer
from pprint import pprint

ellipce_count = 16
ellipce_percent = 0.3
coef = 2.1
big_axis = 1.5
small_axis = 1.0

g = Generator()
v = Visualizer()
a = Analyzer()

# ellipces = g.generate_with_ellipce_count(ellipce_count, axis_size, big_axis, small_axis)
axis_size, shuffled, selected, ellipces_init = g.generate_with_ellipce_percent(ellipce_count, ellipce_percent, big_axis, small_axis)

# v.vizualize(ellipces_init, axis_size)
# v.vizualize(selected, axis_size)
v.vizualize(shuffled, axis_size)

biggest_cluster, info = a.get_biggest_cluster(shuffled, coef)
print([ e['index'] for e in biggest_cluster ])
print(info)
print(axis_size)
print((coef * big_axis))
print(info['size'] > axis_size - big_axis)
# v.vizualize(biggest_cluster, axis_size)

