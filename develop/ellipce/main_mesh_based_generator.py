import sys
sys.path.append('.')

from percolation.dimension2.ellipce.generator.simple.mesh_based_generator import Generator
from percolation.dimension2.ellipce.visualizer import Visualizer
from percolation.dimension2.ellipce.analyzer import Analyzer

count = 20
percent = 0.8
big_axis = 1.0
small_axis = 0.5

coef = 1.1

g = Generator()
v = Visualizer()
a = Analyzer()

items = g.generate_elements_with_given_occupancy(big_axis, small_axis, count, percent)
biggest_cluster, info = a.get_biggest_cluster(items, coef)

axis_size = g.axis_size
print(axis_size)
v.vizualize(g.meshed_items, axis_size)
v.vizualize(items, axis_size)
v.vizualize(biggest_cluster, axis_size)
