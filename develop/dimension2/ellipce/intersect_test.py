
import sys
sys.path.append('.')

import numpy as np
from datetime import datetime
from pprint import pprint
from percolation.dimension2.ellipce.analyzer import Analyzer
from percolation.dimension2.ellipce.visualizer import Visualizer
from percolation.dimension2.ellipce.generator.simple.mesh_based_generator import Generator
from math import inf


ellipce_count = 20
coef = 2.1
big_axis = 0.4
small_axis = 0.3
all_gen_count = 100
min_ellipce_percent = 0.4
max_ellipce_percent = 0.402

conductivity_percent_per_ellipce_count = {}

g = Generator()
a = Analyzer()
v = Visualizer()

ellipces = [{
    "phi_0": 30,
    "a": big_axis,
    "b": small_axis,
    "x": 2,
    "y": 2,
    "index": 1
}, {
    "phi_0": 80,
    "a": big_axis,
    "b": small_axis,
    "x": 2.52,
    "y": 2.54,
    "index": 2
}]

is_intersect = a.is_ellipses_intersect(*ellipces, 1)
print(is_intersect)
v.vizualize(ellipces, 10)
