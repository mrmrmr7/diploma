from os import confstr
import sys
sys.path.append('.')
import plotly
from pprint import pprint

print(plotly.__version__)

from percolation.dimension2.circle.generator.simple.mesh_based_generator import CircleGenerator
from percolation.dimension2.circle.visualizer_2 import CircleVisualizer
from analysis.develop.dimension2.circle.percolation import (
    split_on_clusters, 
    get_clusters_ranges, 
    get_biggest_cluster )
import operator

circle_radius = 0.3
circle_count = 17
circle_percent = 0.3
axis_size = 10
verbose = True

g = CircleGenerator()
v = CircleVisualizer()

circles = g.generate_with_circle_percent(circle_radius, 
                                        circle_count,
                                        circle_percent, 
                                        # axis_size, 
                                        verbose=verbose)
axis_size = g.axis_size

clusters = split_on_clusters(circles, circle_radius)
clusters_ranges = get_clusters_ranges(circles, clusters, circle_radius)
biggest_cluster_number = get_biggest_cluster(clusters_ranges)
pprint(clusters)
pprint(clusters_ranges)
pprint(biggest_cluster_number)
pprint(f"max cluster: {biggest_cluster_number}")

cluster_50 = [biggest_cluster_number[0], *(clusters[biggest_cluster_number[0]])]
circles_for_cluster_50 = [ (c['x'], c['y']) for c in circles if c['index'] in cluster_50]
circles = [ (p['x'], p['y']) for p in circles ]
meshed_circles = [ (p['x'], p['y']) for p in g.meshed_circles ]
shuffle_circles = [ (p['x'], p['y']) for p in g.shuffled_circles ]

# v.vizualize(circle_radius, meshed_circles, axis_size, g.nearest_root)
v.vizualize(circle_radius, shuffle_circles, axis_size, g.nearest_root)
v.vizualize(circle_radius, circles_for_cluster_50, axis_size, g.nearest_root)

