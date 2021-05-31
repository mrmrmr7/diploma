from percolation.dimensions2.circle.generators.fastest_generator import CircleGenerator
from percolation.dimensions2.circle.visualizer import CircleVisualizer
import plotly.graph_objects as go
import time 
from numpy import arange
from datetime import datetime

circle_radius = 1
circle_count = 70
max_circle_percent = 0.6
axis_size = 10
iterations = 10000
attempts = 100
verbose = False
calculation_repeats = 100

g = CircleGenerator()

res_time = {}

with open(f"output/analysis_d2_circle_fastest_res_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}", 'w') as f:  
    for circle_percent in arange(0.01, max_circle_percent, 0.01):
        print(f"Circle percent: {circle_percent}")
        t = 0

        for repeat in range(calculation_repeats):
            t_start = time.time()
            _, _ = g.generate_with_circle_count(circle_radius, 
                                                circle_count, 
                                                axis_size,
                                                max_iteration=iterations, 
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


# v.vizualize(circle_radius, circles, axis_size)
# v.vizualize(circle_radius, shuffled, axis_size)

# data = {
#     'row=1|col=1': circles,
#     'row=1|col=2': shuffled
# }

# v.visualize_mutiple_charts(1, 2, circle_radius, axis_size, data)
