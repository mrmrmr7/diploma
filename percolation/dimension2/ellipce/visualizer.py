from numpy.lib.nanfunctions import nanmean
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import json

class Visualizer:
    def get_ellipce_scatter(self, _ellipse):
        t = np.linspace(0, 2*np.pi + 5.1, 201)
        x0 = _ellipse.a * np.cos(t)
        y0 = _ellipse.b * np.sin(t)

        x_new = []
        y_new = []

        for (x, y) in zip(x0, y0):
            phi = _ellipse.phi
            x_move = _ellipse.x
            y_move = _ellipse.y
            rads = np.deg2rad(phi)
            x_new.append(x*np.cos(rads)-y*np.sin(rads)+x_move)
            y_new.append(x*np.sin(rads)+y*np.cos(rads)+y_move)

        return go.Scatter(
            x=x_new,
            y=y_new,
            line={"width": 2, "color": "black"}, 
            name=f"ellipce {_ellipse.index}"
            )
        
    def vizualize(self, ellipces, axis_size, size=1000, legend=False, title_text="New Picture"):
        layout = go.Layout( 
            width=size,
            height=size,
            xaxis={"range": [0, axis_size]},
            yaxis={"range": [0, axis_size]},
            paper_bgcolor='rgb(255,255,255)',
            plot_bgcolor='rgb(255,255,255)'
        )

        fig = go.Figure(layout=layout)

        fig.update_layout(showlegend=legend)
        fig.update_layout(title_text=title_text)

        for each in ellipces:
            fig.add_trace(self.get_ellipce_scatter(each))

        fig.update_yaxes(range=[0, axis_size])
        fig.update_xaxes(range=[0, axis_size])
        fig.update_xaxes(showline=True, linewidth=10, linecolor='black', mirror=True)
        fig.update_yaxes(showline=True, linewidth=10, linecolor='black', mirror=True)
        fig.show()

    def visualize_mutiple_charts(self, rows, cols, circle_radius, axis_size, data_dict):
        fig = make_subplots(rows=rows, cols=cols)

        for k, v in data_dict.items():
            shapes = [
                {
                    "type": "circle",
                    "xref": "x",
                    "yref": "y",
                    "x0": (x-circle_radius),
                    "x1": (x+circle_radius),
                    "y0": (y-circle_radius),
                    "y1": (y+circle_radius),
                    "line_color": "LightSeaGreen",
                } for (x, y) in v
            ]

            splited = k.split("|")
            row = int(splited[0].split("=")[1])
            col = int(splited[1].split("=")[1])

            for shape in shapes:
                fig.add_shape(shape, row=row, col=col)
                fig.update_yaxes(range=[0, axis_size])
                fig.update_xaxes(range=[0, axis_size])

        fig.show()
