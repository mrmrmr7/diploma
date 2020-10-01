import numpy as np 
from matplotlib import pyplot as plt
from random import randint
from math import sin, sqrt

fig, ax = plt.subplots()
r = 1.5

x_counts = 2
y_counts = x_counts
x_step = 2
y_step = x_step

n = 2 * 2

ax.set_xlim(- r, x_counts * x_step - r)
ax.set_ylim(- r, y_counts * y_step - r)

init_points = []
for x_i in range(x_counts):
    for y_i in range(y_counts):
        init_points.append((x_i * x_step, y_i * y_step))

all_combinations = {}
for e_1 in init_points:
    e_1_list = []
    for e_2 in init_points:
        distance = sqrt(
            (e_2[0]-e_1[0]) ** 2 + (e_2[1]-e_1[1]) ** 2
            )

        if distance >= r:
            e_1_list.append(e_2)

    all_combinations[e_1] = e_1_list

# while len(all_combinations) > 0:
#     p = all_combinations[0]
    

#     all_combinations = []

# print(all_combinations)

connection_counts = n - 1

for (k, v) in all_combinations.items():
    print(all_combinations)
    print()

    if len(v) == connection_counts:
        ax.add_patch(plt.Circle(
                        k, 
                        radius=r, 
                        color='black', 
                        fill=True))

        for e_v in v:
            a = all_combinations[e_v]
            a.remove(k)
            all_combinations[e_v] =  a
        
        connection_counts -= 1
        
    del all_combinations[k]

plt.show()