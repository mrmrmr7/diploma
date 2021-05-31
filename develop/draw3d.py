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
accuracy = 10
count = 2
R = 1
step = m.sqrt(7*R)
for iz in np.arange(0, count):
    for iy in np.arange(0, count):
        for ix in np.arange(0, count):
            x = ix * step
            y = iy * step
            z = iz * step

            traces.append(
                spheres(
                    position={'x':x,'y':y,'z':z}, 
                    accuracy=accuracy, 
                    size=R
                    )
                )

            if x < count - 1:
                if y < count - 1:
                    if z < count - 1:
                        traces.append(
                            spheres(
                                position={'x':x + step * 0.5,'y':y + step * 0.5,'z':z}, 
                                accuracy=accuracy, 
                                size=R
                                )
                            )
                        traces.append(
                            spheres(
                                position={'x':x + step * 0.5,'y':y,'z':z + step * 0.5}, 
                                accuracy=accuracy, 
                                size=R
                                )
                            )
                        traces.append(
                            spheres(
                                position={'x':x,'y':y + step * 0.5,'z':z + step * 0.5}, 
                                accuracy=accuracy, 
                                size=R
                                )
                            )
                        traces.append(
                            spheres(
                                position={'x':x + step,'y':y + step * 0.5,'z':z + step * 0.5}, 
                                accuracy=accuracy, 
                                size=R
                                )
                            )
                        traces.append(
                            spheres(
                                position={'x':x + step * 0.5,'y':y + step,'z':z + step * 0.5}, 
                                accuracy=accuracy, 
                                size=R
                                )
                            )
                        traces.append(
                            spheres(
                                position={'x':x + step * 0.5,'y':y + step * 0.5,'z':z + step}, 
                                accuracy=accuracy, 
                                size=R
                                )
                            )

fig = go.Figure(data=traces)
fig.show()
