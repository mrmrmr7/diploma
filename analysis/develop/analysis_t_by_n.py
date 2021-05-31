import sys
sys.path.append('percolation')

from percolation.dimension2.circle.generator.simple_generator import CircleGenerator
from percolation.dimension2.circle.visualizer import CircleVisualizer
import plotly.graph_objects as go
import time 
from numpy import arange
from datetime import datetime

circle_radius = 0.5
circle_count = 10
max_circle_percent = 0.6
axis_size = 10
iterations_count = 10000
attempts = 100
verbose = False
calculation_repeats = 100

g = CircleGenerator()

res_time = {}

with open(f"output/res_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}", 'w') as f:  
    for circle_percent in arange(0.59, max_circle_percent, 0.01):
        print(f"Circle percent: {circle_percent}")
        t = 0

        for repeat in range(calculation_repeats):
            t_start = time.time()
            circles, _ = g.generate_with_circle_percent(circle_radius, 
                                                circle_count, 
                                                circle_percent,
                                                max_iteration=iterations_count, 
                                                attempts=attempts, 
                                                verbose=verbose)
            t += time.time() - t_start

        res_time[circle_percent] = t / calculation_repeats

        f.write(f"{format(circle_percent, '.3f')}:{res_time[circle_percent]}\n")   
        f.flush() 
    

fig = go.Figure(data=go.Scatter(
        x=list(res_time.keys()), 
        y=list(res_time.values())))

fig.update_layout(title="Generation time t depending on circle count n")
fig.show()


# v.vizualize(circle_radius, circles, axis_size)
