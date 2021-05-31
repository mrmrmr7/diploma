from percolation.dimensions2.circle.generators.simple_generator import CircleGenerator
from percolation.dimensions2.circle.visualizer import CircleVisualizer

circle_radius = 0.5
circle_count = 70
axis_size = 10
iterations_count = 1000
attempts = 100
verbose = True

g = CircleGenerator()
v = CircleVisualizer()

circles = g.generate_with_circle_count(circle_radius, 
                                        circle_count, 
                                        axis_size, 
                                        max_iteration=iterations_count, 
                                        attempts=attempts, 
                                        verbose=verbose)
# v.vizualize(circle_radius, circles, axis_size)

