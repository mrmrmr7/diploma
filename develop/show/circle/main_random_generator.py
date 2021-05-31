import sys
sys.path.append('.')

from percolation.dimension2.circle.generator.simple.mesh_based_generator import CircleGenerator
from percolation.dimension2.circle.visualizer import CircleVisualizer
from pprint import pprint

circle_radius = 0.5
circle_count = 10
axis_size = 10
iterations_count = 10000
attempts = 100
verbose = True

g = CircleGenerator()
v = CircleVisualizer()

circles = g.generate_with_circle_count(circle_radius, 
                                        circle_count, 
                                        axis_size, 
                                        max_iteration=iterations_count, 
                                        attempts=attempts, 
                                        verbose=verbose)

pprint(circles)
# v.vizualize(circle_radius, circles, axis_size)

