import sys
sys.path.append('.')

from percolation.dimension2.square.generator.simple.random_generator import Generator
from percolation.dimension2.square.viualizer import Visualizer
from percolation.dimension2.square.analyzer import Analyzer
from pprint import pprint


square_count = 10
square_side = 9
axis_size = 100
coef = 3
    
g = Generator()
v = Visualizer()
a = Analyzer()

squares = g.generate_elements_with_given_axis_size(square_side, square_count, axis_size)
biggest_cluster, info = a.get_biggest_cluster(squares, coef)

v.vizualize(squares, axis_size)
v.vizualize(biggest_cluster, axis_size)