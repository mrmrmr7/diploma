import sys

sys.path.append('.')

from percolation.dimension2.circle.generator.simple.tight_packing_based_generator import CircleGenerator
from percolation.dimension2.circle.visualizer import CircleVisualizer
from pprint import pprint
import plotly.graph_objects as go
import scipy.stats
from scipy.stats import chi2
import math
import json
import numpy as np
from datetime import datetime

def get_single_axis_distribution(data=None, 
                                axis_range=None, 
                                pocket_count=10):
    h = axis_range / pocket_count
    distr = np.zeros(pocket_count + 1)
    
    for v in data: distr[int(v/h)] += 1
    
    distr = [ ((i + 0.5) * h, int(distr[i])) for i in range(len(distr) - 1)]
    
    return distr


def get_chi(data):
    
    ni_len = len(data)
    x_arr = []
    n_arr = []
    for (xi, ni) in data:
        x_arr.append(xi)
        n_arr.append(ni)
    
    n = sum(n_arr)
    
    m = 0
    for i in range(ni_len):
        m += (x_arr[i] * n_arr[i])
    m /= n
    
    d = 0
    for i in range(ni_len):
        d += ((x_arr[i] - m) ** 2 * n_arr[i])
    d /= n
    
    db = math.sqrt(d)
    
    a = m - math.sqrt(3) * db
    b = m + math.sqrt(3) * db
    
    f = 1 / (b - a)
    
    ni_arr = [ n * f * (x_arr[0] - a) ]
    for i in range(1, ni_len - 1):
        ni_arr.append(n * f * (x_arr[i+1] - x_arr[i]))
    ni_arr.append(n * f * (b - x_arr[-1]))
    
    chi = 0
    for i in range(ni_len):
        if ni_arr[i] != 0:
            chi += ((n_arr[i] - ni_arr[i]) ** 2) / ni_arr[i] 
    
    return chi


def is_uniform_distribution(data, ax, s):
    k = s - 3
    distr_x = get_single_axis_distribution(data, ax, s)
    chi = get_chi(distr_x)
    chi_crit = chi2.ppf(0.999, k)
    return 3 * chi_crit > chi, chi, chi_crit


g = CircleGenerator()
vis = CircleVisualizer()

circles_count_from = 80
circles_count_to = 81
axis_size = 10
attempts = 30
circle_radius = 0.5
shuffles_count = 50
s = 10

info = {}

with open(f"./output/dimension2_circle_uniform_dist_from_{circles_count_from}_to_{circles_count_to}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.txt", 'w') as output:
    params = {
        'circle_count_from': circles_count_from,
        'circle_count_to': circles_count_to,
        'axis_size': axis_size, 
        'attempts': attempts,
        'circle_radius': circle_radius,
        'shuffles_count': shuffles_count
    }
    output.write(json.dumps(params))
    for circles_count in range(circles_count_from, circles_count_to):
        uniform_count = 0
        print(circles_count)
        for i in range(attempts):
            circles = g.generate_with_circle_count(
                    circle_radius=circle_radius,
                    circle_count=circles_count,
                    axis_size=axis_size,
                    shuffles_count=shuffles_count,
                    verbose=False
                )
            
            is_uniform_x, chi_x, _ = is_uniform_distribution([p['x'] for p in circles], axis_size, s) 
            # print(f"Is x uniform: {is_uniform_x}")
            is_uniform_y, chi_y, chi_crit = is_uniform_distribution([p['y'] for p in circles], axis_size, s) 
            # print(f"Is y uniform: {is_uniform_y}")
            if is_uniform_x and is_uniform_y:
                uniform_count += 1
            # else:
            #     vis.vizualize(circle_radius, 
            #         [ (p['x'], p['y']) for p in circles ], 
            #         axis_size,
            #         f'count: {circles_count} '
            #         f'att: {i} '
            #         f'x_unif: {is_uniform_x} '
            #         f'y_unif: {is_uniform_y} '
            #         f'chi_x: {round(chi_x, 3)} '
            #         f'chi_y: {round(chi_y, 3)} '
            #         f'chi_crit: {round(chi_crit, 3)} ')
        
        output.write(f"{circles_count}: {uniform_count}\n")
        output.flush()
        info[circles_count] = uniform_count

print(info)

