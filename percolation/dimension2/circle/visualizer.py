from numpy.lib.nanfunctions import nanmean
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class CircleVisualizer:
    def vizualize(self, circle_radius, circle_centers, axis_size, title=' ', add_grid=False):
        shapes = [
            {
                "type": "circle",
                "xref": "x",
                "yref": "y",
                "x0": (x-circle_radius),
                "x1": (x+circle_radius),
                "y0": (y-circle_radius),
                "y1": (y+circle_radius),
                "line": {
                    "color": "black",
                    "width": 12
                }
            } for (x, y) in circle_centers
        ]

        layout = go.Layout( 
            title=title,
            width=1000,
            height=1000,
            shapes=shapes,
            xaxis={"range":[0, axis_size]},
            yaxis={"range":[0, axis_size]},
            paper_bgcolor='rgb(255,255,255)',
            plot_bgcolor='rgb(255,255,255)'
        )
        
        fig = go.Figure(layout=layout)
        if add_grid:
            fig.update_xaxes(showgrid=True, gridwidth=3, gridcolor='Gray')
            fig.update_yaxes(showgrid=True, gridwidth=3, gridcolor='Gray')
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
