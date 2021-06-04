from math import inf
import sys
sys.path.append('.')

from percolation.dimension2.ellipce.generator.simple.mesh_based_generator import Generator
from percolation.dimension2.ellipce.analyzer import Analyzer
from pprint import pprint
from datetime import datetime
import numpy as np
import time

ellipce_count = 500
coef = 1.1
big_axis = 1.0
small_axis = 0.5
ellipce_percent = 0.60

conductivity_percent_per_ellipce_count = {}

g = Generator()
a = Analyzer()

conductive = 0

all_gen_count = 10
avg_time_count = 0
iteration_time_arr = []
for i in range(all_gen_count):
    t_start = time.time()
    print(i)
    res = g.generate_elements_with_given_occupancy(big_axis, small_axis, ellipce_count, ellipce_percent)
    axis = g.axis_size
    iteration_time = (time.time() - t_start)
    iteration_time_arr.append(iteration_time)
    avg_time_count += iteration_time
    print(f"iteration time: {iteration_time}")
    print(iteration_time)
        
print(f"avg_gen_time per {all_gen_count} generations")
print(f"iteration_times {iteration_time_arr}")
print(avg_time_count/all_gen_count)


