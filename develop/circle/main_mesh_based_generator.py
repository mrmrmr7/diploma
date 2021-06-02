import sys
sys.path.append('.')
from percolation.dimension2.circle.generator.simple.mesh_based_generator import Generator
from percolation.dimension2.circle.visualizer import Visualizer

r = 0.5
count = 5
axis_size = 10

g = Generator()
v = Visualizer()

circles = g.generate_elements_with_given_axis_size(r, count, axis_size)
v.vizualize(circles, axis_size)

