import sys
sys.path.append('.')

from percolation.dimension2.circle.generator.simple.tight_packing_based_generator import CircleGenerator
from percolation.dimension2.circle.visualizer import CircleVisualizer

circle_radius = 0.5
circle_count = 79
circle_fill_percent = 0.5
axis_size = 10
shuffles_count = 50
verbose = True

g = CircleGenerator()
v = CircleVisualizer()

circles = g.generate_with_circle_count(circle_radius, 
                                        circle_count, 
                                        axis_size,
                                        shuffles_count,
                                        verbose=verbose)

tighets_packed_spheres = [ (p['x'], p['y']) for p in g.tighest_circles ]
extended_circles = [ (p['x'], p['y']) for p in g.extended_circles ]
shuffled = [ (p['x'], p['y']) for p in g.shuffled_extended_circles ]
v.vizualize(circle_radius, tighets_packed_spheres, g.ranges['x'])
v.vizualize(circle_radius, extended_circles, g.ranges['x'])
v.vizualize(circle_radius, shuffled, g.ranges['x'])

