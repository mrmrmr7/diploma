import numpy as np
import plotly.graph_objects as go
import math as m


def spheres(position={'x':0, 'y':0, 'z':0}, size=0.5, accuracy=50):
    phi = np.linspace(0, 2*np.pi)
    theta = np.linspace(-np.pi/2, np.pi/2)
    phi, theta=np.meshgrid(phi, theta)

    x0 = position['x'] + np.cos(theta) * np.sin(phi) * 3
    y0 = position['y'] + np.cos(theta) * np.cos(phi) * 2
    z0 = position['z'] + np.sin(theta)
    
    trace= go.Surface(x=x0, y=y0, z=z0)
    trace.update(showscale=False)

    return trace

traces = []
accuracy = 5
R = 1
h = m.sqrt(2)*R

aspect_ratio = 1.5
x_range = 5
y_range = 5
z_range = 5
x_count = int(x_range / (2 * h))
y_count = int((y_range - R) / h)
z_count = int((z_range - R) / h)

for iz in range(z_count):
    for iy in range(y_count):
        for ix in range(x_count):
            next_x = 0
            if iz % 2 == 0:
                next_x = aspect_ratio * (ix * 2 * h + (iy % 2 + 1) * h)
            else:
                next_x = aspect_ratio * (ix * 2 * h + (iy % 2) * h + ((iy + 1) % 2) * 2 * h)
            next_y = aspect_ratio * (iy + 1) * h
            next_z = aspect_ratio * (iz + 1) * h
            traces.append(
                spheres(
                    position={'x': next_x,'y': next_y,'z': next_z}, 
                    accuracy=accuracy, 
                    size=R
                )
            )

fig = go.Figure(data=traces)

fig.update_layout(
    scene = {
        'xaxis': {'range':[0,x_range]},
        'yaxis': {'range':[0,y_range]},
        'zaxis': {'range':[0,z_range]},
        "aspectratio": {"x": 1, "y": 1, "z": 1}
    }
)

fig.show()
