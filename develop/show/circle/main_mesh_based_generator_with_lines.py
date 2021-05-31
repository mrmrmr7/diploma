from os import confstr
import sys
sys.path.append('.')
import plotly

print(plotly.__version__)

from percolation.dimension2.circle.generator.simple.mesh_based_generator import CircleGenerator
from percolation.dimension2.circle.visualizer_2 import CircleVisualizer
from analysis.develop.dimension2.circle.percolation import split_on_clusters

circle_radius = 0.4
circle_count = 50
axis_size = 10
verbose = True

g = CircleGenerator()
v = CircleVisualizer()

circles = g.generate_with_circle_count(circle_radius, 
                                        circle_count, 
                                        axis_size, 
                                        verbose=verbose)

clusters = split_on_clusters(circles, circle_radius)
print(clusters)

circles = [ (p['x'], p['y']) for p in circles ]
meshed_circles = [ (p['x'], p['y']) for p in g.meshed_circles ]

# v.vizualize(circle_radius, circles, axis_size)
v.vizualize(circle_radius, meshed_circles, axis_size, g.nearest_root)

