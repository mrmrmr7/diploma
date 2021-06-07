
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


class Visualizator:
    def __init__(self, generator, accuracy):
        self.generator = generator
        self.accuracy = accuracy
        self.ranges = generator.ranges

    def get_spheres_traces(self, positions=None):
        print('\nTraces generation start.')
        accuracy = self.accuracy
        size = self.generator.sphere_size
        spheres = positions if any(
            positions) else self.generator.shuffled_extended_spheres

        theta = np.linspace(0, 2*np.pi, accuracy)
        phi = np.linspace(0, np.pi, accuracy)
        phi, theta = np.meshgrid(phi, theta)

        traces = []
        for s in spheres:
            x = s['x'] + size * np.cos(theta) * np.sin(phi)
            y = s['y'] + size * np.sin(theta) * np.sin(phi)
            z = s['z'] + size * np.ones(accuracy) * np.cos(phi)

            traces.append(go.Surface(
                x=x, 
                y=y, 
                z=z, 
                showscale=False, 
                lighting=dict(diffuse=0))
            )

        print('Traces generation done.\n')
        return traces

    def display(self, positions=None, display_all=False):
        positions = positions if positions else self.generator.shuffled_extended_spheres
        traces = self.get_spheres_traces(positions)
        ranges = self.ranges

        if display_all:
            return traces
        else:
            fig = go.Figure()

            [fig.add_trace(t) for t in traces]

            fig.update_layout(
                scene={
                    'xaxis': {'range': [0, ranges['x']], 'showbackground': False},
                    'yaxis': {'range': [0, ranges['y']], 'showbackground': False},
                    'zaxis': {'range': [0, ranges['z']], 'showbackground': False},
                    "aspectratio": {"x": 1, "y": 1, "z": 1}
                }
            )
            
            fig.update_layout(
                yaxis_tickformat=',d',
                separators=',.'
            )

            fig.show()

    def display_distribution(self, distribution_results, display_all=False):
        fits = distribution_results['axis_fits']
        distributions = distribution_results['axis_distributions']
        is_uniform = distribution_results['is_axis_uniform']
        a = distribution_results['fit_a_coef']

        fig = go.Figure()
        traces = []

        for p, f in zip(fits.items(), distributions.items()):
            y = [*p[1], None, *f[1]]
            x = [*range(len(p[1])), None, *range(len(f[1]))]
            name = f"{p[0]}. a: {format(a[p[0]], '.2f')}. Uniform: {is_uniform[p[0]]}"

            traces.append(go.Scatter(
                x=x, y=y, mode='lines+markers', name=name))

        if display_all:
            return traces
        else:
            [fig.add_trace(t) for t in traces]
            fig.show()

    def display_all_results(self, distribution_results, positions=None):
        ranges = self.ranges
        traces_spheres = self.display(positions, display_all=True)
        traces_points = self.display_distribution(
            distribution_results, display_all=True)

        fig = make_subplots(
            rows=3,
            cols=2,
            specs=[
                [{'type': 'surface', 'rowspan': 3}, {}],
                [{}, {'type': 'xy'}],
                [{}, {}]
            ]).update_layout(
            scene={
                'xaxis': {'range': [0, ranges['x']]},
                'yaxis': {'range': [0, ranges['y']]},
                'zaxis': {'range': [0, ranges['z']]},
                "aspectratio": {"x": 1, "y": 1, "z": 1}
            }
        )

        [fig.add_trace(t, row=1, col=1) for t in traces_spheres]
        [fig.add_trace(t, row=2, col=2) for t in traces_points]

        fig.show()
