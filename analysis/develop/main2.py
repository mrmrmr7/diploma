from percolation.dimension2.circle.generator.simple_generator import CircleGenerator
from percolation.dimension2.circle.visualizer import CircleVisualizer

circle_radius = 0.5
circle_count = 70
circle_percent = 0.55
iterations_count = 1000
attempts = 100
verbose = True

g = CircleGenerator()
v = CircleVisualizer()

circles, axis_size = g.generate_with_circle_percent(circle_radius, 
                                                    circle_count, 
                                                    circle_percent, 
                                                    max_iteration=iterations_count, 
                                                    attempts=attempts, 
                                                    verbose=verbose)
v.vizualize(circle_radius, circles, axis_size)

