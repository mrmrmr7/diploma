from percolation.dimensions2.circle.generators.fastest_generator import CircleGenerator
from percolation.dimensions2.circle.visualizer import CircleVisualizer

circle_radius = 0.5
circle_count = 70
circle_percent = 0.5
iterations = 1000
axis_size = 10
attempts = 100
verbose = True

g = CircleGenerator()
v = CircleVisualizer()

circles, shuffled = g.generate_with_circle_count(circle_radius,
                                                circle_count,
                                                axis_size,
                                                max_iteration=iterations,
                                                attempts=attempts,
                                                verbose=verbose)

data = {
    'row=1|col=1': circles,
    'row=1|col=2': shuffled
}

v.visualize_mutiple_charts(1, 2, circle_radius, axis_size, data)
