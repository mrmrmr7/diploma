
from visualizator import Visualizator
from statistic import Statistic
from generator import GeneratorOf3DSpheres as Generator
from uniform_generator import GeneratorOf3DSpheres as UniformGenerator

accuracy = 30
sphere_size = 1
sphere_fill_percent = 0.02
sphere_count = 70
pocket_count = 5

generator = Generator(sphere_count, sphere_size, sphere_fill_percent) #, pocket_count)
visualizator = Visualizator(generator, accuracy=accuracy)

spheres = generator.get_uniform_distributed_spheres()

# statistic = Statistic(spheres, generator.ranges)

# stats = statistic.get_all_statistic(pocket_count=pocket_count)
visualizator.display(spheres)
# visualizator.display_all_results(stats) 