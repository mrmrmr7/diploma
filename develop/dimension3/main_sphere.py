import sys
sys.path.append('.')

from percolation.dimension3.sphere.generator import GeneratorOf3DSpheres
from percolation.dimension3.sphere.visualizator import Visualizator

accuracy = 30
sphere_size = 1
sphere_fill_percent = 0.02
sphere_count = 70
pocket_count = 5

generator = GeneratorOf3DSpheres(sphere_count, sphere_size, sphere_fill_percent) #, pocket_count)
visualizator = Visualizator(generator, accuracy=accuracy)

spheres = generator.get_uniform_distributed_spheres()

# statistic = Statistic(spheres, generator.ranges)

# stats = statistic.get_all_statistic(pocket_count=pocket_count)
visualizator.display(spheres)
# visualizator.display_all_results(stats) 