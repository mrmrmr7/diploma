from percolation.dimension2.star.draw import get_star_scatter
from numpy.lib.nanfunctions import nanmean
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import json

class Visualizer:
    def generate_accurate_star_points(self, _star, accuracy = 3):
        (x_arr, y_arr) = generate_star_points(_star)

        accuracy = 3
        x_new_arr = []
        y_new_arr = []
        zip_points = zip(x_arr[:-1], x_arr[1:], 
                        y_arr[:-1], y_arr[1:])

        for (x, x_next, y, y_next) in zip_points:
            dx = (x_next - x) / accuracy
            dy = (y_next - y) / accuracy

            for i in range(accuracy):
                x_new_arr.append(x + i * dx)
                y_new_arr.append(y + i * dy)

        return (x_new_arr,y_new_arr)

    def generate_star_points(self, _star):
        r_inner = _star["r_inner"]
        r_outer = _star["r_outer"]
        phi_0 = _star["phi_0"]
        x = _star["x"]
        y = _star["y"]

        x_arr = []
        y_arr = []
        step = 72

        for i in range(6):
            rads = np.deg2rad(step * i + phi_0)

            x_arr.append(-r_outer*np.sin(rads) + x)
            y_arr.append(r_outer*np.cos(rads) + y)

            rads = np.deg2rad(step * i + 36 + phi_0)

            x_arr.append(-r_inner*np.sin(rads) + x)
            y_arr.append(r_inner*np.cos(rads) + y)

        return (x_arr, y_arr)

    # def get_ellipce_scatter(self, _ellipse):
    #     t = np.linspace(0, 2*np.pi + 5.1, 101)
    #     x0 = _ellipse["a"] * np.cos(t)
    #     y0 = _ellipse["b"] * np.sin(t)

    #     x_new = []
    #     y_new = []

    #     for (x, y) in zip(x0, y0):
    #         phi = _ellipse["phi_0"]
    #         x_move = _ellipse["x"]
    #         y_move = _ellipse["y"]
    #         rads = np.deg2rad(phi)
    #         x_new.append(x*np.cos(rads)-y*np.sin(rads)+x_move)
    #         y_new.append(x*np.sin(rads)+y*np.cos(rads)+y_move)

    #     return go.Scatter(
    #         x=x_new,
    #         y=y_new,
    #         line={"width": 10}
    #         )
    
    def get_star_scatter(self, _star, _type = "simple", accuracy = 3):
        x_arr = []
        y_arr = []
        if _type == "simple": 
            (x_arr, y_arr) = self.generate_star_points(_star)
        if _type == "accurate":
            (x_arr, y_arr) = self.generate_accurate_star_points(_star, accuracy)
        return go.Scatter(
            x=x_arr,
            y=y_arr
            )
    
    def vizualize(self, _stars, axis_size, r_inner, r_outer):
        _p={
            "r_inner": r_inner,
            "r_outer": r_outer,
            "x_max": axis_size,
            "y_max": axis_size,
            "layout_w": 1000,
            "layout_h": 1000,
        }
        
        fig = go.Figure(
            layout=go.Layout( 
                width=_p["layout_w"],
                height=_p["layout_h"],
                xaxis={"range": [-_p["r_outer"], _p["x_max"]+_p["r_outer"]]},
                yaxis={"range": [-_p["r_outer"], _p["y_max"]+_p["r_outer"]]},
                )
            )

        for each in _stars:
            star_dict = json.loads(each)
            fig.add_trace(get_star_scatter(star_dict))
        
        return fig

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
