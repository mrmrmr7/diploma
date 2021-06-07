from pprint import pprint
import sys
sys.path.append('.')

from percolation.dimension2.circle.generator.simple.tight_packing_based_generator import CircleGenerator
from percolation.dimension2.circle.visualizer import Visualizer

circle_radius = 0.8
circle_count = 23
circle_fill_percent = 1
axis_size = 10
shuffles_count = 50
verbose = True

g = CircleGenerator()
v = Visualizer()

circles = g.generate_with_circle_count(circle_radius, 
                                        circle_count, 
                                        axis_size,
                                        shuffles_count,
                                        verbose=verbose)

pprint(g.tighest_circles)
pprint(g.extended_circles)
pprint(g.shuffled_extended_circles)

v.vizualize(g.tighest_circles, axis_size)
v.vizualize(g.extended_circles, axis_size)
v.vizualize(g.shuffled_extended_circles, axis_size)

