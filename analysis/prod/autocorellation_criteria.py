import sys

sys.path.append('.')

from percolation.dimension2.circle.generator.simple.tight_packing_based_generator import CircleGenerator
from percolation.dimension2.circle.visualizer import CircleVisualizer
from pprint import pprint
import plotly.graph_objects as go
import scipy.stats
import math as m

g = CircleGenerator()
v = CircleVisualizer()

gen_count = 10
circles_count = 50
axis_size = 10
circles_data = []
for igen in range(gen_count):
    print(igen)
    circles_data.append(g.generate_with_circle_count(
                            circle_radius=0.5,
                            circle_count=circles_count,
                            axis_size=axis_size,
                            verbose=True
                        ))
    
index_based_data = {}
for index in range(1, circles_count):
    x_arr = []
    y_arr = []
    for iteration in circles_data:
        for circle in iteration:
            if circle['index'] == index:
                x_arr.append(circle['x'])
                y_arr.append(circle['y'])
                break
            
    index_based_data[index] = {'x_arr': x_arr, 'y_arr': y_arr}

def calculate_autocorrelation(input_data):
    data = sorted(input_data)
    max_val = data[-1]
    data = [ d / max_val for d in data ]
    sumiandinext = 0
    sumi = 0
    sumisquare = 0
    
    n = len(data)
    for i in range(1, n - 1):
        sumiandinext += data[i] * data[i + 1]
        
    for i in range(n):
        sumi += data[i]
        sumisquare += data[i] ** 2
        
    top = (n * sumiandinext - sumi ** 2 + n * data[0] * data[-1])
    bot = (n * sumisquare - sumi ** 2)
    r1n = top / bot
    
    mr1n = - 1 / (n - 1)
    dr1n = (n * (n - 3)) / ((n + 1) * (n - 1) ** 2)
    
    r = abs(r1n - mr1n) / m.sqrt(dr1n)
    
    return abs(r)


fig = go.Figure()

normally_located = 0
unnormally_located = 0

for index, values in index_based_data.items():
    
    alpha = scipy.stats.norm.ppf(0.975)
    
    rx = calculate_autocorrelation(values['x_arr'])
    ry = calculate_autocorrelation(values['y_arr'])    
    r = min(rx, ry)
    is_normally_located = r < alpha
    if is_normally_located:
        normally_located += 1
    else:
        unnormally_located += 1
    print(f"Alpha: {round(alpha, 3)} index:{index} R: {round(r, 3)} is located normally: {is_normally_located}")
    
    fig.add_trace(go.Scatter(
        x = values['x_arr'],
        y = values['y_arr'], 
        name=f'index: {index}',
        line=dict(color='green' if is_normally_located else 'red') 
    ))
    
    
print(f'Normally located: {normally_located}')
print(f'Unormally located: {unnormally_located}')
print(f'Is full location normally: {normally_located > unnormally_located}')

fig.update_layout(
    width=1000,
    height=1000,
    xaxis={"range":[0, axis_size]},
    yaxis={"range":[0, axis_size]})

fig.show()