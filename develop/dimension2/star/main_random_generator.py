import sys
sys.path.append('.')

from percolation.dimension2.star.generator.simple.random_generator import Generator
from percolation.dimension2.star.viualizer import Visualizer
from percolation.dimension2.star.analyzer import Analyzer
from pprint import pprint

star_count = 200
axis_size = 100
coef = 3
big_axis = 0.2
small_axis = 0.1

star_count = 100
r_inner = 7
r_outer = 20
    
g = Generator()
v = Visualizer()
a = Analyzer()

stars = g.generate_with_star_count(star_count, r_inner, r_outer)
biggest_cluster, info = a.get_biggest_cluster(stars, coef)

v.vizualize(stars, axis_size, r_inner, r_outer)
v.vizualize(biggest_cluster, axis_size, r_inner, r_outer)