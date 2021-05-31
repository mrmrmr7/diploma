import sys
sys.path.append('.')
from percolation.dimension2.circle.generator.simple.mesh_based_generator import CircleGenerator
from percolation.dimension2.circle.visualizer import CircleVisualizer

circle_radius = 0.2
circle_count = 50
axis_size = 10
verbose = True

g = CircleGenerator()
v = CircleVisualizer()

circles = g.generate_with_circle_count(circle_radius, 
                                        circle_count, 
                                        axis_size, 
                                        verbose=verbose)

circles = [ (p['x'], p['y']) for p in circles ]
meshed_circles = [ (p['x'], p['y']) for p in g.meshed_circles ]

v.vizualize(circle_radius, meshed_circles, axis_size, g.nearest_root)

