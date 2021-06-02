from scipy.spatial.distance import euclidean as dist
from scipy.spatial.distance import euclidean as distance
import math as m
import random
from operator import itemgetter as get


class Analyzer:
    def calculate_r(self, phi, phi_0, a, b, **kvargs):
        phi_actual_rad = phi * m.pi / 180.0
        return (a * b)/m.sqrt(b**2 * m.cos(phi_actual_rad)**2 + a**2 * m.sin(phi_actual_rad)**2)

    def calculate_phi(self, _ellipse1, _ellipse2):
        dx = _ellipse2['x']-_ellipse1['x']
        dy = _ellipse2['y']-_ellipse1['y']

        if dx == 0:
            return (90 + _ellipse1["phi_0"], 90 + _ellipse2["phi_0"])

        e1e2_tan = dy/dx
        tan_phi = m.atan(e1e2_tan) * 180.0 / m.pi
        e1_phi = 180.0 - tan_phi + _ellipse1["phi_0"]
        e2_phi = tan_phi - _ellipse2["phi_0"]

        e1_phi = e1_phi if e1_phi < 0 else e1_phi - 180
        e2_phi = e2_phi if e2_phi < 0 else e2_phi - 180
        return (e1_phi, e2_phi)

    def ellipse_dist(self, _ellipse1, _ellipse2):
        return distance(get("x", "y")(_ellipse1),
                        get("x", "y")(_ellipse2))

    def is_ellipses_intersect(self, _ellipse1, _ellipse2, coef):
        (e1_phi, e2_phi) = self.calculate_phi(_ellipse1, _ellipse2)
        r1 = self.calculate_r(phi=e1_phi, **_ellipse1)
        r2 = self.calculate_r(phi=e2_phi, **_ellipse2)
        dist = self.ellipse_dist(_ellipse1, _ellipse2)
        return (r1 + r2) * coef > dist

    def split_on_clusters(self, ellipces, coef):
        markers = {i['index']: i['index'] for i in ellipces}
        for i in range(len(ellipces)):
            for j in [*range(0, i), *range(i + 1, len(ellipces))]:
                if self.is_ellipses_intersect(ellipces[i], ellipces[j], coef):
                    i_marker = markers[ellipces[i]['index']]
                    j_marker = markers[ellipces[j]['index']]
                    circles_with_marker_i = [
                        k for k, v in markers.items() if v == i_marker]
                    for c in circles_with_marker_i:
                        markers[c] = j_marker
        clusters = {i: [] for i in set(markers.values())}
        for k, v in markers.items():
            clusters[v] = clusters[v] + [k]
        return clusters

    def get_clusters_ranges(self, circles, clusters):
        clusters_ranges = {}

        for k, v in clusters.items():
            cluster_circles = [i for i in circles if i['index'] in v]
            min_x = min([c['x'] for c in cluster_circles])
            max_x = max([c['x'] for c in cluster_circles])
            min_y = min([c['y'] for c in cluster_circles])
            max_y = max([c['y'] for c in cluster_circles])

            clusters_ranges[k] = {'min_x': min_x, 'max_x': max_x,
                                  'min_y': min_y, 'max_y': max_y, }

        return clusters_ranges

    def _get_biggest_cluster(self, clusters_ranges):
        sizes = [(k, v['max_x'] - v['min_x'])
                 for k, v in clusters_ranges.items()]
        return max(sizes, key=lambda x: x[1])

    def get_biggest_cluster(self, ellipces, coef):
        clusters = self.split_on_clusters(ellipces, coef)
        clusters_ranges = self.get_clusters_ranges(ellipces, clusters)
        biggest_cluster_number = self._get_biggest_cluster(clusters_ranges)

        cluster_max = [biggest_cluster_number[0],
                       *(clusters[biggest_cluster_number[0]])]
        biggest_cluster = [c for c in ellipces if c['index'] in cluster_max]

        return biggest_cluster, {'size': biggest_cluster_number[1] + 2 * ellipces[0]['a']}
