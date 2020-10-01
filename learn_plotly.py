import plotly.graph_objects as go
import pandas as pd
import numpy as np

n = 10 
square_vertex_size = 1000

x_arr = np.tile(np.arange(n), n)
y_arr = np.repeat(np.arange(n), n)

shapes = [
    {
        "type":"circle",
        "xref":"x",
        "yref":"y",
        "x0":(x-0.5),
        "y0":(y-0.5),
        "x1":(x+0.5),
        "y1":(y+0.5),
        "line_color":"LightSeaGreen",
    }

    for (x, y) in zip(x_arr, y_arr)
]

layout = go.Layout( 
    width=1000,
    height=1000,
    shapes=shapes,
    xaxis={"range":[-1, n]},
    yaxis={"range":[-1,n]}
)

fig = go.Figure(layout=layout)

fig.show()