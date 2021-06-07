from os import confstr
import sys
sys.path.append('.')
import plotly

print(plotly.__version__)

from percolation.dimension2.circle.generator.simple.mesh_based_generator import Generator
from percolation.dimension2.circle.visualizer import Visualizer

r = 0.4
count = 50
axis_size = 10

g = Generator()
v = Visualizer()

circles = g.generate_elements_with_given_axis_size(r, count, axis_size)

v.vizualize(g.meshed_items, axis_size, nearest_root = g.nearest_root)
v.vizualize(circles, axis_size)

