import numpy as np

with open("output/2d/ellipce/biggest_cluster/arange.txt", "w") as f:
    f.write(":".join(map(lambda x: format(x, '.3f'), list(np.arange(0.1, 1.05, 0.05)))))