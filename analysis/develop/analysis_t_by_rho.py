from percolation.dimensions2.circle.generators.simple_generator import CircleGenerator
from percolation.dimensions2.circle.visualizer import CircleVisualizer
import plotly.graph_objects as go
import time 

circle_radius = 0.5
max_circle_count = 70
circle_percent = 0.55
axis_size = 10
iterations_count = 10000
attempts = 100
verbose = True
calculation_repeats = 100

g = CircleGenerator()

res_time = {}

for circle_count in range(1, max_circle_count + 1):
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

    res_time[circle_count] = t / calculation_repeats



fig = go.Figure(data=go.Scatter(
        x=list(res_time.keys()), 
        y=list(res_time.values())))

fig.update_layout(title="Generation time t depending on circle count n")
fig.show()


# v.vizualize(circle_radius, circles, axis_size)
