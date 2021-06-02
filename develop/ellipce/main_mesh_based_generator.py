import sys
sys.path.append('.')

from percolation.dimension2.ellipce.generator.simple.mesh_based_generator import Generator
from percolation.dimension2.ellipce.visualizer import Visualizer

count = 36
axis_size = 10
big_axis = 1.0
small_axis = 0.5

g = Generator()
v = Visualizer()

items = g.generate_elements_with_given_axis_size(big_axis, small_axis, count, axis_size)
v.vizualize(g.meshed_items, axis_size)
v.vizualize(items, axis_size)

