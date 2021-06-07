from math import inf
import sys
sys.path.append('.')

from percolation.dimension2.ellipce.generator.simple.mesh_based_generator import Generator
from percolation.dimension2.ellipce.visualizer import Visualizer
from percolation.dimension2.ellipce.analyzer import Analyzer
from pprint import pprint
from datetime import datetime
import numpy as np
import os
import json

ellipce_count = 1000

big_axis = 1.0
coef = big_axis / 2
all_gen_count = 100
min_ellipce_percent = 0.1
max_ellipce_percent = 0.8
ellipce_percent = 0.5
step = 0.005

g = Generator()
a = Analyzer()

output_dir = "output/2d/ellipce"
os.makedirs(output_dir, exist_ok=True)

for i in range(100):
    print(f"repeat: {i}")
    small_axis_size_range = []
    ranges = ""
    repeats = 0
    sizes_dict = {}
    with open(f"output/2d/ellipce/biggest_cluster/clusters_{ellipce_percent}.txt", "r") as f:
        lines = f.readlines()
        repeats = int(lines[0])
        ranges = lines[1]
        small_axis_size_range = list(map(float, lines[1].split(":")))
        sizes_dict = json.loads(lines[2])

    with open(f"output/2d/ellipce/biggest_cluster/clusters.txt", 'w') as f:  
        for small_axis in small_axis_size_range:
            res = g.generate_elements_with_given_occupancy(big_axis, small_axis, ellipce_count, ellipce_percent)
            biggest_cluster, info = a.get_biggest_cluster(res, coef)
            sizes_dict[str(small_axis)] += len(biggest_cluster)

        repeats += 1
        f.write(f"{repeats}\n")
        f.write(f"{ranges}")
        f.write(json.dumps(sizes_dict))   

