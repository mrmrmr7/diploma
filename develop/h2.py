import numpy as np
import plotly.graph_objects as go
import math as m

def spheres(position={'x':0, 'y':0, 'z':0}, size=0.5, accuracy=50):
    theta = np.linspace(0, 2*np.pi, accuracy)
    phi = np.linspace(0, np.pi, accuracy)
    
    x0 = position['x'] + size * np.outer(np.cos(theta), np.sin(phi))
    y0 = position['y'] + size * np.outer(np.sin(theta), np.sin(phi))
    z0 = position['z'] + size * np.outer(np.ones(accuracy), np.cos(phi))
    
    trace= go.Surface(x=x0, y=y0, z=z0)
    trace.update(showscale=False)

    return trace

traces = []
accuracy = 30
count = 2
R = 1
x_range = 10
y_range = 10
z_range = 10
x_count = int(x_range / (2 * m.sqrt(2) * R))
y_count = int((y_range - R) / (m.sqrt(2) * R))
z_count = int((z_range - R) / (m.sqrt(2) * R))
print(f"x_count: {x_count}")
print(f"y_count: {y_count}")
print(f"z_count: {z_count}")

h = m.sqrt(2)*R

for iy in range(y_count):
    for ix in range(x_count):
        traces.append(
            spheres(
                position={
                    'x':(iy % 2) * h + ix*2*h,
                    'y':(iy+1)*h,
                    'z':h
                    }, 
                accuracy=accuracy, 
                size=R
                )
        )

# for ix in range(x_count):
#     traces.append(
#         spheres(position={'x':ix*2*h,'y':h,'z':h}, accuracy=accuracy, size=R)
#     )

# for ix in range(x_count):
#     traces.append(
#         spheres(position={'x':h+ix*2*h,'y':2*h,'z':h}, accuracy=accuracy, size=R)
#     )


# for ix in range(x_count):
#     traces.append(
#         spheres(position={'x':ix*2*h,'y':3*h,'z':h}, accuracy=accuracy, size=R)
#     )


traces.append(
    spheres(position={'x':h,'y':2*h,'z':h}, accuracy=accuracy, size=R)
    )
traces.append(
    spheres(position={'x':3*h,'y':2*h,'z':h}, accuracy=accuracy, size=R)
    )
traces.append(
    spheres(position={'x':4*h,'y':h,'z':h}, accuracy=accuracy, size=R)
    )
traces.append(
    spheres(position={'x':2*h,'y':h,'z':h}, accuracy=accuracy, size=R)
    )


fig = go.Figure(data=traces)
fig.show()
