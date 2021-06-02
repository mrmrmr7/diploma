import sys
sys.path.append('.')

from percolation.dimension2.ellipce.generator.simple.random_generator import Generator
from percolation.dimension2.ellipce.visualizer import Visualizer
from percolation.dimension2.ellipce.analyzer import Analyzer
from pprint import pprint

ellipce_count = 16
axis_size = 10
coef = 3
big_axis = 1.5
small_axis = 1.0

g = Generator()
v = Visualizer()
a = Analyzer()

ellipces = g.generate_with_ellipce_count(ellipce_count, axis_size, big_axis, small_axis)
biggest_cluster, info = a.get_biggest_cluster(ellipces, coef)

v.vizualize(ellipces, axis_size)
v.vizualize(biggest_cluster, axis_size)

